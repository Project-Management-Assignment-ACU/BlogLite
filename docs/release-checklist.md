# BlogLite Yayın Öncesi Kontrol Listesi

## 1. Kod Kalitesi ve Test

- [ ] Tüm testler başarıyla geçiyor (`pytest`)
- [ ] Test coverage %80'in üzerinde
- [ ] Kod formatlaması kontrol edildi (`black`)
- [ ] Kod kalitesi kontrol edildi (`flake8`)
- [ ] Import sıralaması kontrol edildi (`isort`)
- [ ] Tüm docstring'ler güncel ve doğru
- [ ] Kullanılmayan importlar ve kod blokları temizlendi
- [ ] Pre-commit hook'lar başarıyla çalışıyor

## 2. Güvenlik Kontrolleri

- [ ] `DEBUG = False` ayarlandı
- [ ] Gizli anahtarlar ve hassas bilgiler environment variable'lara taşındı
- [ ] `ALLOWED_HOSTS` doğru yapılandırıldı
- [ ] HTTPS zorunlu kılındı
- [ ] Admin paneli URL'i özelleştirildi
- [ ] Veritabanı yedekleme betiği test edildi
- [ ] Güvenlik duvarı kuralları kontrol edildi
- [ ] Tüm paketler güncel ve güvenlik açığı içermiyor

## 3. Performans

- [ ] Statik dosyalar optimize edildi (resimler, CSS, JS)
- [ ] Veritabanı indeksleri kontrol edildi
- [ ] Sayfalama (pagination) doğru çalışıyor
- [ ] Cache mekanizması aktif ve çalışıyor
- [ ] Debug toolbar kaldırıldı
- [ ] Gereksiz middleware'ler devre dışı bırakıldı
- [ ] Database query optimizasyonları yapıldı

## 4. Kullanıcı Deneyimi

- [ ] Tüm formlar doğru çalışıyor
- [ ] Hata mesajları anlaşılır ve yardımcı
- [ ] 404 ve 500 hata sayfaları özelleştirildi
- [ ] Responsive tasarım tüm cihazlarda test edildi
- [ ] Sayfa yükleme süreleri kabul edilebilir seviyede
- [ ] Tüm bağlantılar çalışıyor
- [ ] Kullanıcı geri bildirimleri değerlendirildi

## 5. İçerik ve SEO

- [ ] Tüm metinler yazım hataları için kontrol edildi
- [ ] Meta etiketleri doğru yapılandırıldı
- [ ] robots.txt ve sitemap.xml güncel
- [ ] Sosyal medya meta etiketleri eklendi
- [ ] Alt metinler ve başlıklar SEO uyumlu
- [ ] İçerik hiyerarşisi mantıklı

## 6. Dağıtım Hazırlıkları

- [ ] requirements.txt güncel
- [ ] Veritabanı migrasyonları temiz
- [ ] Environment variables dokümante edildi
- [ ] Statik dosyalar toplandı (`collectstatic`)
- [ ] WSGI/ASGI yapılandırması test edildi
- [ ] Dağıtım kılavuzu güncel
- [ ] Yedekleme stratejisi dokümante edildi

## 7. Dokümantasyon

- [ ] README.md güncel
- [ ] API dokümantasyonu (varsa) güncel
- [ ] Kurulum kılavuzu test edildi
- [ ] Değişiklik günlüğü (CHANGELOG) güncellendi
- [ ] Katkıda bulunma kılavuzu (CONTRIBUTING) güncel
- [ ] Lisans dosyası mevcut

## 8. Son Kontroller

- [ ] Git dalları temiz ve güncel
- [ ] Tüm çakışmalar çözüldü
- [ ] Sürüm numarası güncellendi
- [ ] Release notes hazırlandı
- [ ] Deployment test ortamında denendi
- [ ] Rollback planı hazır
- [ ] Ekip üyeleri bilgilendirildi

## Onay

**Proje Lideri:** _________________
**Tarih:** _________________

## Notlar

- Bu kontrol listesi her yeni sürüm öncesinde doldurulmalıdır
- Eksik maddeler varsa, yayın ertelenmelidir
- Kontrol listesi proje ihtiyaçlarına göre güncellenebilir
