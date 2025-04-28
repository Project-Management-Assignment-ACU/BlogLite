"""Blog uygulamasının view testlerini içerir."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from blog.forms import BlogPostForm
from blog.models import BlogPost


class BlogViewsTest(TestCase):
    """Blog view'ları için temel test sınıfı."""

    def setUp(self):
        """Test metodları için gerekli verileri oluşturur."""
        # Create two test users
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="testuser1", email="test1@example.com", password="testpassword1"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", email="test2@example.com", password="testpassword2"
        )

        # Create test blog posts
        self.post1 = BlogPost.objects.create(
            title="Test Blog Post 1",
            body="This is the first test blog post.",
            author=self.user1,
            slug="test-blog-post-1",
        )
        self.post2 = BlogPost.objects.create(
            title="Test Blog Post 2",
            body="This is the second test blog post.",
            author=self.user2,
            slug="test-blog-post-2",
        )


class BlogPostListViewTest(BlogViewsTest):
    """Blog gönderilerinin listelendiği view için test sınıfı."""

    def test_view_url_exists(self):
        """Doğrular ki blog listesi URL'si var."""
        response = self.client.get("/blog/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """URL'nin isim ile erişilebilir olduğunu test eder."""
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Doğru şablonun kullanıldığını test eder."""
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/list.html")

    def test_view_lists_all_posts(self):
        """Tüm gönderilerin listelendiğini test eder."""
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 2)

    def test_pagination_is_five(self):
        """Sayfalandırmanın sayfa başına 5 gönderi olduğunu test eder."""
        # Create 8 additional posts for a total of 10
        for i in range(8):
            BlogPost.objects.create(
                title=f"Test Blog Post {i+3}",
                body=f"This is test blog post {i+3}.",
                author=self.user1,
                slug=f"test-blog-post-{i+3}",
            )

        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["posts"]), 5)

    def test_search_filters_posts(self):
        """Arama işlevinin gönderileri doğru filtrelediğini test eder."""
        response = self.client.get(f"{reverse('blog:post_list')}?search=first")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 1)
        self.assertEqual(response.context["posts"][0], self.post1)


class BlogPostDetailViewTest(BlogViewsTest):
    """Blog gönderilerinin detay sayfası için test sınıfı."""

    def test_view_url_exists(self):
        """Blog detay sayfası URL'sinin var olduğunu test eder."""
        response = self.client.get(f"/blog/post/{self.post1.slug}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """URL'nin isim ile erişilebilir olduğunu test eder."""
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.post1.slug}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Doğru şablonun kullanıldığını test eder."""
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.post1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/detail.html")

    def test_view_displays_correct_post(self):
        """Doğrular ki doğru gönderi görüntüleniyor."""
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": self.post1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["post"], self.post1)

    def test_404_for_nonexistent_post(self):
        """Var olmayan gönderi için 404 döndürüldüğünü test eder."""
        response = self.client.get(reverse("blog:post_detail", kwargs={"slug": "nonexistent-post"}))
        self.assertEqual(response.status_code, 404)


class BlogPostCreateViewTest(BlogViewsTest):
    """Blog gönderisi oluşturma view'ı için test sınıfı."""

    def test_redirect_if_not_logged_in(self):
        """Giriş yapmamış kullanıcıların yönlendirildiğini test eder."""
        response = self.client.get(reverse("blog:post_create"))
        self.assertEqual(response.status_code, 302)  # Check it's a redirect
        self.assertTrue(
            response.url.startswith("/login/")
        )  # Check redirect destination starts with login URL

    def test_view_url_exists_at_desired_location(self):
        """Blog oluşturma URL'sinin var olduğunu test eder."""
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.get("/blog/post/new/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """URL'nin isim ile erişilebilir olduğunu test eder."""
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.get(reverse("blog:post_create"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Doğru şablonun kullanıldığını test eder."""
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.get(reverse("blog:post_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/form.html")

    def test_form_is_rendered(self):
        """Formun context'te olduğunu test eder."""
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.get(reverse("blog:post_create"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], BlogPostForm)

    def test_post_creation(self):
        """Yeni gönderi oluşturmayı test eder."""
        self.client.login(username="testuser1", password="testpassword1")
        post_count = BlogPost.objects.count()

        response = self.client.post(
            reverse("blog:post_create"),
            {"title": "New Test Post", "body": "This is a new test post created from a test."},
        )

        # Check redirection after post creation
        self.assertEqual(BlogPost.objects.count(), post_count + 1)
        new_post = BlogPost.objects.latest("created_on")
        self.assertEqual(new_post.title, "New Test Post")
        self.assertEqual(new_post.author, self.user1)
        self.assertRedirects(response, reverse("blog:post_detail", kwargs={"slug": new_post.slug}))


class BlogPostUpdateViewTest(BlogViewsTest):
    """Blog gönderisi güncelleme view'ı için test sınıfı."""

    def test_redirect_if_not_logged_in(self):
        """Giriş yapmamış kullanıcıların yönlendirildiğini test eder."""
        response = self.client.get(reverse("blog:post_update", kwargs={"slug": self.post1.slug}))
        self.assertEqual(response.status_code, 302)  # Check it's a redirect
        self.assertTrue(
            response.url.startswith("/login/")
        )  # Check redirect destination starts with login URL

    def test_forbidden_if_not_author(self):
        """Yazar olmayan kullanıcıların erişiminin engellendiğini test eder."""
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.get(reverse("blog:post_update", kwargs={"slug": self.post1.slug}))
        self.assertEqual(
            response.status_code, 302
        )  # Should redirect to blog list with error message
        self.assertEqual(response.url, reverse("blog:post_list"))  # Should redirect to blog list

    def test_view_url_accessible_by_name(self):
        """URL'nin yazar için isim ile erişilebilir olduğunu test eder."""
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.get(reverse("blog:post_update", kwargs={"slug": self.post1.slug}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Doğru şablonun kullanıldığını test eder."""
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.get(reverse("blog:post_update", kwargs={"slug": self.post1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/form.html")

    def test_form_is_rendered_with_post_data(self):
        """Doğrular ki form gönderi verileriyle doldurulmuş."""
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.get(reverse("blog:post_update", kwargs={"slug": self.post1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], BlogPostForm)
        self.assertEqual(response.context["form"].instance, self.post1)

    def test_post_update(self):
        """Doğrular ki gönderi güncelleme çalışıyor."""
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.post(
            reverse("blog:post_update", kwargs={"slug": self.post1.slug}),
            {
                "title": "Updated Test Post 1",
                "body": "This is the updated content for the first test blog post.",
            },
        )

        # Refresh the post from the database
        self.post1.refresh_from_db()

        # Check that the post was updated and redirects to detail view
        self.assertEqual(self.post1.title, "Updated Test Post 1")
        self.assertEqual(
            self.post1.body, "This is the updated content for the first test blog post."
        )
        self.assertRedirects(
            response, reverse("blog:post_detail", kwargs={"slug": self.post1.slug})
        )


class BlogPostDeleteViewTest(BlogViewsTest):
    """Blog gönderisi silme view'ı için test sınıfı."""

    def test_redirect_if_not_logged_in(self):
        """Giriş yapmamış kullanıcıların yönlendirildiğini test eder."""
        response = self.client.get(reverse("blog:post_delete", kwargs={"slug": self.post1.slug}))
        self.assertEqual(response.status_code, 302)  # Check it's a redirect
        self.assertTrue(
            response.url.startswith("/login/")
        )  # Check redirect destination starts with login URL

    def test_forbidden_if_not_author(self):
        """Yazar olmayan kullanıcıların erişiminin engellendiğini test eder."""
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.get(reverse("blog:post_delete", kwargs={"slug": self.post1.slug}))
        self.assertEqual(
            response.status_code, 302
        )  # Should redirect to blog list with error message
        self.assertEqual(response.url, reverse("blog:post_list"))  # Should redirect to blog list

    def test_view_url_accessible_by_name(self):
        """URL'nin yazar için isim ile erişilebilir olduğunu test eder."""
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.get(reverse("blog:post_delete", kwargs={"slug": self.post1.slug}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Doğru şablonun kullanıldığını test eder."""
        self.client.login(username="testuser1", password="testpassword1")
        response = self.client.get(reverse("blog:post_delete", kwargs={"slug": self.post1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/confirm_delete.html")

    def test_post_deletion(self):
        """Doğrular ki gönderi silme çalışıyor."""
        self.client.login(username="testuser1", password="testpassword1")
        post_count = BlogPost.objects.count()

        response = self.client.post(reverse("blog:post_delete", kwargs={"slug": self.post1.slug}))

        # Check that the post was deleted and the user is redirected to the blog list
        self.assertEqual(BlogPost.objects.count(), post_count - 1)
        self.assertFalse(BlogPost.objects.filter(slug=self.post1.slug).exists())
        self.assertRedirects(response, reverse("blog:post_list"))
