# Hızlı Başlangıç Kılavuzu

Bu kılavuz, projeyi hızlıca çalıştırmak için gerekli adımları içerir.

## Adım 1: Gereksinimleri Yükleyin

```bash
# Python 3.7+ yüklü olduğundan emin olun
python3 --version

# Gerekli paketleri yükleyin
pip install -r requirements.txt
```

## Adım 2: Veritabanlarını Hazırlayın

### MySQL/MSSQL
- Veritabanı sunucusunun çalıştığından emin olun
- Bağlantı bilgilerinizi hazırlayın (host, port, database, username, password)

### MongoDB
- MongoDB sunucusunun çalıştığından emin olun
- Bağlantı bilgilerinizi hazırlayın (host, port, database)

## Adım 3: Konfigürasyonu Düzenleyin

`config.yaml` dosyasını açın ve aşağıdaki bilgileri doldurun:

```yaml
sql_database:
  type: "mysql"  # veya "mssql"
  host: "localhost"
  port: 3306
  database: "your_database_name"
  username: "your_username"
  password: "your_password"

mongodb:
  host: "localhost"
  port: 27017
  database: "migrated_database"
```

## Adım 4: Uygulamayı Çalıştırın

```bash
python main.py
```

## Adım 5: Sonuçları Kontrol Edin

- **Loglar**: `logs/migration.log` dosyasında
- **Rapor**: `reports/` dizininde oluşturulan markdown dosyası

## Örnek Çıktı

```
============================================================
SQL → MongoDB Migration Tool
============================================================

2024-01-01 10:00:00 - INFO - Migration uygulaması başlatılıyor...
2024-01-01 10:00:01 - INFO - MySQL veritabanına başarıyla bağlanıldı
2024-01-01 10:00:02 - INFO - Veritabanı şeması keşfediliyor...
2024-01-01 10:00:03 - INFO - 5 tablo bulundu
2024-01-01 10:00:04 - INFO - MongoDB'ye başarıyla bağlanıldı
2024-01-01 10:00:05 - INFO - Veri aktarımı başlatılıyor...
2024-01-01 10:00:10 - INFO - Veri aktarımı tamamlandı. 5 tablo, 1000 belge aktarıldı.
2024-01-01 10:00:11 - INFO - Teknik rapor oluşturuluyor...
2024-01-01 10:00:12 - INFO - Rapor oluşturuldu: reports/migration_report_20240101_100012.md

============================================================
MIGRATION TAMAMLANDI
============================================================
Aktarılan Tablo Sayısı: 5
Aktarılan Belge Sayısı: 1000
Hata Sayısı: 0
Rapor: reports/migration_report_20240101_100012.md
============================================================
```

## Sorun Giderme

### "ModuleNotFoundError" Hatası
```bash
# Gerekli paketlerin yüklü olduğundan emin olun
pip install -r requirements.txt
```

### "Connection refused" Hatası
- Veritabanı sunucularının çalıştığından emin olun
- Port numaralarını kontrol edin
- Firewall ayarlarını kontrol edin

### "Authentication failed" Hatası
- Kullanıcı adı ve şifrenin doğru olduğundan emin olun
- Kullanıcının gerekli yetkilere sahip olduğundan emin olun

## İleri Seviye Kullanım

### Sadece Şema Keşfi
Şema keşfi yapmak için `example_usage.py` dosyasındaki örnekleri inceleyin.

### Özel Migration Ayarları
`config.yaml` dosyasında migration ayarlarını özelleştirebilirsiniz:

```yaml
migration:
  batch_size: 500        # Batch boyutu
  drop_existing: true   # Mevcut collection'ları sil
  preserve_ids: true    # Primary key'leri _id olarak kullan
```

## Daha Fazla Bilgi

- Detaylı dokümantasyon: `README.md`
- Proje yapısı: `PROJECT_STRUCTURE.md`
- Uygulama notları: `IMPLEMENTATION_NOTES.md`

