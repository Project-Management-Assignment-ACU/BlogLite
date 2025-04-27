from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 5


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog/form.html'
    fields = ['title', 'body']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    template_name = 'blog/form.html'
    fields = ['title', 'body']
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Only allow users to edit their own posts
        return BlogPost.objects.filter(author=self.request.user)


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        # Only allow users to delete their own posts
        return BlogPost.objects.filter(author=self.request.user)
