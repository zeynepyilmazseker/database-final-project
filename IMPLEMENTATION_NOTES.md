# Uygulama Notları

Bu dokümantasyon, projenin teknik detaylarını ve implementasyon notlarını içerir.

## Teknik Detaylar

### 1. Veritabanı Bağlantısı

#### SQL Bağlantısı
- **SQLAlchemy** kullanılarak MySQL ve MSSQL desteği sağlanmıştır
- Connection string'ler dinamik olarak oluşturulur
- Bağlantı testi yapılarak hata kontrolü sağlanır

#### MongoDB Bağlantısı
- **PyMongo** kullanılarak MongoDB bağlantısı sağlanmıştır
- Connection string veya manuel bağlantı bilgileri kullanılabilir
- Authentication desteği mevcuttur

### 2. Şema Keşfi

#### Keşif Metodolojisi
1. **SQLAlchemy Inspector**: Temel şema bilgileri için kullanılır
   - Tablolar
   - Kolonlar ve veri tipleri
   - Primary Key'ler
   - Foreign Key'ler
   - Index'ler

2. **SQL Sorguları**: Özel bilgiler için kullanılır
   - Check Constraint'ler (INFORMATION_SCHEMA veya sys tabloları)
   - Trigger'ler
   - Stored Procedure'ler
   - Function'lar
   - View'ler

#### Veritabanı Desteği
- **MySQL**: INFORMATION_SCHEMA tabloları kullanılır
- **MSSQL**: sys tabloları ve INFORMATION_SCHEMA kullanılır

### 3. Veri Aktarımı

#### Dönüşüm Stratejisi
- **Tablolar → Collections**: Her SQL tablosu bir MongoDB collection'ına dönüştürülür
- **Satırlar → Belgeler**: Her SQL satırı bir MongoDB belgesine dönüştürülür
- **Primary Key → _id**: Primary key kolonları MongoDB `_id` alanına dönüştürülür
  - Tek kolonlu PK: Doğrudan `_id` olarak kullanılır
  - Composite PK: Kolonlar birleştirilerek string `_id` oluşturulur

#### İdempotent Çalışma
- **Upsert** kullanılarak tekrar çalıştırılabilirlik sağlanır
- Primary key'ler `_id` olarak kullanıldığında, aynı kayıt tekrar eklenmez, güncellenir
- `drop_existing` seçeneği ile mevcut collection'lar silinebilir

#### Performans Optimizasyonları
- **Batch Insert**: Büyük veri setleri için batch'ler halinde ekleme yapılır
- Varsayılan batch size: 1000 belge
- Bulk write operations kullanılır

#### Veri Tipi Dönüşümleri
- **DateTime**: ISO 8601 string formatına dönüştürülür
- **Decimal**: Float'a dönüştürülür
- **NULL**: MongoDB'de `null` olarak saklanır
- **Diğer tipler**: Olduğu gibi aktarılır

### 4. Index Oluşturma

- Primary key'ler otomatik olarak unique index olarak oluşturulur
- Diğer index'ler MongoDB'de aynı şekilde oluşturulur
- Unique index'ler işaretlenir

### 5. Raporlama

#### Rapor İçeriği
1. **Veritabanı Keşif Süreci**: Bağlantı bilgileri ve metodoloji
2. **Tespit Edilen Nesneler**: Tüm şema bileşenlerinin listesi
3. **MongoDB Veri Modeli**: Dönüşüm stratejisi ve örnek yapılar
4. **Dönüştürülen Yapılar**: Başarıyla aktarılan yapılar
5. **Dönüştürülemeyen Yapılar**: Neden dönüştürülemediği ve çözüm önerileri
6. **Problemler ve Çözümler**: Karşılaşılan sorunlar ve çözüm önerileri

#### Rapor Formatı
- **Markdown**: Varsayılan format, GitHub'da iyi görünür
- **HTML**: Gelecekte eklenebilir

## Dönüştürülemeyen Yapılar ve Çözümleri

### Foreign Key İlişkileri
**Neden dönüştürülemez?**
- MongoDB'de foreign key constraint'leri desteklenmez
- Referans bütünlüğü veritabanı seviyesinde kontrol edilmez

**Çözüm Önerileri:**
1. Referansları belge içinde alan olarak sakla
2. Uygulama katmanında referans kontrolü yap
3. MongoDB validation rules kullan (MongoDB 3.6+)
4. Mongoose/Pydantic gibi ODM/ORM araçları kullan

### Check Constraint'ler
**Neden dönüştürülemez?**
- MongoDB'de check constraint'ler doğrudan desteklenmez

**Çözüm Önerileri:**
1. MongoDB JSON Schema validation kullan (MongoDB 3.6+)
2. Uygulama katmanında veri doğrulama yap
3. ODM/ORM araçları kullan

### Trigger'ler
**Neden dönüştürülemez?**
- MongoDB'de trigger'ler desteklenmez

**Çözüm Önerileri:**
1. MongoDB Change Streams kullanarak değişiklikleri izle
2. Event-driven mimari kullan
3. MongoDB Realm Functions kullan
4. Serverless functions kullan

### Stored Procedure'ler
**Neden dönüştürülemez?**
- MongoDB'de stored procedure'ler desteklenmez

**Çözüm Önerileri:**
1. Mantığı uygulama katmanına taşı
2. MongoDB aggregation pipeline'lar kullan
3. MongoDB Realm Functions kullan
4. Uygulama kodunda fonksiyonlar olarak implement et

### Function'lar
**Neden dönüştürülemez?**
- MongoDB'de SQL function'ları desteklenmez

**Çözüm Önerileri:**
1. Mantığı uygulama katmanına taşı
2. MongoDB aggregation pipeline'lar kullan
3. Uygulama kodunda fonksiyonlar olarak implement et

### View'ler
**Neden dönüştürülemez?**
- SQL view'leri MongoDB'de doğrudan desteklenmez

**Çözüm Önerileri:**
1. MongoDB View'leri kullan (MongoDB 3.4+)
2. Aggregation pipeline'lar kullan
3. Uygulama katmanında sorgu fonksiyonları olarak implement et

## Hata Yönetimi

### Loglama
- **Seviyeler**: DEBUG, INFO, WARNING, ERROR
- **Çıktılar**: Dosya ve konsol
- **Format**: Renkli konsol çıktısı (colorlog)

### Hata İşleme
- Bağlantı hataları yakalanır ve loglanır
- Migration sırasında hatalar toplanır ve raporlanır
- Her tablo için ayrı hata yönetimi yapılır
- Kritik hatalar uygulamayı durdurmaz, loglanır

## Performans Notları

### Büyük Veri Setleri
- Batch insert kullanılır (varsayılan: 1000)
- Batch size konfigürasyon dosyasından ayarlanabilir
- Memory kullanımı optimize edilir

### İndex'ler
- Primary key index'leri otomatik oluşturulur
- Diğer index'ler korunur
- Unique index'ler işaretlenir

## Güvenlik Notları

### Bağlantı Bilgileri
- Şifreler config.yaml dosyasında saklanır
- Production ortamında environment variables kullanılmalıdır
- .gitignore dosyası config.yaml'ı ignore etmez (dikkatli olun!)

### Öneriler
- Config dosyasını Git'e commit etmeyin
- Environment variables kullanın
- MongoDB authentication kullanın
- SSL/TLS bağlantıları kullanın (production)

## Test Senaryoları

### Önerilen Testler
1. **Boş veritabanı**: Hiç tablo yok
2. **Tek tablo**: Basit bir tablo
3. **Çoklu tablo**: Birden fazla tablo
4. **İlişkisel veri**: Foreign key'ler
5. **Büyük veri seti**: Binlerce kayıt
6. **Özel veri tipleri**: DateTime, Decimal, vb.
7. **İdempotent test**: Aynı migration'ı iki kez çalıştırma

## Gelecek Geliştirmeler

### Potansiyel Özellikler
1. **PostgreSQL desteği**: Şu anda sadece MySQL ve MSSQL
2. **Incremental migration**: Sadece değişen verileri aktarma
3. **Data validation**: Aktarılan verilerin doğruluğunu kontrol etme
4. **Rollback**: Migration'ı geri alma
5. **Parallel migration**: Birden fazla tabloyu paralel aktarma
6. **Progress bar**: İlerleme çubuğu
7. **Email notification**: Migration tamamlandığında e-posta gönderme

## Kod Kalitesi

### Standartlar
- PEP 8 Python kodlama standartlarına uyulmuştur
- Docstring'ler tüm fonksiyonlarda mevcuttur
- Türkçe yorumlar kullanılmıştır
- Modüler yapı tercih edilmiştir

### Bakım
- Kod yorumları güncel tutulmalıdır
- Yeni özellikler eklenirken dokümantasyon güncellenmelidir
- Test senaryoları genişletilmelidir

