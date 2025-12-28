# İdempotent Test - MongoDB Veritabanını Silme ve Tekrar Oluşturma

## ✅ Cevap: Evet, Aynı DB Oluşur!

Proje **idempotent** çalışacak şekilde tasarlanmıştır. Bu demek oluyor ki:

- MongoDB'deki `migrated_database` veritabanını silseniz bile
- Migration'ı tekrar çalıştırdığınızda
- **Aynı veritabanı ve veriler tekrar oluşturulur**

## 🔄 Nasıl Çalışır?

1. **Upsert Mekanizması**: Primary key'ler `_id` olarak kullanıldığı için, aynı `_id` ile belge varsa güncellenir, yoksa oluşturulur.

2. **Drop Existing Seçeneği**: `config.yaml`'da `drop_existing: false` olduğu için mevcut collection'lar silinmez, sadece güncellenir.

3. **Tekrar Çalıştırılabilirlik**: Aynı migration'ı istediğiniz kadar çalıştırabilirsiniz, her seferinde aynı sonuçları alırsınız.

## 🧪 Test Senaryosu

### Senaryo 1: MongoDB'yi Sil ve Tekrar Çalıştır

```bash
# 1. MongoDB veritabanını sil
python3 -c "from pymongo import MongoClient; client = MongoClient('localhost', 27017); client.drop_database('migrated_database'); print('✅ Veritabanı silindi')"

# 2. Migration'ı tekrar çalıştır
source venv/bin/activate
python main.py

# 3. Sonuçları kontrol et
python3 -c "from pymongo import MongoClient; client = MongoClient('localhost', 27017); db = client['migrated_database']; print('Collections:', db.list_collection_names()); [print(f'{col}: {db[col].count_documents({})}') for col in db.list_collection_names()]"
```

**Beklenen Sonuç:**
- 6 collection oluşturulur
- 32 belge aktarılır
- Aynı veriler tekrar oluşturulur

### Senaryo 2: Mevcut Verilerle Tekrar Çalıştır

```bash
# Migration'ı tekrar çalıştır (veritabanı mevcut)
python main.py
```

**Beklenen Sonuç:**
- Mevcut belgeler güncellenir (upsert)
- Yeni belge eklenmez (zaten var)
- Aynı sayıda belge kalır (32)

## 📊 Video Çekimi İçin Öneri

Video çekiminde şu sırayı takip edin:

1. **İlk Migration**: MongoDB boşken migration çalıştır
2. **Sonuçları Göster**: Collection'ları ve belge sayılarını göster
3. **MongoDB'yi Sil**: Veritabanını sil
4. **Tekrar Migration**: Aynı migration'ı tekrar çalıştır
5. **Aynı Sonuçları Göster**: Aynı collection'lar ve belge sayıları oluştuğunu göster

Bu, projenin **idempotent** özelliğini güzel bir şekilde gösterir.

## ⚙️ Config Ayarları

`config.yaml` dosyasında:

```yaml
migration:
  drop_existing: false  # Mevcut collection'ları silme
  preserve_ids: true    # Primary key'leri _id olarak kullan
```

- `drop_existing: false` → Mevcut collection'lar silinmez, sadece güncellenir
- `drop_existing: true` → Mevcut collection'lar silinir ve yeniden oluşturulur

Her iki durumda da idempotent çalışır, sadece davranış farklıdır.

## 🎯 Sonuç

**Evet, MongoDB'deki veritabanını silseniz ve migration'ı tekrar çalıştırsanız, aynı veritabanı ve veriler tekrar oluşturulur!**

Bu, projenin en önemli özelliklerinden biridir ve production ortamında güvenli bir şekilde migration'ı tekrar çalıştırmanıza olanak sağlar.

