import pytest
from django.urls import reverse


def test_core_urls_exist():
    """Test core URL'lerinin varlığını kontrol eder."""
    urls = ["core:home", "login", "register"]
    for url_name in urls:
        try:
            reverse(url_name)
        except Exception as e:
            pytest.fail(f"{url_name} URL'si bulunamadı: {str(e)}")
