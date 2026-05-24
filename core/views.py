from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from generator.models import ContentProject, GeneratedContent


def home(request):
    return render(request, "core/home.html")


@login_required
def dashboard(request):
    user = request.user
    projects = ContentProject.objects.filter(user=user)
    generations = GeneratedContent.objects.filter(project__user=user)

    total_words = sum(g.word_count_actual for g in generations[:50])
    stats = {
        "project_count": projects.count(),
        "content_count": generations.count(),
        "total_words": total_words,
        "credits": user.profile.credits,
        "recent": generations.select_related("project")[:5],
        "by_type": list(
            projects.values("content_type")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        ),
    }
    return render(request, "core/dashboard.html", stats)
