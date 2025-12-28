# Proje Yapısı

Bu dokümantasyon, projenin yapısını ve her dosyanın işlevini açıklar.

## Dizin Yapısı

```
database-final-project/
├── main.py                          # Ana uygulama dosyası
├── config.yaml                      # Konfigürasyon dosyası
├── requirements.txt                 # Python bağımlılıkları
├── README.md                        # Proje açıklaması
├── .gitignore                       # Git ignore dosyası
├── setup.sh                         # Kurulum scripti
├── example_usage.py                 # Örnek kullanım senaryoları
├── TECHNICAL_REPORT_TEMPLATE.md     # Teknik rapor şablonu
│
├── src/                             # Kaynak kod dizini
│   ├── __init__.py
│   │
│   ├── database/                    # Veritabanı modülleri
│   │   ├── __init__.py
│   │   ├── sql_connector.py         # SQL veritabanı bağlantısı
│   │   ├── schema_discovery.py      # Şema keşif modülü
│   │   └── mongodb_connector.py     # MongoDB bağlantısı
│   │
│   ├── migration/                   # Veri aktarım modülleri
│   │   ├── __init__.py
│   │   └── migrator.py              # Veri aktarım sınıfı
│   │
│   └── reporting/                   # Raporlama modülleri
│       ├── __init__.py
│       └── report_generator.py      # Rapor oluşturucu
│
├── logs/                            # Log dosyaları
└── reports/                         # Oluşturulan raporlar
```

## Dosya Açıklamaları

### Ana Dosyalar

- **main.py**: Uygulamanın giriş noktası. Tüm modülleri bir araya getirir ve migration sürecini yönetir.

- **config.yaml**: Tüm konfigürasyon ayarları (SQL bağlantı bilgileri, MongoDB ayarları, migration parametreleri).

- **requirements.txt**: Projenin Python bağımlılıkları.

### Database Modülleri

- **sql_connector.py**: MySQL ve MSSQL veritabanlarına bağlanmayı sağlar. SQLAlchemy kullanır.

- **schema_discovery.py**: Veritabanı şemasını dinamik olarak keşfeder. Tablolar, kolonlar, indexler, constraintler, triggerler, stored procedure'ler ve function'ları tespit eder.

- **mongodb_connector.py**: MongoDB veritabanına bağlanmayı ve işlem yapmayı sağlar. PyMongo kullanır.

### Migration Modülleri

- **migrator.py**: SQL veritabanından MongoDB'ye veri aktarımını gerçekleştirir. İdempotent çalışma sağlar (upsert kullanarak).

### Reporting Modülleri

- **report_generator.py**: Migration sürecini ve sonuçlarını detaylı teknik rapor olarak oluşturur. Markdown formatında rapor üretir.

## Modül İlişkileri

```
main.py
  ├── SQLConnector (sql_connector.py)
  │     └── SchemaDiscovery (schema_discovery.py)
  │
  ├── MongoDBConnector (mongodb_connector.py)
  │
  ├── DataMigrator (migrator.py)
  │     ├── SQLConnector
  │     └── MongoDBConnector
  │
  └── ReportGenerator (report_generator.py)
        └── SchemaInfo + MigrationStats
```

## Çalışma Akışı

1. **Başlangıç**: `main.py` çalıştırılır, konfigürasyon yüklenir.

2. **Bağlantı**: SQL ve MongoDB bağlantıları kurulur.

3. **Şema Keşfi**: `SchemaDiscovery` tüm veritabanı yapılarını keşfeder.

4. **Veri Aktarımı**: `DataMigrator` verileri SQL'den MongoDB'ye aktarır.

5. **Raporlama**: `ReportGenerator` detaylı teknik rapor oluşturur.

6. **Sonlandırma**: Bağlantılar kapatılır, istatistikler gösterilir.

## Genişletilebilirlik

Proje modüler yapıda tasarlanmıştır. Yeni özellikler eklemek için:

- Yeni veritabanı desteği: `sql_connector.py`'ye yeni connection string builder eklenebilir.
- Yeni şema bileşenleri: `schema_discovery.py`'ye yeni keşif metodları eklenebilir.
- Yeni rapor formatları: `report_generator.py`'ye yeni format desteği eklenebilir.

