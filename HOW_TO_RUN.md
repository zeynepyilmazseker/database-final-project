# Projeyi Çalıştırma Kılavuzu

## 📋 Adım 1: Gereksinimleri Yükleyin

```bash
# Python 3.7+ yüklü olduğundan emin olun
python3 --version

# Gerekli paketleri yükleyin
pip install -r requirements.txt

# VEYA virtual environment kullanın (önerilir)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📋 Adım 2: Veritabanlarını Hazırlayın

### MySQL veya MSSQL Veritabanı
- Veritabanı sunucusunun çalıştığından emin olun
- Test için örnek tablolar oluşturabilirsiniz (opsiyonel)

### MongoDB
- MongoDB sunucusunun çalıştığından emin olun
- MongoDB Community Edition: https://www.mongodb.com/try/download/community
- Veya MongoDB Atlas kullanabilirsiniz: https://www.mongodb.com/cloud/atlas

## 📋 Adım 3: Konfigürasyonu Düzenleyin

`config.yaml` dosyasını açın ve aşağıdaki bilgileri doldurun:

```yaml
sql_database:
  type: "mysql"  # veya "mssql"
  host: "localhost"
  port: 3306  # MySQL: 3306, MSSQL: 1433
  database: "your_database_name"
  username: "your_username"
  password: "your_password"

mongodb:
  host: "localhost"
  port: 27017
  database: "migrated_database"
```

## 📋 Adım 4: Uygulamayı Çalıştırın

```bash
python main.py
```

## 📋 Adım 5: Sonuçları Kontrol Edin

- **Loglar**: `logs/migration.log` dosyasında
- **Rapor**: `reports/` dizininde oluşturulan markdown dosyası

## 🧪 Test Senaryosu (MySQL Örneği)

Eğer test için örnek bir veritabanı oluşturmak isterseniz:

```sql
-- MySQL'de test veritabanı oluştur
CREATE DATABASE test_db;
USE test_db;

-- Örnek tablo oluştur
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Örnek veri ekle
INSERT INTO users (name, email) VALUES 
    ('Ahmet Yılmaz', 'ahmet@example.com'),
    ('Ayşe Demir', 'ayse@example.com'),
    ('Mehmet Kaya', 'mehmet@example.com');

-- İkinci tablo (Foreign Key ile)
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    product_name VARCHAR(100),
    amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO orders (user_id, product_name, amount) VALUES
    (1, 'Laptop', 15000.00),
    (1, 'Mouse', 250.50),
    (2, 'Keyboard', 500.00);
```

Sonra `config.yaml`'da:
```yaml
sql_database:
  type: "mysql"
  database: "test_db"
  # ... diğer bilgiler
```

## 🐛 Sorun Giderme

### "ModuleNotFoundError" Hatası
```bash
pip install -r requirements.txt
```

### MySQL Bağlantı Hatası
- MySQL sunucusunun çalıştığından emin olun: `mysql -u root -p`
- Port 3306'ın açık olduğundan emin olun
- Kullanıcı adı ve şifreyi kontrol edin

### MSSQL Bağlantı Hatası
- ODBC Driver'ın yüklü olduğundan emin olun
- SQL Server'ın çalıştığından emin olun
- Port 1433'ün açık olduğundan emin olun

### MongoDB Bağlantı Hatası
- MongoDB'nin çalıştığından emin olun: `mongod --version`
- Port 27017'nin açık olduğundan emin olun
- MongoDB servisini başlatın: `brew services start mongodb-community` (Mac) veya `sudo systemctl start mongod` (Linux)

## 📊 Beklenen Çıktı

```
============================================================
SQL → MongoDB Migration Tool
============================================================

2024-01-01 10:00:00 - INFO - Migration uygulaması başlatılıyor...
2024-01-01 10:00:01 - INFO - MySQL veritabanına başarıyla bağlanıldı
2024-01-01 10:00:02 - INFO - Veritabanı şeması keşfediliyor...
2024-01-01 10:00:03 - INFO - 2 tablo bulundu: users, orders
2024-01-01 10:00:04 - INFO - MongoDB'ye başarıyla bağlanıldı
2024-01-01 10:00:05 - INFO - Veri aktarımı başlatılıyor...
2024-01-01 10:00:06 - INFO - users tablosu aktarılıyor...
2024-01-01 10:00:07 - INFO - orders tablosu aktarılıyor...
2024-01-01 10:00:08 - INFO - Veri aktarımı tamamlandı. 2 tablo, 5 belge aktarıldı.
2024-01-01 10:00:09 - INFO - Teknik rapor oluşturuluyor...
2024-01-01 10:00:10 - INFO - Rapor oluşturuldu: reports/migration_report_20240101_100010.md

============================================================
MIGRATION TAMAMLANDI
============================================================
Aktarılan Tablo Sayısı: 2
Aktarılan Belge Sayısı: 5
Hata Sayısı: 0
Rapor: reports/migration_report_20240101_100010.md
============================================================
```

## 🔍 MongoDB'de Verileri Kontrol Etme

```bash
# MongoDB shell'e bağlan
mongosh

# Veritabanını seç
use migrated_database

# Collection'ları listele
show collections

# Verileri görüntüle
db.users.find()
db.orders.find()
```

## 📝 Notlar

- İlk çalıştırmada `logs/` ve `reports/` dizinleri otomatik oluşturulur
- Migration idempotent'tir - aynı migration'ı tekrar çalıştırabilirsiniz
- Primary key'ler MongoDB'de `_id` olarak saklanır
- Rapor dosyası her çalıştırmada yeni bir timestamp ile oluşturulur

