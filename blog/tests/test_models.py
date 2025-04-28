"""Blog uygulamasının model testlerini içerir."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from blog.models import BlogPost


class BlogPostModelTest(TestCase):
    """BlogPost modeli için test sınıfı."""

    @classmethod
    def setUpTestData(cls):
        """Test metodları tarafından kullanılacak test verilerini oluşturur."""
        # Create a test user
        test_user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

        # Create test blog post
        cls.blog_post = BlogPost.objects.create(
            title="Test Blog Post", body="This is a test blog post content.", author=test_user
        )

    def test_title_max_length(self):
        """Başlık alanının maksimum uzunluğunu test eder."""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        max_length = blog_post._meta.get_field("title").max_length
        self.assertEqual(max_length, 200)

    def test_slug_max_length(self):
        """Slug alanının maksimum uzunluğunu test eder."""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        max_length = blog_post._meta.get_field("slug").max_length
        self.assertEqual(max_length, 200)

    def test_slug_unique(self):
        """Slug alanının benzersiz olduğunu test eder."""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        unique = blog_post._meta.get_field("slug").unique
        self.assertTrue(unique)

    def test_auto_slug_generation(self):
        """Slug'ın başlıktan otomatik olarak oluşturulduğunu test eder."""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        expected_slug = slugify(blog_post.title)
        self.assertEqual(blog_post.slug, expected_slug)

    def test_object_name_is_title(self):
        """Blog gönderisinin string temsilinin başlık olduğunu test eder."""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        expected_object_name = blog_post.title
        self.assertEqual(str(blog_post), expected_object_name)

    def test_get_absolute_url(self):
        """get_absolute_url metodunun doğru URL'yi döndürdüğünü test eder."""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        expected_url = reverse("blog:post_detail", kwargs={"slug": blog_post.slug})
        self.assertEqual(blog_post.get_absolute_url(), expected_url)

    def test_ordering(self):
        """Blog gönderilerinin oluşturulma tarihine göre azalan sırada olduğunu test eder."""
        # Create another blog post
        User.objects.create_user(
            username="anotheruser", email="another@example.com", password="anotherpassword"
        )

        another_post = BlogPost.objects.create(
            title="Another Test Blog Post",
            body="This is another test blog post content.",
            author=User.objects.get(username="anotheruser"),
        )

        blog_posts = BlogPost.objects.all()
        self.assertEqual(blog_posts[0], another_post)  # newer post first
        self.assertEqual(blog_posts[1], self.blog_post)  # older post second

    def test_author_relationship(self):
        """Yazar ForeignKey ilişkisini test eder."""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        self.assertEqual(blog_post.author.username, "testuser")

    def test_cascade_delete(self):
        """Yazar silindiğinde blog gönderilerinin de silindiğini test eder."""
        initial_count = BlogPost.objects.count()
        User.objects.get(username="testuser").delete()
        self.assertEqual(BlogPost.objects.count(), initial_count - 1)

    def test_created_updated_on_fields(self):
        """created_on ve updated_on alanlarının otomatik doldurulduğunu test eder."""
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        self.assertIsNotNone(blog_post.created_on)
        self.assertIsNotNone(blog_post.updated_on)

    def test_update_changes_updated_on(self):
        """Güncellemenin updated_on alanını değiştirdiğini ama created_on alanını değiştirmediğini test eder."""
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
