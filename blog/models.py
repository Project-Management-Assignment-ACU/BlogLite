"""Blog uygulaması için veritabanı modellerini içerir."""

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class BlogPost(models.Model):
    """Blog gönderilerini temsil eden model sınıfı.

    Bu sınıf, blog gönderilerinin başlık, içerik, yazar ve zaman bilgilerini saklar.
    Ayrıca SEO dostu URL'ler için slug alanı içerir.
    """

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")

    class Meta:
        """Meta sınıfı blog gönderilerinin sıralama düzenini belirler."""

        ordering = ["-created_on"]

    def __str__(self):
        """Blog gönderisinin string temsilini döndürür."""
        return self.title

    def save(self, *args, **kwargs):
        """Blog gönderisini kaydeder ve otomatik olarak slug oluşturur."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Blog gönderisinin detay sayfasının URL'sini döndürür."""
        return reverse("blog:post_detail", kwargs={"slug": self.slug})
