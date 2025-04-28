"""Blog uygulaması için view sınıflarını içerir.

Bu modül, blog gönderilerinin listelenmesi, görüntülenmesi, oluşturulması,
düzenlenmesi ve silinmesi için gerekli view sınıflarını içerir.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import BlogPostForm
from .models import BlogPost


class BlogPostListView(ListView):
    """Blog gönderilerinin listelendiği view.

    Bu view, blog gönderilerini sayfalama, arama ve sıralama özellikleriyle birlikte listeler.
    """

    model = BlogPost
    template_name = "blog/list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        """Oluşturulma tarihine göre sıralanmış ve filtrelenmiş gönderileri döndürür."""
        queryset = super().get_queryset()

        # Apply search filter if provided
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(title__icontains=search_query) | queryset.filter(
                body__icontains=search_query
            )

        # Apply ordering if provided, otherwise use default ordering
        ordering = self.request.GET.get("order", "-created_on")
        valid_ordering_fields = ["created_on", "-created_on", "title", "-title"]
        if ordering in valid_ordering_fields:
            queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, **kwargs):
        """Sayfalama kontrolleri için ek context verilerini ekler."""
        context = super().get_context_data(**kwargs)

        # Add search query to context for form
        context["search_query"] = self.request.GET.get("search", "")

        # Add current ordering to context
        context["current_ordering"] = self.request.GET.get("order", "-created_on")

        # Add page size options
        context["page_sizes"] = [5, 10, 25, 50]
        context["current_page_size"] = int(self.request.GET.get("page_size", self.paginate_by))

        # Preserve query parameters in pagination links
        query_params = self.request.GET.copy()
        if "page" in query_params:
            del query_params["page"]
        context["query_params"] = query_params.urlencode()

        return context

    def get_paginate_by(self, queryset):
        """Kullanıcının sayfa başına gönderi sayısını özelleştirmesine izin verir."""
        page_size = self.request.GET.get("page_size", self.paginate_by)
        return page_size


class BlogPostDetailView(DetailView):
    """Blog gönderilerinin detay sayfasını gösteren view."""

    model = BlogPost
    template_name = "blog/detail.html"
    context_object_name = "post"
    slug_url_kwarg = "slug"


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """Yeni blog gönderisi oluşturma view'ı.

    Kullanıcının giriş yapmış olmasını gerektirir.
    Mevcut kullanıcıyı otomatik olarak yazar olarak atar.
    """

    model = BlogPost
    template_name = "blog/form.html"
    form_class = BlogPostForm
    login_url = "/login/"  # Where to redirect if user is not logged in

    def get_context_data(self, **kwargs):
        """Form şablonu için başlık ve buton metni ekler."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Create a New Blog Post"
        context["button_text"] = "Create Post"
        return context

    def form_valid(self, form):
        """Form geçerliyse yazarı atar ve başarı mesajı gösterir."""
        # Set the author to current user
        form.instance.author = self.request.user

        # Save the form
        response = super().form_valid(form)

        # Add a success message
        messages.success(
            self.request, f'Your blog post "{form.instance.title}" has been created successfully!'
        )

        return response

    def form_invalid(self, form):
        """Form geçersizse hata mesajı gösterir."""
        messages.error(
            self.request,
            "There was an error with your submission. Please check the form and try again.",
        )
        return super().form_invalid(form)


class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Mevcut blog gönderisini düzenleme view'ı.

    Kullanıcının giriş yapmış olmasını ve gönderinin yazarı olmasını gerektirir.
    """

    model = BlogPost
    template_name = "blog/form.html"
    form_class = BlogPostForm
    slug_url_kwarg = "slug"
    login_url = "/login/"

    def test_func(self):
        """Mevcut kullanıcının gönderinin yazarı olup olmadığını kontrol eder."""
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        """Form şablonu için başlık ve buton metni ekler."""
        context = super().get_context_data(**kwargs)
        context["title"] = f"Edit Blog Post: {self.get_object().title}"
        context["button_text"] = "Update Post"
        return context

    def form_valid(self, form):
        """Form geçerliyse başarı mesajı gösterir."""
        response = super().form_valid(form)
        messages.success(
            self.request, f'The blog post "{form.instance.title}" has been updated successfully!'
        )
        return response

    def form_invalid(self, form):
        """Form geçersizse hata mesajı gösterir."""
        messages.error(
            self.request,
            "There was an error updating your post. Please check the form and try again.",
        )
        return super().form_invalid(form)

    def handle_no_permission(self):
        """Kullanıcı yazar değilse özel hata mesajı gösterir."""
        if self.request.user.is_authenticated:
            messages.error(self.request, "You don't have permission to edit this post.")
            return HttpResponseRedirect(reverse_lazy("blog:post_list"))
        return super().handle_no_permission()


class BlogPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Blog gönderisi silme view'ı.

    Kullanıcının giriş yapmış olmasını ve gönderinin yazarı olmasını gerektirir.
    """

    model = BlogPost
    template_name = "blog/confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
    slug_url_kwarg = "slug"
    login_url = "/login/"

    def test_func(self):
        """Mevcut kullanıcının gönderinin yazarı olup olmadığını kontrol eder."""
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        """Gönderiyi siler ve başarı mesajı gösterir."""
        post = self.get_object()
        messages.success(
            self.request, f'The blog post "{post.title}" has been deleted successfully!'
        )
        return super().delete(request, *args, **kwargs)

    def handle_no_permission(self):
        """Kullanıcı yazar değilse özel hata mesajı gösterir."""
        if self.request.user.is_authenticated:
            messages.error(self.request, "You don't have permission to delete this post.")
            return HttpResponseRedirect(reverse_lazy("blog:post_list"))
        return super().handle_no_permission()
