from django import forms
from .models import CustomUser, Snippet, languages

# SnippetSaveForm

class SnippetSaveForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ["title", "code", "language", "author"]

# UserEditForm

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "image"]

# SnippetGenerationForm

class SnippetGenerationForm(forms.Form):
    LANGUAGE_CHOICES = languages

    PROBLEM_CHOICES = [
        ("bug_fix", "Bug Fix"),
        ("algorithm", "Algorithm"),
        ("project set up", "Project set up"),
    ]

    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, label="Programming Language")
    problem_type = forms.ChoiceField(choices=PROBLEM_CHOICES, label="Problem Type")
    explanation = forms.CharField(
        widget=forms.Textarea, label="Explanation", max_length=500
    )
