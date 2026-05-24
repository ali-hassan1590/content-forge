from django.conf import settings
from django.db import models


class ContentProject(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("in_progress", "In Progress"),
        ("published", "Published"),
    ]
    CONTENT_TYPE_CHOICES = [
        ("blog", "Blog Post"),
        ("youtube", "YouTube Script"),
        ("instagram", "Instagram Caption"),
        ("linkedin", "LinkedIn Article"),
        ("email", "Email Newsletter"),
        ("twitter", "Twitter/X Thread"),
        ("podcast", "Podcast Outline"),
    ]

    title = models.CharField(max_length=200)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class GeneratedContent(models.Model):
    TONE_CHOICES = [
        ("professional", "Professional"),
        ("casual", "Casual"),
        ("funny", "Funny"),
        ("inspirational", "Inspirational"),
        ("persuasive", "Persuasive"),
    ]

    project = models.ForeignKey(
        ContentProject,
        on_delete=models.CASCADE,
        related_name="generations",
    )
    topic = models.CharField(max_length=300)
    keywords = models.CharField(max_length=500, blank=True)
    target_audience = models.CharField(max_length=200, blank=True)
    word_count = models.PositiveIntegerField(default=500)
    tone = models.CharField(max_length=30, choices=TONE_CHOICES, default="professional")
    content = models.TextField()
    seo_score = models.IntegerField(null=True, blank=True)
    seo_meta_title = models.CharField(max_length=70, blank=True)
    seo_meta_description = models.CharField(max_length=160, blank=True)
    seo_keywords_suggested = models.TextField(blank=True)
    readability_score = models.FloatField(null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    grammar_notes = models.TextField(blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self):
        return f"{self.topic[:50]} ({self.project.content_type})"

    @property
    def word_count_actual(self):
        return len(self.content.split())


class ContentCalendar(models.Model):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("draft", "Draft"),
        ("in_progress", "In Progress"),
        ("published", "Published"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="calendar_entries",
    )
    date = models.DateField()
    title = models.CharField(max_length=200)
    content = models.ForeignKey(
        GeneratedContent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="calendar_slots",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]
        verbose_name_plural = "Content calendar entries"

    def __str__(self):
        return f"{self.title} on {self.date}"
