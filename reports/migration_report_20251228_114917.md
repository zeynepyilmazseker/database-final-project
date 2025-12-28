# SQL → MongoDB Migration Teknik Raporu

**Oluşturulma Tarihi:** 2025-12-28 11:49:17

---

## 1. Veritabanı Keşif Süreci

### Bağlantı Bilgileri

- **Veritabanı Tipi:** MYSQL
- **Host:** localhost
- **Port:** 3306
- **Database:** test_db
- **Username:** root

### Keşif Metodolojisi

Veritabanı şeması aşağıdaki adımlarla keşfedilmiştir:

1. SQLAlchemy Inspector kullanılarak tablo listesi alındı
2. Her tablo için kolon bilgileri, veri tipleri ve özellikler tespit edildi
3. Primary Key ve Foreign Key ilişkileri analiz edildi
4. Index'ler ve constraint'ler keşfedildi
5. Trigger'ler ve stored procedure'ler tespit edildi
6. View'ler ve function'lar analiz edildi

## 2. Tespit Edilen Nesnelerin Listesi

### Tablolar (6)

- `categories`
- `order_items`
- `orders`
- `payments`
- `products`
- `users`

### Kolonlar ve Veri Tipleri

#### Tablo: `categories`

| Kolon | Tip | Nullable | Default |
|-------|-----|----------|----------|
| category_id | INTEGER | Hayır | None |
| category_name | VARCHAR(100) COLLATE "utf8mb4_turkish_ci" | Hayır | None |
| description | TEXT COLLATE "utf8mb4_turkish_ci" | Evet | None |
| parent_category_id | INTEGER | Evet | None |
| created_at | DATETIME | Evet | CURRENT_TIMESTAMP |

#### Tablo: `order_items`

| Kolon | Tip | Nullable | Default |
|-------|-----|----------|----------|
| order_item_id | INTEGER | Hayır | None |
| order_id | INTEGER | Hayır | None |
| product_id | INTEGER | Hayır | None |
| quantity | INTEGER | Hayır | None |
| unit_price | DECIMAL(10, 2) | Hayır | None |
| subtotal | DECIMAL(10, 2) | Hayır | None |

#### Tablo: `orders`

| Kolon | Tip | Nullable | Default |
|-------|-----|----------|----------|
| order_id | INTEGER | Hayır | None |
| user_id | INTEGER | Hayır | None |
| order_date | DATETIME | Evet | CURRENT_TIMESTAMP |
| total_amount | DECIMAL(10, 2) | Hayır | None |
| status | ENUM | Evet | 'pending' |
| shipping_address | TEXT COLLATE "utf8mb4_turkish_ci" | Hayır | None |
| notes | TEXT COLLATE "utf8mb4_turkish_ci" | Evet | None |

#### Tablo: `payments`

| Kolon | Tip | Nullable | Default |
|-------|-----|----------|----------|
| payment_id | INTEGER | Hayır | None |
| order_id | INTEGER | Hayır | None |
| payment_method | ENUM | Hayır | None |
| amount | DECIMAL(10, 2) | Hayır | None |
| payment_date | DATETIME | Evet | CURRENT_TIMESTAMP |
| status | ENUM | Evet | 'pending' |
| transaction_id | VARCHAR(100) COLLATE "utf8mb4_turkish_ci" | Evet | None |

#### Tablo: `products`

| Kolon | Tip | Nullable | Default |
|-------|-----|----------|----------|
| product_id | INTEGER | Hayır | None |
| product_name | VARCHAR(200) COLLATE "utf8mb4_turkish_ci" | Hayır | None |
| description | TEXT COLLATE "utf8mb4_turkish_ci" | Evet | None |
| category_id | INTEGER | Hayır | None |
| price | DECIMAL(10, 2) | Hayır | None |
| stock_quantity | INTEGER | Hayır | '0' |
| sku | VARCHAR(50) COLLATE "utf8mb4_turkish_ci" | Evet | None |
| created_at | DATETIME | Evet | CURRENT_TIMESTAMP |
| updated_at | DATETIME | Evet | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

#### Tablo: `users`

| Kolon | Tip | Nullable | Default |
|-------|-----|----------|----------|
| user_id | INTEGER | Hayır | None |
| username | VARCHAR(50) COLLATE "utf8mb4_turkish_ci" | Hayır | None |
| email | VARCHAR(100) COLLATE "utf8mb4_turkish_ci" | Hayır | None |
| password_hash | VARCHAR(255) COLLATE "utf8mb4_turkish_ci" | Hayır | None |
| first_name | VARCHAR(50) COLLATE "utf8mb4_turkish_ci" | Hayır | None |
| last_name | VARCHAR(50) COLLATE "utf8mb4_turkish_ci" | Hayır | None |
| phone | VARCHAR(20) COLLATE "utf8mb4_turkish_ci" | Evet | None |
| birth_date | DATE | Evet | None |
| registration_date | DATETIME | Evet | CURRENT_TIMESTAMP |
| is_active | TINYINT | Evet | '1' |
| balance | DECIMAL(10, 2) | Evet | '0.00' |

### Primary Key'ler

- **categories:** category_id
- **order_items:** order_item_id
- **orders:** order_id
- **payments:** payment_id
- **products:** product_id
- **users:** user_id

### Foreign Key'ler

#### Tablo: `categories`

- **categories_ibfk_1:** parent_category_id → categories.category_id

#### Tablo: `order_items`

- **order_items_ibfk_1:** order_id → orders.order_id
- **order_items_ibfk_2:** product_id → products.product_id

#### Tablo: `orders`

- **orders_ibfk_1:** user_id → users.user_id

#### Tablo: `payments`

- **payments_ibfk_1:** order_id → orders.order_id

#### Tablo: `products`

- **products_ibfk_1:** category_id → categories.category_id

### Index'ler

#### Tablo: `categories`

- **category_name:** category_name (Unique)
- **idx_parent_category:** parent_category_id

#### Tablo: `order_items`

- **idx_order:** order_id
- **idx_product:** product_id

#### Tablo: `orders`

- **idx_order_date:** order_date
- **idx_status:** status
- **idx_user:** user_id

#### Tablo: `payments`

- **idx_order_payment:** order_id
- **idx_payment_date:** payment_date
- **idx_status_payment:** status
- **transaction_id:** transaction_id (Unique)

#### Tablo: `products`

- **idx_category:** category_id
- **idx_price:** price
- **idx_sku:** sku
- **idx_stock:** stock_quantity
- **sku:** sku (Unique)

#### Tablo: `users`

- **email:** email (Unique)
- **idx_email:** email
- **idx_registration_date:** registration_date
- **idx_username:** username
- **username:** username (Unique)

### Check Constraint'ler

Check constraint bulunamadı.

### Trigger'ler

#### Tablo: `orders`

- **before_order_insert:** BEFORE INSERT
- **after_order_cancel:** AFTER UPDATE

#### Tablo: `order_items`

- **after_order_item_insert:** AFTER INSERT

#### Tablo: `products`

- **before_product_update:** BEFORE UPDATE

### Stored Procedure'ler

- `CalculateOrderTotal`
- `CreateOrder`
- `GetProductsByCategory`
- `GetTopSellingProducts`
- `GetUserOrderHistory`

### Function'lar

- `CalculateDaysBetween`
- `GetAverageProductPrice`
- `GetUserTotalSpent`

### View'ler

- `daily_sales_summary`
- `product_stock_status`
- `user_order_summary`

## 3. MongoDB Veri Modeli

### Dönüşüm Stratejisi

SQL veritabanı yapıları MongoDB'ye aşağıdaki şekilde dönüştürülmüştür:

- **Tablolar → Collections:** Her SQL tablosu bir MongoDB collection'ına dönüştürülmüştür
- **Satırlar → Belgeler:** Her SQL satırı bir MongoDB belgesine (document) dönüştürülmüştür
- **Kolonlar → Alanlar:** SQL kolonları MongoDB belge alanlarına dönüştürülmüştür
- **Primary Key → _id:** Primary key kolonları MongoDB `_id` alanına dönüştürülmüştür
- **Foreign Key → Referans:** Foreign key ilişkileri belge içinde referans olarak saklanmıştır
- **Index'ler:** SQL index'leri MongoDB index'lerine dönüştürülmüştür

### Örnek Belge Yapısı

**Collection:** `categories`

```json
{
  "category_id": <INTEGER>,
  "category_name": <VARCHAR(100) COLLATE "utf8mb4_turkish_ci">,
  "description": <TEXT COLLATE "utf8mb4_turkish_ci">,
  "parent_category_id": <INTEGER>,
  "created_at": <DATETIME>
}
```

## 4. Dönüştürülen Yapılar

Aşağıdaki yapılar başarıyla MongoDB'ye dönüştürülmüştür:

- ✅ **Tablolar:** 6 tablo collection'a dönüştürüldü
- ✅ **Kolonlar:** Tüm kolonlar belge alanlarına dönüştürüldü
- ✅ **Primary Key'ler:** Primary key'ler `_id` alanına dönüştürüldü
- ✅ **Index'ler:** 21 index oluşturuldu
- ✅ **Veri:** 0 belge aktarıldı

## 5. Dönüştürülemeyen Yapılar ve Gerekçeleri

### Foreign Key İlişkileri

**Durum:** Foreign key constraint'leri MongoDB'de doğrudan desteklenmez.

**Çözüm Önerisi:**
- Foreign key referansları belge içinde alan olarak saklanır
- Uygulama katmanında referans bütünlüğü kontrol edilmelidir
- Gerekirse MongoDB'de referans kontrolü için validation kuralları eklenebilir

### Check Constraint'ler

Check constraint bulunmadığı için dönüşüm gerekmedi.

### Trigger'ler

**Durum:** Trigger'ler MongoDB'de doğrudan desteklenmez.

**Çözüm Önerisi:**
- MongoDB Change Streams kullanılarak değişiklikler izlenebilir
- Uygulama katmanında event-driven mimari kullanılabilir
- MongoDB Realm Functions veya serverless functions kullanılabilir

### Stored Procedure'ler

**Durum:** Stored procedure'ler MongoDB'de doğrudan desteklenmez.

**Çözüm Önerisi:**
- Stored procedure mantığı uygulama katmanına taşınmalıdır
- MongoDB'de aggregation pipeline'lar kullanılabilir
- MongoDB Realm Functions veya serverless functions kullanılabilir
- Uygulama kodunda fonksiyonlar olarak implement edilmelidir

### Function'lar

**Durum:** SQL function'ları MongoDB'de doğrudan desteklenmez.

**Çözüm Önerisi:**
- Function mantığı uygulama katmanına taşınmalıdır
- MongoDB aggregation pipeline'lar kullanılabilir
- Uygulama kodunda fonksiyonlar olarak implement edilmelidir

### View'ler

**Durum:** SQL view'leri MongoDB'de doğrudan desteklenmez.

**Çözüm Önerisi:**
- View mantığı MongoDB aggregation pipeline'larına dönüştürülebilir
- MongoDB View'leri (MongoDB 3.4+) kullanılabilir
- Uygulama katmanında sorgu fonksiyonları olarak implement edilmelidir

## 6. Karşılaşılan Problemler ve Çözüm Önerileri

### Migration Sırasında Karşılaşılan Hatalar

1. categories tablosu aktarım hatası: batch op errors occurred, full error: {'writeErrors': [{'index': 1, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.categories index: category_id_1 dup key: { category_id: null }', 'keyPattern': {'category_id': 1}, 'keyValue': {'category_id': None}, 'op': {'q': {'_id': 2.0}, 'u': {'$set': {'category_name': 'Bilgisayar', 'description': 'Bilgisayar ve aksesuarlarÄ±', 'parent_category_id': 1.0, 'created_at': '2025-12-28T11:48:21'}}, 'multi': False, 'upsert': True}}, {'index': 2, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.categories index: category_id_1 dup key: { category_id: null }', 'keyPattern': {'category_id': 1}, 'keyValue': {'category_id': None}, 'op': {'q': {'_id': 3.0}, 'u': {'$set': {'category_name': 'Telefon', 'description': 'Cep telefonu ve aksesuarlarÄ±', 'parent_category_id': 1.0, 'created_at': '2025-12-28T11:48:21'}}, 'multi': False, 'upsert': True}}, {'index': 3, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.categories index: category_id_1 dup key: { category_id: null }', 'keyPattern': {'category_id': 1}, 'keyValue': {'category_id': None}, 'op': {'q': {'_id': 4.0}, 'u': {'$set': {'category_name': 'Giyim', 'description': 'Giyim ve moda Ã¼rÃ¼nleri', 'parent_category_id': None, 'created_at': '2025-12-28T11:48:21'}}, 'multi': False, 'upsert': True}}, {'index': 4, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.categories index: category_id_1 dup key: { category_id: null }', 'keyPattern': {'category_id': 1}, 'keyValue': {'category_id': None}, 'op': {'q': {'_id': 5.0}, 'u': {'$set': {'category_name': 'Erkek Giyim', 'description': 'Erkek giyim Ã¼rÃ¼nleri', 'parent_category_id': 4.0, 'created_at': '2025-12-28T11:48:21'}}, 'multi': False, 'upsert': True}}, {'index': 5, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.categories index: category_id_1 dup key: { category_id: null }', 'keyPattern': {'category_id': 1}, 'keyValue': {'category_id': None}, 'op': {'q': {'_id': 6.0}, 'u': {'$set': {'category_name': 'KadÄ±n Giyim', 'description': 'KadÄ±n giyim Ã¼rÃ¼nleri', 'parent_category_id': 4.0, 'created_at': '2025-12-28T11:48:21'}}, 'multi': False, 'upsert': True}}], 'writeConcernErrors': [], 'nInserted': 0, 'nUpserted': 0, 'nMatched': 1, 'nModified': 0, 'nRemoved': 0, 'upserted': []}
2. order_items tablosu aktarım hatası: batch op errors occurred, full error: {'writeErrors': [{'index': 1, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.order_items index: order_item_id_1 dup key: { order_item_id: null }', 'keyPattern': {'order_item_id': 1}, 'keyValue': {'order_item_id': None}, 'op': {'q': {'_id': 2.0}, 'u': {'$set': {'order_id': 2.0, 'product_id': 6.0, 'quantity': 1.0, 'unit_price': 500.0, 'subtotal': 500.0}}, 'multi': False, 'upsert': True}}, {'index': 2, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.order_items index: order_item_id_1 dup key: { order_item_id: null }', 'keyPattern': {'order_item_id': 1}, 'keyValue': {'order_item_id': None}, 'op': {'q': {'_id': 3.0}, 'u': {'$set': {'order_id': 3.0, 'product_id': 2.0, 'quantity': 1.0, 'unit_price': 45000.0, 'subtotal': 45000.0}}, 'multi': False, 'upsert': True}}, {'index': 3, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.order_items index: order_item_id_1 dup key: { order_item_id: null }', 'keyPattern': {'order_item_id': 1}, 'keyValue': {'order_item_id': None}, 'op': {'q': {'_id': 4.0}, 'u': {'$set': {'order_id': 4.0, 'product_id': 4.0, 'quantity': 1.0, 'unit_price': 150.0, 'subtotal': 150.0}}, 'multi': False, 'upsert': True}}, {'index': 4, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.order_items index: order_item_id_1 dup key: { order_item_id: null }', 'keyPattern': {'order_item_id': 1}, 'keyValue': {'order_item_id': None}, 'op': {'q': {'_id': 5.0}, 'u': {'$set': {'order_id': 5.0, 'product_id': 5.0, 'quantity': 1.0, 'unit_price': 350.0, 'subtotal': 350.0}}, 'multi': False, 'upsert': True}}], 'writeConcernErrors': [], 'nInserted': 0, 'nUpserted': 0, 'nMatched': 1, 'nModified': 0, 'nRemoved': 0, 'upserted': []}
3. orders tablosu aktarım hatası: batch op errors occurred, full error: {'writeErrors': [{'index': 1, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.orders index: order_id_1 dup key: { order_id: null }', 'keyPattern': {'order_id': 1}, 'keyValue': {'order_id': None}, 'op': {'q': {'_id': 2.0}, 'u': {'$set': {'user_id': 1.0, 'order_date': '2025-12-28T11:48:21', 'total_amount': 500.0, 'status': 'shipped', 'shipping_address': 'Ä°stanbul, KadÄ±kÃ¶y, Moda Caddesi No:123', 'notes': None}}, 'multi': False, 'upsert': True}}, {'index': 2, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.orders index: order_id_1 dup key: { order_id: null }', 'keyPattern': {'order_id': 1}, 'keyValue': {'order_id': None}, 'op': {'q': {'_id': 3.0}, 'u': {'$set': {'user_id': 2.0, 'order_date': '2025-12-28T11:48:21', 'total_amount': 45000.0, 'status': 'processing', 'shipping_address': 'Ankara, Ã‡ankaya, KÄ±zÄ±lay Mahallesi No:456', 'notes': None}}, 'multi': False, 'upsert': True}}, {'index': 3, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.orders index: order_id_1 dup key: { order_id: null }', 'keyPattern': {'order_id': 1}, 'keyValue': {'order_id': None}, 'op': {'q': {'_id': 4.0}, 'u': {'$set': {'user_id': 3.0, 'order_date': '2025-12-28T11:48:21', 'total_amount': 150.0, 'status': 'pending', 'shipping_address': 'Ä°zmir, Konak, Alsancak Caddesi No:789', 'notes': None}}, 'multi': False, 'upsert': True}}, {'index': 4, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.orders index: order_id_1 dup key: { order_id: null }', 'keyPattern': {'order_id': 1}, 'keyValue': {'order_id': None}, 'op': {'q': {'_id': 5.0}, 'u': {'$set': {'user_id': 2.0, 'order_date': '2025-12-28T11:48:21', 'total_amount': 350.0, 'status': 'delivered', 'shipping_address': 'Ankara, Ã‡ankaya, KÄ±zÄ±lay Mahallesi No:456', 'notes': None}}, 'multi': False, 'upsert': True}}], 'writeConcernErrors': [], 'nInserted': 0, 'nUpserted': 0, 'nMatched': 1, 'nModified': 0, 'nRemoved': 0, 'upserted': []}
4. payments tablosu aktarım hatası: batch op errors occurred, full error: {'writeErrors': [{'index': 1, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.payments index: payment_id_1 dup key: { payment_id: null }', 'keyPattern': {'payment_id': 1}, 'keyValue': {'payment_id': None}, 'op': {'q': {'_id': 2.0}, 'u': {'$set': {'order_id': 2.0, 'payment_method': 'credit_card', 'amount': 500.0, 'payment_date': '2024-01-20T14:20:00', 'status': 'completed', 'transaction_id': 'TXN-002-2024'}}, 'multi': False, 'upsert': True}}, {'index': 2, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.payments index: payment_id_1 dup key: { payment_id: null }', 'keyPattern': {'payment_id': 1}, 'keyValue': {'payment_id': None}, 'op': {'q': {'_id': 3.0}, 'u': {'$set': {'order_id': 3.0, 'payment_method': 'bank_transfer', 'amount': 45000.0, 'payment_date': '2024-01-25T09:15:00', 'status': 'pending', 'transaction_id': 'TXN-003-2024'}}, 'multi': False, 'upsert': True}}, {'index': 3, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.payments index: payment_id_1 dup key: { payment_id: null }', 'keyPattern': {'payment_id': 1}, 'keyValue': {'payment_id': None}, 'op': {'q': {'_id': 4.0}, 'u': {'$set': {'order_id': 4.0, 'payment_method': 'credit_card', 'amount': 150.0, 'payment_date': '2024-01-28T16:45:00', 'status': 'pending', 'transaction_id': 'TXN-004-2024'}}, 'multi': False, 'upsert': True}}, {'index': 4, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.payments index: payment_id_1 dup key: { payment_id: null }', 'keyPattern': {'payment_id': 1}, 'keyValue': {'payment_id': None}, 'op': {'q': {'_id': 5.0}, 'u': {'$set': {'order_id': 5.0, 'payment_method': 'debit_card', 'amount': 350.0, 'payment_date': '2024-01-30T11:30:00', 'status': 'completed', 'transaction_id': 'TXN-005-2024'}}, 'multi': False, 'upsert': True}}], 'writeConcernErrors': [], 'nInserted': 0, 'nUpserted': 0, 'nMatched': 1, 'nModified': 0, 'nRemoved': 0, 'upserted': []}
5. products tablosu aktarım hatası: batch op errors occurred, full error: {'writeErrors': [{'index': 1, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.products index: product_id_1 dup key: { product_id: null }', 'keyPattern': {'product_id': 1}, 'keyValue': {'product_id': None}, 'op': {'q': {'_id': 2.0}, 'u': {'$set': {'product_name': 'iPhone 15 Pro', 'description': 'Apple iPhone 15 Pro 256GB', 'category_id': 3.0, 'price': 45000.0, 'stock_quantity': 5.0, 'sku': 'PHN-IPH-15PRO', 'created_at': '2025-12-28T11:48:21', 'updated_at': '2025-12-28T11:48:21'}}, 'multi': False, 'upsert': True}}, {'index': 2, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.products index: product_id_1 dup key: { product_id: null }', 'keyPattern': {'product_id': 1}, 'keyValue': {'product_id': None}, 'op': {'q': {'_id': 3.0}, 'u': {'$set': {'product_name': 'Samsung Galaxy S24', 'description': 'Samsung Galaxy S24 Ultra', 'category_id': 3.0, 'price': 40000.0, 'stock_quantity': 8.0, 'sku': 'PHN-SAM-S24', 'created_at': '2025-12-28T11:48:21', 'updated_at': '2025-12-28T11:48:21'}}, 'multi': False, 'upsert': True}}, {'index': 3, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.products index: product_id_1 dup key: { product_id: null }', 'keyPattern': {'product_id': 1}, 'keyValue': {'product_id': None}, 'op': {'q': {'_id': 4.0}, 'u': {'$set': {'product_name': 'Erkek TiÅŸÃ¶rt', 'description': 'Pamuklu erkek tiÅŸÃ¶rt', 'category_id': 5.0, 'price': 150.0, 'stock_quantity': 50.0, 'sku': 'CLT-M-TSHIRT', 'created_at': '2025-12-28T11:48:21', 'updated_at': '2025-12-28T11:48:21'}}, 'multi': False, 'upsert': True}}, {'index': 4, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.products index: product_id_1 dup key: { product_id: null }', 'keyPattern': {'product_id': 1}, 'keyValue': {'product_id': None}, 'op': {'q': {'_id': 5.0}, 'u': {'$set': {'product_name': 'KadÄ±n Elbise', 'description': 'YazlÄ±k kadÄ±n elbise', 'category_id': 6.0, 'price': 350.0, 'stock_quantity': 30.0, 'sku': 'CLT-F-DRESS', 'created_at': '2025-12-28T11:48:21', 'updated_at': '2025-12-28T11:48:21'}}, 'multi': False, 'upsert': True}}, {'index': 5, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.products index: product_id_1 dup key: { product_id: null }', 'keyPattern': {'product_id': 1}, 'keyValue': {'product_id': None}, 'op': {'q': {'_id': 6.0}, 'u': {'$set': {'product_name': 'Gaming Mouse', 'description': 'RGB aydÄ±nlatmalÄ± gaming mouse', 'category_id': 2.0, 'price': 500.0, 'stock_quantity': 25.0, 'sku': 'ACC-MOUSE-GM', 'created_at': '2025-12-28T11:48:21', 'updated_at': '2025-12-28T11:48:21'}}, 'multi': False, 'upsert': True}}, {'index': 6, 'code': 11000, 'errmsg': 'Plan executor error during update :: caused by :: E11000 duplicate key error collection: migrated_database.products index: product_id_1 dup key: { product_id: null }', 'keyPattern': {'product_id': 1}, 'keyValue': {'product_id': None}, 'op': {'q': {'_id': 7.0}, 'u': {'$set': {'product_name': 'Klavye Mekanik', 'description': 'Mekanik klavye RGB', 'category_id': 2.0, 'price': 1200.0, 'stock_quantity': 15.0, 'sku': 'ACC-KEY-MECH', 'created_at': '2025-12-28T11:48:21', 'updated_at': '2025-12-28T11:48:21'}}, 'multi': False, 'upsert': True}}], 'writeConcernErrors': [], 'nInserted': 0, 'nUpserted': 0, 'nMatched': 1, 'nModified': 0, 'nRemoved': 0, 'upserted': []}
6. users tablosu aktarım hatası: cannot encode object: datetime.date(1990, 5, 15), of type: <class 'datetime.date'>

### Genel Problemler ve Çözümler

#### 1. Veri Tipi Uyumsuzlukları

**Problem:** Bazı SQL veri tipleri MongoDB'de doğrudan karşılık bulmaz.

**Çözüm:** Veri tipleri uygun MongoDB BSON tiplerine dönüştürülmüştür:
- DATETIME → ISO 8601 string formatı
- DECIMAL → Double
- ENUM → String

#### 2. İlişkisel Veri Yapısı

**Problem:** SQL ilişkisel model, MongoDB dokümantasyon modelinden farklıdır.

**Çözüm:** İlişkiler referans veya embedded document olarak saklanabilir:
- One-to-Many: Referans kullanılabilir
- Many-to-Many: Referans dizisi kullanılabilir
- Küçük ilişkili veriler: Embedded document olarak saklanabilir

#### 3. Transaction Desteği

**Problem:** MongoDB'de multi-document transaction'lar sınırlıdır.

**Çözüm:** MongoDB 4.0+ sürümlerinde transaction desteği mevcuttur.
Kritik işlemler için transaction kullanılmalıdır.

## Migration İstatistikleri

- **Aktarılan Tablo Sayısı:** 0
- **Aktarılan Belge Sayısı:** 0
- **Toplam Süre:** 0.01 saniye
- **Hata Sayısı:** 6

## MongoDB Bağlantı Bilgileri

- **Host:** localhost
- **Port:** 27017
- **Database:** migrated_database

---

*Bu rapor otomatik olarak oluşturulmuştur.*
