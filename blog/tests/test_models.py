from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from blog.models import BlogPost


class BlogPostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods"""
        # Create a test user
        test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # Create test blog post
        cls.blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            body='This is a test blog post content.',
            author=test_user
        )
    
    def test_title_max_length(self):
        """Test title field max length"""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        max_length = blog_post._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)
        
    def test_slug_max_length(self):
        """Test slug field max length"""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        max_length = blog_post._meta.get_field('slug').max_length
        self.assertEqual(max_length, 200)
    
    def test_slug_unique(self):
        """Test that slug field is unique"""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        unique = blog_post._meta.get_field('slug').unique
        self.assertTrue(unique)
    
    def test_auto_slug_generation(self):
        """Test that slug is auto-generated from title"""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        expected_slug = slugify(blog_post.title)
        self.assertEqual(blog_post.slug, expected_slug)
    
    def test_object_name_is_title(self):
        """Test that the blog post string representation is the title"""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        expected_object_name = blog_post.title
        self.assertEqual(str(blog_post), expected_object_name)
    
    def test_get_absolute_url(self):
        """Test get_absolute_url method"""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        expected_url = reverse('blog:post_detail', kwargs={'slug': blog_post.slug})
        self.assertEqual(blog_post.get_absolute_url(), expected_url)
    
    def test_ordering(self):
        """Test that blog posts are ordered by created_on in descending order"""
        # Create another blog post
        User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='anotherpassword'
        )
        
        another_post = BlogPost.objects.create(
            title='Another Test Blog Post',
            body='This is another test blog post content.',
            author=User.objects.get(username='anotheruser')
        )
        
        blog_posts = BlogPost.objects.all()
        self.assertEqual(blog_posts[0], another_post)  # newer post first
        self.assertEqual(blog_posts[1], self.blog_post)  # older post second
    
    def test_author_relationship(self):
        """Test the author ForeignKey relationship"""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        self.assertEqual(blog_post.author.username, 'testuser')
    
    def test_cascade_delete(self):
        """Test that blog posts are deleted when the author is deleted"""
        initial_count = BlogPost.objects.count()
        User.objects.get(username='testuser').delete()
        self.assertEqual(BlogPost.objects.count(), initial_count - 1)
        
    def test_created_updated_on_fields(self):
        """Test that created_on and updated_on are auto-populated"""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        self.assertIsNotNone(blog_post.created_on)
        self.assertIsNotNone(blog_post.updated_on)
        
    def test_update_changes_updated_on(self):
        """Test that updating a post changes updated_on but not created_on"""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        original_created_on = blog_post.created_on
        original_updated_on = blog_post.updated_on
        
        # Update the post
        blog_post.title = "Updated Test Blog Post"
        blog_post.save()
        
        # Refresh from database
        blog_post.refresh_from_db()
        
        # created_on should not change
        self.assertEqual(blog_post.created_on, original_created_on)
        
        # updated_on should change
        self.assertNotEqual(blog_post.updated_on, original_updated_on) 