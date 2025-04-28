"""Proje seviyesinde URL yapılandırmalarını içerir."""

from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "core"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.HomeView.as_view(), name="home"),
    path("blog/", include("blog.urls")),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
