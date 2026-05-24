from django import forms

from .models import ContentCalendar, ContentProject, GeneratedContent


class ContentGenerationForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "input-field",
            "placeholder": "Project title (e.g. Django AI Tutorial Blog)",
        }),
    )
    content_type = forms.ChoiceField(
        choices=ContentProject.CONTENT_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "input-field"}),
    )
    topic = forms.CharField(
        max_length=300,
        widget=forms.TextInput(attrs={
            "class": "input-field",
            "placeholder": "Main topic",
        }),
    )
    keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "input-field",
            "placeholder": "SEO keywords (comma-separated)",
        }),
    )
    target_audience = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "input-field",
            "placeholder": "e.g. beginner developers, marketers",
        }),
    )
    word_count = forms.IntegerField(
        min_value=100,
        max_value=5000,
        initial=800,
        widget=forms.NumberInput(attrs={"class": "input-field"}),
    )
    tone = forms.ChoiceField(
        choices=GeneratedContent.TONE_CHOICES,
        widget=forms.Select(attrs={"class": "input-field"}),
    )


class ContentEditForm(forms.ModelForm):
    class Meta:
        model = GeneratedContent
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "input-field font-mono text-sm",
                "rows": 20,
            }),
        }


class CalendarEntryForm(forms.ModelForm):
    class Meta:
        model = ContentCalendar
        fields = ["date", "title", "status", "notes", "content"]
        widgets = {
            "date": forms.DateInput(attrs={"class": "input-field", "type": "date"}),
            "title": forms.TextInput(attrs={"class": "input-field"}),
            "status": forms.Select(attrs={"class": "input-field"}),
            "notes": forms.Textarea(attrs={"class": "input-field", "rows": 3}),
            "content": forms.Select(attrs={"class": "input-field"}),
        }
