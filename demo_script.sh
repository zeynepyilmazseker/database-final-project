#!/bin/bash

# Video Demo Script
# Bu script video çekimi için tüm adımları otomatik olarak gösterir

echo "=========================================="
echo "SQL → MongoDB Migration Tool - Demo"
echo "=========================================="
echo ""

# Renkler
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Proje Yapısı
echo -e "${BLUE}1. Proje Yapısı${NC}"
echo "-------------------"
ls -la src/
echo ""

# 2. MySQL Kontrol
echo -e "${BLUE}2. MySQL Test Veritabanı Kontrolü${NC}"
echo "-------------------"
mysql -u root -p5545228936Zm. test_db -e "SHOW TABLES;" 2>/dev/null
echo ""

# 3. MySQL İstatistikler
echo -e "${BLUE}3. MySQL Tablo İstatistikleri${NC}"
echo "-------------------"
mysql -u root -p5545228936Zm. test_db -e "
SELECT 
    'users' as tablo, COUNT(*) as kayit FROM users
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'categories', COUNT(*) FROM categories
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'payments', COUNT(*) FROM payments;
" 2>/dev/null
echo ""

# 4. MongoDB'yi Temizle (isteğe bağlı)
read -p "MongoDB'deki migrated_database'i silmek ister misiniz? (y/n): " CLEAN_DB
if [ "$CLEAN_DB" = "y" ]; then
    echo -e "${YELLOW}MongoDB veritabanı siliniyor...${NC}"
    python3 -c "from pymongo import MongoClient; client = MongoClient('localhost', 27017); client.drop_database('migrated_database'); print('✅ Veritabanı silindi')" 2>/dev/null
    echo ""
fi

# 5. Migration Çalıştır
echo -e "${BLUE}4. Migration Başlatılıyor...${NC}"
echo "-------------------"
source venv/bin/activate
python main.py
echo ""

# 6. MongoDB Sonuçları
echo -e "${BLUE}5. MongoDB Sonuçları${NC}"
echo "-------------------"
python3 -c "
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['migrated_database']
print('Collections:', db.list_collection_names())
print('')
for col in db.list_collection_names():
    count = db[col].count_documents({})
    print(f'{col}: {count} documents')
" 2>/dev/null
echo ""

# 7. Örnek Belge
echo -e "${BLUE}6. Örnek Belge (users collection)${NC}"
echo "-------------------"
python3 -c "
from pymongo import MongoClient
import json
client = MongoClient('localhost', 27017)
db = client['migrated_database']
user = db.users.find_one()
print(json.dumps(user, indent=2, default=str))
" 2>/dev/null
echo ""

# 8. Rapor Bilgisi
echo -e "${BLUE}7. Oluşturulan Rapor${NC}"
echo "-------------------"
LATEST_REPORT=$(ls -t reports/*.md 2>/dev/null | head -1)
if [ -n "$LATEST_REPORT" ]; then
    echo "Rapor: $LATEST_REPORT"
    echo ""
    echo "İstatistikler:"
    grep -A 5 "Migration İstatistikleri" "$LATEST_REPORT" | head -6
else
    echo "Rapor bulunamadı"
fi
echo ""

echo -e "${GREEN}=========================================="
echo "Demo Tamamlandı!"
echo "==========================================${NC}"

