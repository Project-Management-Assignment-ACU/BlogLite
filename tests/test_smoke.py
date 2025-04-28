import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import BlogPost
from django.core import mail
from core.forms import ContactForm

@pytest.mark.django_db
class TestSmokeTests:
    """Uygulamanın temel işlevselliğini kontrol eden smoke testler."""
    
    @pytest.fixture
    def test_user(self):
        """Test kullanıcısı oluşturur."""
        return User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    @pytest.fixture
    def test_post(self, test_user):
        """Test blog gönderisi oluşturur."""
        return BlogPost.objects.create(
            title='Test Post',
            body='Test Content',
            author=test_user
        )

    def test_home_page_loads(self, client):
        """Ana sayfa yükleniyor mu?"""
        response = client.get(reverse('core:home'))
        assert response.status_code == 200
    
    def test_about_page_loads(self, client):
        """Hakkında sayfası yükleniyor mu?"""
        response = client.get(reverse('core:about'))
        assert response.status_code == 200

    def test_contact_form_submission(self, client):
        """İletişim formu çalışıyor mu?"""
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        }
        response = client.post(reverse('core:contact'), form_data)
        assert response.status_code in [200, 302]
        assert len(mail.outbox) == 1  # E-posta gönderildi mi?

    def test_blog_list_page_loads(self, client):
        """Blog listesi sayfası yükleniyor mu?"""
        response = client.get(reverse('blog:post_list'))
        assert response.status_code == 200

    def test_user_registration(self, client):
        """Kullanıcı kaydı çalışıyor mu?"""
        form_data = {
            'username': 'newuser',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
            'email': 'newuser@example.com'
        }
        response = client.post(reverse('register'), form_data)
        assert response.status_code in [200, 302]
        assert User.objects.filter(username='newuser').exists()

    def test_user_login(self, client, test_user):
        """Kullanıcı girişi çalışıyor mu?"""
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        assert response.status_code in [200, 302]
        
    def test_blog_post_creation(self, client, test_user):
        """Blog gönderisi oluşturma çalışıyor mu?"""
        client.force_login(test_user)
        form_data = {
            'title': 'New Test Post',
            'body': 'This is a test content that is long enough to pass validation.'  # En az 20 karakter
        }
        response = client.post(reverse('blog:post_create'), form_data)
        assert response.status_code in [200, 302]
        assert BlogPost.objects.filter(title='New Test Post').exists()

    def test_blog_post_detail(self, client, test_post):
        """Blog gönderisi detay sayfası yükleniyor mu?"""
        response = client.get(test_post.get_absolute_url())
        assert response.status_code == 200
        assert test_post.title in str(response.content) 