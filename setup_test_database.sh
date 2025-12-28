#!/bin/bash

# Test Veritabanı Kurulum Scripti
# Bu script test veritabanını oluşturur ve örnek verileri ekler

echo "=========================================="
echo "Test Veritabanı Kurulumu"
echo "=========================================="
echo ""

# MySQL kullanıcı bilgilerini sor
read -p "MySQL kullanıcı adı (varsayılan: root): " MYSQL_USER
MYSQL_USER=${MYSQL_USER:-root}

read -sp "MySQL şifresi: " MYSQL_PASS
echo ""

# MySQL'e bağlan ve test veritabanını oluştur
echo ""
echo "Test veritabanı oluşturuluyor..."

if [ -z "$MYSQL_PASS" ]; then
    mysql -u "$MYSQL_USER" < test_database.sql
else
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" < test_database.sql
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Test veritabanı başarıyla oluşturuldu!"
    echo "=========================================="
    echo ""
    echo "Veritabanı: ecommerce_test"
    echo "Tablolar:"
    echo "  - users (4 kayıt)"
    echo "  - categories (6 kayıt)"
    echo "  - products (7 kayıt)"
    echo "  - orders (5 kayıt)"
    echo "  - order_items (5 kayıt)"
    echo "  - payments (5 kayıt)"
    echo ""
    echo "Trigger'ler: 4 adet"
    echo "Stored Procedure'ler: 5 adet"
    echo "Function'lar: 3 adet"
    echo "View'ler: 3 adet"
    echo ""
    echo "Şimdi config.yaml dosyasını düzenleyip uygulamayı çalıştırabilirsiniz:"
    echo "  python main.py"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ Hata! Veritabanı oluşturulamadı"
    echo "=========================================="
    echo ""
    echo "Olası nedenler:"
    echo "1. MySQL kullanıcı adı veya şifresi yanlış"
    echo "2. MySQL sunucusu çalışmıyor"
    echo "3. Kullanıcının veritabanı oluşturma yetkisi yok"
    echo ""
fi

