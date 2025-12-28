# Test Veritabanı Kullanım Kılavuzu

## 📋 Test Veritabanı Özellikleri

Bu test veritabanı, migration uygulamasını test etmek için özel olarak tasarlanmıştır.

### İçerik

- **7 Tablo**: İlişkisel yapıda tablolar
- **Foreign Key'ler**: Tablolar arası ilişkiler
- **Primary Key'ler**: Her tabloda primary key
- **Index'ler**: Performans için çoklu index'ler
- **Check Constraint'ler**: Veri doğrulama kuralları
- **4 Trigger**: Otomatik işlemler
- **5 Stored Procedure**: İş mantığı fonksiyonları
- **3 Function**: Yardımcı fonksiyonlar
- **3 View**: Sorgu görünümleri
- **Örnek Veriler**: Test için hazır veriler

## 🚀 Kurulum

### Yöntem 1: Otomatik Script (Önerilen)

```bash
./setup_test_database.sh
```

Script, MySQL kullanıcı adı ve şifresini soracak ve veritabanını otomatik oluşturacaktır.

### Yöntem 2: Manuel Kurulum

```bash
# MySQL'e bağlan
mysql -u root -p

# SQL dosyasını çalıştır
source test_database.sql

# VEYA terminal'den
mysql -u root -p < test_database.sql
```

## 📊 Veritabanı Yapısı

### Tablolar

1. **users** - Kullanıcı bilgileri (4 kayıt)
2. **categories** - Ürün kategorileri (6 kayıt, hiyerarşik)
3. **products** - Ürün bilgileri (7 kayıt)
4. **orders** - Siparişler (5 kayıt)
5. **order_items** - Sipariş detayları (5 kayıt)
6. **payments** - Ödeme işlemleri (5 kayıt)

### İlişkiler

```
users (1) ──< orders (N)
categories (1) ──< products (N)
categories (1) ──< categories (N) [parent_category_id]
orders (1) ──< order_items (N)
orders (1) ──< payments (N)
products (1) ──< order_items (N)
```

### Trigger'ler

1. **before_order_insert** - Sipariş öncesi kontrol
2. **after_order_item_insert** - Sipariş detayı sonrası stok güncelleme
3. **after_order_cancel** - Sipariş iptalinde stok geri ekleme
4. **before_product_update** - Ürün güncelleme zamanı

### Stored Procedure'ler

1. **GetUserOrderHistory** - Kullanıcı sipariş geçmişi
2. **GetProductsByCategory** - Kategoriye göre ürünler
3. **CreateOrder** - Yeni sipariş oluşturma
4. **CalculateOrderTotal** - Sipariş toplamı hesaplama
5. **GetTopSellingProducts** - En çok satan ürünler

### Function'lar

1. **CalculateDaysBetween** - Tarih aralığı hesaplama
2. **GetUserTotalSpent** - Kullanıcı toplam harcama
3. **GetAverageProductPrice** - Ortalama ürün fiyatı

### View'ler

1. **user_order_summary** - Kullanıcı sipariş özeti
2. **product_stock_status** - Ürün stok durumu
3. **daily_sales_summary** - Günlük satış özeti

## ⚙️ Config.yaml Ayarları

Test veritabanını kullanmak için `config.yaml` dosyasını şu şekilde ayarlayın:

```yaml
sql_database:
  type: "mysql"
  host: "localhost"
  port: 3306
  database: "ecommerce_test"
  username: "root"  # MySQL kullanıcı adınız
  password: ""      # MySQL şifreniz

mongodb:
  host: "localhost"
  port: 27017
  database: "ecommerce_migrated"  # MongoDB'de oluşturulacak
```

## 🧪 Test Senaryoları

### Senaryo 1: Basit Migration
```bash
python main.py
```

### Senaryo 2: İdempotent Test
```bash
# İlk çalıştırma
python main.py

# İkinci çalıştırma (aynı veriler tekrar eklenmemeli)
python main.py
```

### Senaryo 3: Drop Existing
```yaml
# config.yaml'da
migration:
  drop_existing: true  # Mevcut collection'ları sil
```

## 📝 Test Sorguları

### MySQL'de Test

```sql
USE ecommerce_test;

-- Stored procedure test
CALL GetUserOrderHistory(1);
CALL GetTopSellingProducts(5);

-- Function test
SELECT GetUserTotalSpent(1);
SELECT GetAverageProductPrice();

-- View test
SELECT * FROM user_order_summary;
SELECT * FROM product_stock_status;
```

### MongoDB'de Kontrol

```bash
mongosh

use ecommerce_migrated

# Collection'ları listele
show collections

# Verileri kontrol et
db.users.find()
db.orders.find()
db.products.find()

# İstatistikler
db.users.countDocuments()
db.orders.countDocuments()
db.products.countDocuments()
```

## 🔍 Beklenen Sonuçlar

Migration sonrası MongoDB'de:

- **7 Collection**: Her tablo bir collection
- **32 Belge**: Toplam kayıt sayısı
  - users: 4
  - categories: 6
  - products: 7
  - orders: 5
  - order_items: 5
  - payments: 5
- **Index'ler**: Primary key ve diğer index'ler oluşturulmuş
- **Rapor**: Detaylı teknik rapor oluşturulmuş

## 🐛 Sorun Giderme

### Veritabanı Oluşturulamıyor
- MySQL sunucusunun çalıştığından emin olun
- Kullanıcının CREATE DATABASE yetkisi olduğundan emin olun

### Trigger/SP Bulunamıyor
- MySQL versiyonunuzun 5.0+ olduğundan emin olun
- DELIMITER komutlarının doğru çalıştığından emin olun

### Foreign Key Hatası
- Tabloların doğru sırayla oluşturulduğundan emin olun
- Mevcut veritabanını silip yeniden oluşturun

## 📚 Ek Bilgiler

- Veritabanı adı: `ecommerce_test`
- Karakter seti: `utf8mb4`
- Engine: `InnoDB` (Foreign Key desteği için)
- Tüm tablolarda örnek veriler mevcuttur

