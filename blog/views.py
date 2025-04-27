from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """Return posts ordered by created date with optional filtering"""
        queryset = super().get_queryset()
        
        # Apply search filter if provided
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query) | queryset.filter(body__icontains=search_query)
        
        # Apply ordering if provided, otherwise use default ordering
        ordering = self.request.GET.get('order', '-created_on')
        valid_ordering_fields = ['created_on', '-created_on', 'title', '-title']
        if ordering in valid_ordering_fields:
            queryset = queryset.order_by(ordering)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add additional context for pagination controls"""
        context = super().get_context_data(**kwargs)
        
        # Add search query to context for form
        context['search_query'] = self.request.GET.get('search', '')
        
        # Add current ordering to context
        context['current_ordering'] = self.request.GET.get('order', '-created_on')
        
        # Add page size options
        context['page_sizes'] = [5, 10, 25, 50]
        context['current_page_size'] = int(self.request.GET.get('page_size', self.paginate_by))
        
        # Preserve query parameters in pagination links
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['query_params'] = query_params.urlencode()
        
        return context
    
    def get_paginate_by(self, queryset):
        """Allow user to customize page size"""
        page_size = self.request.GET.get('page_size', self.paginate_by)
        return page_size


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog/form.html'
    form_class = BlogPostForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    template_name = 'blog/form.html'
    form_class = BlogPostForm
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
