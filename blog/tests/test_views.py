from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import BlogPost
from blog.forms import BlogPostForm


class BlogViewsTest(TestCase):
    def setUp(self):
        """Set up data for the test methods"""
        # Create two test users
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpassword1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword2'
        )
        
        # Create test blog posts
        self.post1 = BlogPost.objects.create(
            title='Test Blog Post 1',
            body='This is the first test blog post.',
            author=self.user1,
            slug='test-blog-post-1'
        )
        self.post2 = BlogPost.objects.create(
            title='Test Blog Post 2',
            body='This is the second test blog post.',
            author=self.user2,
            slug='test-blog-post-2'
        )


class BlogPostListViewTest(BlogViewsTest):
    def test_view_url_exists(self):
        """Test that the URL for the blog list view exists"""
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        """Test that the URL is accessible by name"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the correct template is used"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/list.html')
    
    def test_view_lists_all_posts(self):
        """Test that all posts are displayed"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 2)
    
    def test_pagination_is_five(self):
        """Test that pagination is set to 5 per page"""
        # Create 8 additional posts for a total of 10
        for i in range(8):
            BlogPost.objects.create(
                title=f'Test Blog Post {i+3}',
                body=f'This is test blog post {i+3}.',
                author=self.user1,
                slug=f'test-blog-post-{i+3}'
            )
        
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['posts']), 5)
    
    def test_search_filters_posts(self):
        """Test that search functionality filters posts correctly"""
        response = self.client.get(f"{reverse('blog:post_list')}?search=first")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['posts']), 1)
        self.assertEqual(response.context['posts'][0], self.post1)


class BlogPostDetailViewTest(BlogViewsTest):
    def test_view_url_exists(self):
        """Test that the URL for the blog detail view exists"""
        response = self.client.get(f'/blog/post/{self.post1.slug}/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        """Test that the URL is accessible by name"""
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the correct template is used"""
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')
    
    def test_view_displays_correct_post(self):
        """Test that the correct post is displayed"""
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.post1)
    
    def test_404_for_nonexistent_post(self):
        """Test that a 404 is returned for a nonexistent post"""
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'nonexistent-post'}))
        self.assertEqual(response.status_code, 404)


class BlogPostCreateViewTest(BlogViewsTest):
    def test_redirect_if_not_logged_in(self):
        """Test that unauthenticated users are redirected"""
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 302)  # Check it's a redirect
        self.assertTrue(response.url.startswith('/login/'))  # Check redirect destination starts with login URL
    
    def test_view_url_exists_at_desired_location(self):
        """Test that the URL for the blog create view exists"""
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get('/blog/post/new/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        """Test that the URL is accessible by name"""
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the correct template is used"""
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/form.html')
    
    def test_form_is_rendered(self):
        """Test that the form is rendered in the context"""
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], BlogPostForm)
    
    def test_post_creation(self):
        """Test creating a new post"""
        self.client.login(username='testuser1', password='testpassword1')
        post_count = BlogPost.objects.count()
        
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'New Test Post',
            'body': 'This is a new test post created from a test.'
        })
        
        # Check redirection after post creation
        self.assertEqual(BlogPost.objects.count(), post_count + 1)
        new_post = BlogPost.objects.latest('created_on')
        self.assertEqual(new_post.title, 'New Test Post')
        self.assertEqual(new_post.author, self.user1)
        self.assertRedirects(response, reverse('blog:post_detail', kwargs={'slug': new_post.slug}))


class BlogPostUpdateViewTest(BlogViewsTest):
    def test_redirect_if_not_logged_in(self):
        """Test that unauthenticated users are redirected"""
        response = self.client.get(reverse('blog:post_update', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 302)  # Check it's a redirect
        self.assertTrue(response.url.startswith('/login/'))  # Check redirect destination starts with login URL
    
    def test_forbidden_if_not_author(self):
        """Test that non-authors are redirected with access denied"""
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(reverse('blog:post_update', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 302)  # Should redirect to blog list with error message
        self.assertEqual(response.url, reverse('blog:post_list'))  # Should redirect to blog list
    
    def test_view_url_accessible_by_name(self):
        """Test that the URL is accessible by name for the author"""
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('blog:post_update', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the correct template is used"""
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('blog:post_update', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/form.html')
    
    def test_form_is_rendered_with_post_data(self):
        """Test that the form is rendered with the post data"""
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('blog:post_update', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], BlogPostForm)
        self.assertEqual(response.context['form'].instance, self.post1)
    
    def test_post_update(self):
        """Test updating a post"""
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.post(reverse('blog:post_update', kwargs={'slug': self.post1.slug}), {
            'title': 'Updated Test Post 1',
            'body': 'This is the updated content for the first test blog post.'
        })
        
        # Refresh the post from the database
        self.post1.refresh_from_db()
        
        # Check that the post was updated and redirects to detail view
        self.assertEqual(self.post1.title, 'Updated Test Post 1')
        self.assertEqual(self.post1.body, 'This is the updated content for the first test blog post.')
        self.assertRedirects(response, reverse('blog:post_detail', kwargs={'slug': self.post1.slug}))


class BlogPostDeleteViewTest(BlogViewsTest):
    def test_redirect_if_not_logged_in(self):
        """Test that unauthenticated users are redirected"""
        response = self.client.get(reverse('blog:post_delete', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 302)  # Check it's a redirect
        self.assertTrue(response.url.startswith('/login/'))  # Check redirect destination starts with login URL
    
    def test_forbidden_if_not_author(self):
        """Test that non-authors are redirected with access denied"""
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(reverse('blog:post_delete', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 302)  # Should redirect to blog list with error message
        self.assertEqual(response.url, reverse('blog:post_list'))  # Should redirect to blog list
    
    def test_view_url_accessible_by_name(self):
        """Test that the URL is accessible by name for the author"""
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('blog:post_delete', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        """Test that the correct template is used"""
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('blog:post_delete', kwargs={'slug': self.post1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/confirm_delete.html')
    
    def test_post_deletion(self):
        """Test deleting a post"""
        self.client.login(username='testuser1', password='testpassword1')
        post_count = BlogPost.objects.count()
        
        response = self.client.post(reverse('blog:post_delete', kwargs={'slug': self.post1.slug}))
        
        # Check that the post was deleted and the user is redirected to the blog list
        self.assertEqual(BlogPost.objects.count(), post_count - 1)
        self.assertFalse(BlogPost.objects.filter(slug=self.post1.slug).exists())
        self.assertRedirects(response, reverse('blog:post_list')) 