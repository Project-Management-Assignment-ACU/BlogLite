"""Blog uygulaması için URL yapılandırmalarını içerir."""

from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.BlogPostListView.as_view(), name="post_list"),
    path("post/new/", views.BlogPostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/", views.BlogPostDetailView.as_view(), name="post_detail"),
    path("post/<slug:slug>/edit/", views.BlogPostUpdateView.as_view(), name="post_update"),
    path("post/<slug:slug>/delete/", views.BlogPostDeleteView.as_view(), name="post_delete"),
]
