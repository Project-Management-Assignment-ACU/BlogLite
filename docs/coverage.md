# Test Coverage Raporu

Bu dokümantasyon, BlogLite projesinin test coverage raporlarının nasıl oluşturulacağını ve yorumlanacağını açıklar.

## Coverage Raporu Oluşturma

Coverage raporu oluşturmak için aşağıdaki komutu çalıştırın:

```bash
pytest
```

Bu komut, `pytest.ini` dosyasındaki yapılandırma sayesinde otomatik olarak HTML formatında bir coverage raporu oluşturacaktır.

## Raporun Konumu

Coverage raporu `htmlcov/` dizininde oluşturulur. Raporu görüntülemek için:

1. `htmlcov/index.html` dosyasını web tarayıcınızda açın
2. İnteraktif raporda her bir Python dosyası için detaylı coverage bilgilerini görebilirsiniz

## Raporu Yorumlama

Coverage raporu şu bilgileri içerir:

- **Statements**: Test edilen kod satırlarının yüzdesi
- **Missing**: Test edilmemiş kod satırları
- **Excluded**: Coverage hesaplamasından çıkarılan satırlar
- **Branches**: If/else dallanmalarının test kapsamı

## Hedefler

Projemiz için coverage hedefleri:

- Genel coverage: En az %80
- Views: En az %90
- Models: %100
- Forms: En az %90

## Coverage'ı İyileştirme

Coverage'ı artırmak için:

1. Missing satırları belirleyin
2. Eksik test senaryolarını yazın
3. Edge case'leri test edin
4. Branch coverage'a özellikle dikkat edin

## Notlar

- `--no-cov-on-fail` seçeneği sayesinde, testler başarısız olduğunda coverage raporu oluşturulmaz
- Coverage raporları `.gitignore` dosyasına eklenmiştir
- Her PR öncesi coverage raporunu kontrol edin
