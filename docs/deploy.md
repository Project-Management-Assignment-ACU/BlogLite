# BlogLite Dağıtım Kılavuzu (PythonAnywhere)

Bu kılavuz, BlogLite projesinin PythonAnywhere üzerinde nasıl dağıtılacağını adım adım açıklar.

## 1. PythonAnywhere Hesabı Oluşturma

1. [PythonAnywhere](https://www.pythonanywhere.com/) sitesine gidin
2. "Pricing & Signup" sayfasından ücretsiz hesap oluşturun
3. Hesabınızı doğrulayın ve giriş yapın

## 2. Kod Tabanını Yükleme

```bash
# PythonAnywhere Bash konsolunda:
git clone https://github.com/kullanici_adi/BlogLite.git
cd BlogLite
```

## 3. Sanal Ortam Oluşturma

```bash
mkvirtualenv --python=/usr/bin/python3.9 bloglite-env
pip install -r requirements.txt
```

## 4. Veritabanı Ayarları

```bash
cd BlogLite
python manage.py migrate
python manage.py createsuperuser
```

## 5. Web Uygulaması Yapılandırma

1. PythonAnywhere Dashboard'da "Web" sekmesine gidin
2. "Add a new web app" seçin
3. Manuel yapılandırma -> Python 3.9 seçin
4. Yapılandırma dosyasını şu şekilde düzenleyin:

```python
# /var/www/kullanici_adi_pythonanywhere_com_wsgi.py

import os
import sys

path = '/home/kullanici_adi/BlogLite'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 6. Statik Dosyaları Toplama

```bash
python manage.py collectstatic
```

## 7. PythonAnywhere Yapılandırması

Web sekmesinde aşağıdaki ayarları yapın:

### Virtualenv:
```
/home/kullanici_adi/.virtualenvs/bloglite-env
```

### Static files:
```
URL: /static/
Directory: /home/kullanici_adi/BlogLite/staticfiles
```

### WSGI configuration file:
```
/var/www/kullanici_adi_pythonanywhere_com_wsgi.py
```

## 8. Güvenlik Ayarları

`core/settings.py` dosyasında:

```python
DEBUG = False
ALLOWED_HOSTS = ['kullanici_adi.pythonanywhere.com']
```

## 9. E-posta Ayarları

PythonAnywhere'in SMTP sunucusunu kullanmak için:

```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
```

## 10. Son Adımlar

1. Web uygulamasını yeniden başlatın
2. Hata günlüklerini kontrol edin
3. Site bağlantısını test edin: `https://kullanici_adi.pythonanywhere.com`

## Sorun Giderme

### Sık Karşılaşılan Hatalar

1. **500 Internal Server Error**
   - Hata günlüklerini kontrol edin
   - DEBUG = True yaparak detaylı hata mesajını görün

2. **Statik Dosyalar Yüklenmiyor**
   - `collectstatic` komutunu tekrar çalıştırın
   - Statik dosya yollarını kontrol edin

3. **Veritabanı Hataları**
   - Migrationları kontrol edin
   - Veritabanı izinlerini kontrol edin

### Günlük Dosyaları

- Error log: `/var/log/kullanici_adi.pythonanywhere.com.error.log`
- Access log: `/var/log/kullanici_adi.pythonanywhere.com.access.log`
- Server log: `/var/log/kullanici_adi.pythonanywhere.com.server.log`

## Bakım

### Güncellemeler

```bash
cd BlogLite
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
```

### Yedekleme

1. Veritabanı yedekleme:
```bash
./scripts/backup.sh
```

2. Media dosyalarını yedekleme:
```bash
tar -czf media_backup.tar.gz media/
```

## Güvenlik Tavsiyeleri

1. Düzenli güvenlik güncellemelerini yapın
2. DEBUG modunu kapalı tutun
3. Güçlü şifreler kullanın
4. HTTPS kullanımını zorunlu kılın
5. Düzenli yedekleme alın
