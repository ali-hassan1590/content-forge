import json
from datetime import date

import markdown
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import CalendarEntryForm, ContentEditForm, ContentGenerationForm
from .models import ContentCalendar, ContentProject, GeneratedContent
from .services.ai import AIError, analyze_seo, check_grammar, generate_content, generate_image_url
from .services.seo import flesch_reading_ease, readability_label


@login_required
def generate_content_view(request):
    if request.method == "POST":
        form = ContentGenerationForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            cost = settings.CONTENT_GENERATION_COST
            if not profile.has_credits(cost):
                messages.error(request, f"Not enough credits. Need {cost}, have {profile.credits}.")
                return render(request, "generator/generate.html", {"form": form})

            data = form.cleaned_data
            try:
                body = generate_content(
                    content_type=data["content_type"],
                    topic=data["topic"],
                    keywords=data.get("keywords", ""),
                    target_audience=data.get("target_audience", ""),
                    word_count=data["word_count"],
                    tone=data["tone"],
                )
            except AIError as exc:
                messages.error(request, str(exc))
                return render(request, "generator/generate.html", {"form": form})

            project = ContentProject.objects.create(
                title=data["title"],
                user=request.user,
                content_type=data["content_type"],
                status="draft",
            )
            generated = GeneratedContent.objects.create(
                project=project,
                topic=data["topic"],
                keywords=data.get("keywords", ""),
                target_audience=data.get("target_audience", ""),
                word_count=data["word_count"],
                tone=data["tone"],
                content=body,
                readability_score=flesch_reading_ease(body),
            )
            profile.deduct_credits(cost)
            messages.success(request, "Content generated successfully!")
            return redirect("content_detail", pk=generated.pk)
    else:
        form = ContentGenerationForm()

    return render(request, "generator/generate.html", {"form": form})


@login_required
def content_detail(request, pk):
    content = get_object_or_404(
        GeneratedContent,
        pk=pk,
        project__user=request.user,
    )
    seo_data = None
    if content.seo_keywords_suggested:
        try:
            seo_data = {
                "suggested_keywords": json.loads(content.seo_keywords_suggested),
            }
        except json.JSONDecodeError:
            pass

    html_content = markdown.markdown(
        content.content,
        extensions=["extra", "nl2br"],
    )
    return render(request, "generator/content_detail.html", {
        "content": content,
        "html_content": html_content,
        "readability_label": readability_label(content.readability_score or 0),
        "edit_form": ContentEditForm(instance=content),
    })


@login_required
@require_POST
def content_edit(request, pk):
    content = get_object_or_404(GeneratedContent, pk=pk, project__user=request.user)
    form = ContentEditForm(request.POST, instance=content)
    if form.is_valid():
        updated = form.save(commit=False)
        updated.readability_score = flesch_reading_ease(updated.content)
        updated.save()
        messages.success(request, "Content saved.")
    else:
        messages.error(request, "Could not save content.")
    return redirect("content_detail", pk=pk)


@login_required
@require_POST
def analyze_seo_view(request, pk):
    content = get_object_or_404(GeneratedContent, pk=pk, project__user=request.user)
    profile = request.user.profile
    cost = settings.SEO_ANALYSIS_COST
    if not profile.has_credits(cost):
        messages.error(request, f"Not enough credits for SEO analysis ({cost} required).")
        return redirect("content_detail", pk=pk)

    try:
        result = analyze_seo(content.content, content.topic, content.keywords)
    except AIError as exc:
        messages.error(request, str(exc))
        return redirect("content_detail", pk=pk)

    content.seo_score = result.get("seo_score")
    content.seo_meta_title = result.get("meta_title", "")[:70]
    content.seo_meta_description = result.get("meta_description", "")[:160]
    content.seo_keywords_suggested = json.dumps(result.get("suggested_keywords", []))
    content.save()
    profile.deduct_credits(cost)

    if request.headers.get("HX-Request"):
        return render(request, "generator/partials/seo_results.html", {"seo": result})
    messages.success(request, "SEO analysis complete.")
    return redirect("content_detail", pk=pk)


@login_required
@require_POST
def grammar_check_view(request, pk):
    content = get_object_or_404(GeneratedContent, pk=pk, project__user=request.user)
    try:
        notes = check_grammar(content.content)
    except AIError as exc:
        messages.error(request, str(exc))
        return redirect("content_detail", pk=pk)

    content.grammar_notes = notes
    content.save()

    if request.headers.get("HX-Request"):
        return render(request, "generator/partials/grammar_results.html", {"notes": notes})
    messages.success(request, "Grammar check complete.")
    return redirect("content_detail", pk=pk)


@login_required
@require_POST
def generate_image_view(request, pk):
    content = get_object_or_404(GeneratedContent, pk=pk, project__user=request.user)
    profile = request.user.profile
    cost = settings.IMAGE_GENERATION_COST
    style = request.POST.get("style", "illustration")

    if not profile.has_credits(cost):
        messages.error(request, f"Not enough credits for image generation ({cost} required).")
        return redirect("content_detail", pk=pk)

    url = generate_image_url(content.topic, content.project.content_type, style)
    if url:
        content.image_url = url
        content.save()
        profile.deduct_credits(cost)
        messages.success(request, "Image generated!")
    else:
        messages.info(
            request,
            "Image API not configured. Add IMAGE_API_KEY for Flux/Ideogram integration.",
        )
    return redirect("content_detail", pk=pk)


@login_required
def export_content(request, pk, fmt):
    content = get_object_or_404(GeneratedContent, pk=pk, project__user=request.user)
    filename = f"{content.project.title[:40].replace(' ', '_')}"

    if fmt == "md":
        response = HttpResponse(content.content, content_type="text/markdown")
        response["Content-Disposition"] = f'attachment; filename="{filename}.md"'
        return response

    if fmt == "txt":
        response = HttpResponse(content.content, content_type="text/plain")
        response["Content-Disposition"] = f'attachment; filename="{filename}.txt"'
        return response

    messages.error(request, "Unsupported export format.")
    return redirect("content_detail", pk=pk)


@login_required
def calendar_view(request):
    entries = ContentCalendar.objects.filter(user=request.user).select_related("content")
    form = CalendarEntryForm()
    form.fields["content"].queryset = GeneratedContent.objects.filter(
        project__user=request.user,
    )

    if request.method == "POST":
        form = CalendarEntryForm(request.POST)
        form.fields["content"].queryset = GeneratedContent.objects.filter(
            project__user=request.user,
        )
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, "Calendar entry added.")
            return redirect("calendar")

    return render(request, "generator/calendar.html", {
        "entries": entries,
        "form": form,
        "today": date.today(),
    })


@login_required
@require_http_methods(["DELETE", "POST"])
def calendar_delete(request, pk):
    entry = get_object_or_404(ContentCalendar, pk=pk, user=request.user)
    entry.delete()
    if request.headers.get("HX-Request"):
        return HttpResponse("")
    messages.success(request, "Entry removed.")
    return redirect("calendar")


@login_required
def history_view(request):
    projects = ContentProject.objects.filter(user=request.user).prefetch_related(
        "generations",
    )
    return render(request, "generator/history.html", {"projects": projects})
