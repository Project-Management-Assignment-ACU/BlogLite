"""Blog uygulaması için form sınıflarını içerir.

Bu modül, blog gönderilerinin oluşturulması ve düzenlenmesi için gerekli
form sınıflarını içerir.
"""

from django import forms
from django.core.validators import MinLengthValidator

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    """Blog gönderisi oluşturma ve düzenleme formu.

    Bu form, blog gönderilerinin başlık ve içerik alanlarını içerir.
    Her iki alan için minimum uzunluk doğrulaması yapar ve
    Markdown formatında içerik girişini destekler.
    """

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
        """Form meta sınıfı model ve alan bilgilerini içerir."""

        model = BlogPost
        fields = ["title", "body"]

    def clean_title(self):
        """Başlık alanı için özel doğrulama yapar.

        'test' kelimesinin başlık olarak kullanılmasını engeller.
        """
        title = self.cleaned_data.get("title")
        if title and title.lower() == "test":
            raise forms.ValidationError("Please choose a more descriptive title")
        return title
