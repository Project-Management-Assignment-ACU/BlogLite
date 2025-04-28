"""Blog uygulaması için Django uygulama yapılandırmasını içerir."""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Blog uygulamasının yapılandırma sınıfı."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
