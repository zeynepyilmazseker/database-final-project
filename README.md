# Database Migration Tool: SQL to MongoDB

Bu proje, MySQL veya MSSQL veritabanlarından MongoDB'ye otomatik veri ve şema aktarımı yapan bir araçtır.

## Özellikler

- ✅ MySQL ve MSSQL veritabanlarına bağlanma
- ✅ Dinamik şema keşfi (tables, columns, indexes, constraints, triggers, stored procedures)
- ✅ Otomatik MongoDB'ye veri aktarımı
- ✅ İdempotent çalışma (tekrar çalıştırılabilir)
- ✅ Detaylı hata loglama
- ✅ Teknik rapor oluşturma

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

1. `config.yaml` dosyasını düzenleyin
2. Uygulamayı çalıştırın:

```bash
python main.py
```

## Yapı

```
database-final-project/
├── main.py                 # Ana uygulama
├── src/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── sql_connector.py    # SQL veritabanı bağlantısı
│   │   ├── schema_discovery.py  # Şema keşif modülü
│   │   └── mongodb_connector.py # MongoDB bağlantısı
│   ├── migration/
│   │   ├── __init__.py
│   │   └── migrator.py          # Veri aktarım modülü
│   └── reporting/
│       ├── __init__.py
│       └── report_generator.py  # Rapor oluşturucu
├── config.yaml            # Konfigürasyon dosyası
├── logs/                  # Log dosyaları
└── reports/               # Oluşturulan raporlar
```

## Konfigürasyon

`config.yaml` dosyasında aşağıdaki bilgileri doldurun:

- SQL veritabanı bağlantı bilgileri
- MongoDB bağlantı bilgileri
- Log seviyesi ve rapor ayarları

## Proje Yapısı

Detaylı proje yapısı için `PROJECT_STRUCTURE.md` dosyasına bakın.

## Özellikler Detayı

### Şema Keşfi
- Otomatik tablo keşfi
- Kolon ve veri tipi analizi
- Primary Key ve Foreign Key tespiti
- Index ve constraint keşfi
- Trigger, Stored Procedure ve Function tespiti
- View analizi

### Veri Aktarımı
- Batch insert (performans için)
- İdempotent çalışma (upsert)
- Primary key'lerin `_id` olarak korunması
- Otomatik veri tipi dönüşümü
- Hata yönetimi ve loglama

### Raporlama
- Detaylı teknik rapor
- Dönüştürülen ve dönüştürülemeyen yapıların listesi
- Çözüm önerileri
- Migration istatistikleri

## Gereksinimler

- Python 3.7+
- MySQL veya MSSQL veritabanı
- MongoDB 3.6+ (transaction desteği için 4.0+ önerilir)

## Kullanım Örnekleri

Detaylı kullanım örnekleri için `example_usage.py` dosyasına bakın.

## Sorun Giderme

### MySQL Bağlantı Hatası
- MySQL sunucusunun çalıştığından emin olun
- Kullanıcı adı ve şifrenin doğru olduğundan emin olun
- Port numarasını kontrol edin (varsayılan: 3306)

### MSSQL Bağlantı Hatası
- ODBC Driver'ın yüklü olduğundan emin olun
- `trust_server_certificate` ayarını kontrol edin
- Port numarasını kontrol edin (varsayılan: 1433)

### MongoDB Bağlantı Hatası
- MongoDB sunucusunun çalıştığından emin olun
- Port numarasını kontrol edin (varsayılan: 27017)
- Authentication gerekiyorsa username/password ayarlarını kontrol edin

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

