"""Blog uygulaması için admin panel yapılandırmasını içerir."""

from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """Blog gönderilerinin admin panel yapılandırması.

    Bu sınıf, admin panelinde blog gönderilerinin nasıl görüntüleneceğini,
    filtreleneceğini ve düzenleneceğini belirler.
    """

    list_display = ("title", "slug", "author", "created_on")
    list_filter = ("created_on", "author")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_on"
    ordering = ("-created_on",)
