# Video Çekimi İçin Terminal Komutları

## 🎬 Video Sırasında Kullanılacak Komutlar

### 1. Proje Dizinine Git
```bash
cd /Users/zeynepyilmaz/Desktop/database-final-project
```

### 2. Proje Yapısını Göster
```bash
tree -L 2 -I '__pycache__|*.pyc|venv' || ls -la
```

### 3. MySQL'de Test Veritabanını Kontrol Et
```bash
mysql -u root -p5545228936Zm. test_db -e "SHOW TABLES;"
```

### 4. MySQL'de Tablo Detaylarını Göster
```bash
mysql -u root -p5545228936Zm. test_db -e "SELECT COUNT(*) as kayit_sayisi, 'users' as tablo FROM users UNION SELECT COUNT(*), 'products' FROM products UNION SELECT COUNT(*), 'orders' FROM orders;"
```

### 5. MySQL'de Trigger'leri Göster
```bash
mysql -u root -p5545228936Zm. test_db -e "SHOW TRIGGERS;"
```

### 6. MySQL'de Stored Procedure'leri Göster
```bash
mysql -u root -p5545228936Zm. test_db -e "SHOW PROCEDURE STATUS WHERE Db = 'test_db';"
```

### 7. Virtual Environment Aktifleştir
```bash
source venv/bin/activate
```

### 8. Migration Uygulamasını Çalıştır
```bash
python main.py
```

### 9. MongoDB'de Collection'ları Listele
```bash
python -c "from pymongo import MongoClient; client = MongoClient('localhost', 27017); db = client['migrated_database']; print('Collections:', db.list_collection_names())"
```

### 10. MongoDB'de Belge Sayılarını Göster
```bash
python -c "from pymongo import MongoClient; client = MongoClient('localhost', 27017); db = client['migrated_database']; [print(f'{col}: {db[col].count_documents({})} documents') for col in db.list_collection_names()]"
```

### 11. MongoDB'de Örnek Belge Göster
```bash
python -c "from pymongo import MongoClient; import json; client = MongoClient('localhost', 27017); db = client['migrated_database']; user = db.users.find_one(); print(json.dumps(user, indent=2, default=str))"
```

### 12. MongoDB Veritabanını Sil (İdempotent Test İçin)
```bash
python -c "from pymongo import MongoClient; client = MongoClient('localhost', 27017); client.drop_database('migrated_database'); print('Veritabanı silindi')"
```

### 13. Rapor Dosyasını Göster
```bash
ls -lh reports/ | tail -1
```

### 14. En Son Raporu Aç (macOS)
```bash
open reports/$(ls -t reports/*.md | head -1)
```

### 15. Rapor İstatistiklerini Göster
```bash
cat reports/$(ls -t reports/*.md | head -1) | grep -A 5 "Migration İstatistikleri"
```

### 16. Dönüştürülemeyen Yapıları Göster
```bash
cat reports/$(ls -t reports/*.md | head -1) | grep -A 10 "Dönüştürülemeyen Yapılar"
```

---

## 🔄 İdempotent Test Senaryosu

### Senaryo: MongoDB'yi silip tekrar migration çalıştırma

```bash
# 1. MongoDB veritabanını sil
python -c "from pymongo import MongoClient; client = MongoClient('localhost', 27017); client.drop_database('migrated_database'); print('✅ Veritabanı silindi')"

# 2. Migration'ı tekrar çalıştır
python main.py

# 3. Sonuçları kontrol et
python -c "from pymongo import MongoClient; client = MongoClient('localhost', 27017); db = client['migrated_database']; print('Collections:', db.list_collection_names()); [print(f'{col}: {db[col].count_documents({})}') for col in db.list_collection_names()]"
```

---

## 📋 Hızlı Komut Listesi (Kopyala-Yapıştır İçin)

```bash
# Proje dizinine git
cd /Users/zeynepyilmaz/Desktop/database-final-project

# Virtual environment aktifleştir
source venv/bin/activate

# MySQL tablolarını kontrol et
mysql -u root -p5545228936Zm. test_db -e "SHOW TABLES;"

# Migration çalıştır
python main.py

# MongoDB'de kontrol et
python -c "from pymongo import MongoClient; client = MongoClient('localhost', 27017); db = client['migrated_database']; print('Collections:', db.list_collection_names())"
```

---

## ⚠️ Önemli Notlar

1. **MongoDB'yi silmek güvenlidir**: Proje idempotent çalıştığı için MongoDB'deki veritabanını silseniz bile, migration'ı tekrar çalıştırdığınızda aynı veritabanı ve veriler oluşturulur.

2. **Config dosyası**: `config.yaml` dosyasında MySQL şifresi var, video çekiminde dikkatli olun.

3. **Virtual environment**: Her terminal açılışında `source venv/bin/activate` çalıştırmanız gerekebilir.

4. **Rapor dosyaları**: Her migration'da yeni bir rapor oluşturulur, eski raporlar silinmez.

