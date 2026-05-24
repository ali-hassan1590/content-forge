from django.contrib import admin

from .models import ContentCalendar, ContentProject, GeneratedContent


class GeneratedContentInline(admin.TabularInline):
    model = GeneratedContent
    extra = 0
    readonly_fields = ("generated_at",)


@admin.register(ContentProject)
class ContentProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "content_type", "status", "created_at")
    list_filter = ("content_type", "status")
    search_fields = ("title", "user__username")
    inlines = [GeneratedContentInline]


@admin.register(GeneratedContent)
class GeneratedContentAdmin(admin.ModelAdmin):
    list_display = ("topic", "project", "seo_score", "word_count", "generated_at")
    list_filter = ("tone",)
    search_fields = ("topic", "content")


@admin.register(ContentCalendar)
class ContentCalendarAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "date", "status")
    list_filter = ("status", "date")
