from django import forms
from .models import BlogPost
from django.core.validators import MinLengthValidator


class BlogPostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        validators=[MinLengthValidator(5, "Title must be at least 5 characters long")],
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter post title", "autofocus": True}
        ),
    )

    body = forms.CharField(
        validators=[MinLengthValidator(20, "Content must be at least 20 characters long")],
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 12,
                "placeholder": "Write your post content here...",
                "style": "font-family: monospace;",
            }
        ),
        help_text=(
            "You can use Markdown for formatting: **bold**, *italic*, "
            "[links](https://example.com), and more."
        ),
    )

    class Meta:
        model = BlogPost
        fields = ["title", "body"]

    def clean_title(self):
        """Custom validation for title field"""
        title = self.cleaned_data.get("title")
        if title and title.lower() == "test":
            raise forms.ValidationError("Please choose a more descriptive title")
        return title
