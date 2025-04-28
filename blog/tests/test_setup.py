import pytest
from django.test import Client


@pytest.mark.django_db
def test_pytest_setup():
    """Test pytest kurulumunun doğru çalıştığını kontrol eder."""
    client = Client()
    response = client.get("/")
    assert response.status_code in [200, 302]  # Ana sayfa ya başarılı ya da yönlendirme döndürmeli
