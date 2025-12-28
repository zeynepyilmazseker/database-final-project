#!/bin/bash

# Test Verilerini Yükleme Scripti
# Bu script, mevcut test_db veritabanına test verilerini yükler

echo "=========================================="
echo "Test Verileri Yükleme"
echo "=========================================="
echo ""

# MySQL kullanıcı bilgilerini sor
read -p "MySQL kullanıcı adı (varsayılan: root): " MYSQL_USER
MYSQL_USER=${MYSQL_USER:-root}

read -sp "MySQL şifresi: " MYSQL_PASS
echo ""

# Veritabanının var olup olmadığını kontrol et
echo ""
echo "test_db veritabanı kontrol ediliyor..."

if [ -z "$MYSQL_PASS" ]; then
    DB_EXISTS=$(mysql -u "$MYSQL_USER" -e "SHOW DATABASES LIKE 'test_db';" | grep test_db)
else
    DB_EXISTS=$(mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -e "SHOW DATABASES LIKE 'test_db';" | grep test_db)
fi

if [ -z "$DB_EXISTS" ]; then
    echo ""
    echo "⚠️  UYARI: test_db veritabanı bulunamadı!"
    echo ""
    read -p "test_db veritabanını oluşturmak ister misiniz? (y/n): " CREATE_DB
    
    if [ "$CREATE_DB" = "y" ]; then
        if [ -z "$MYSQL_PASS" ]; then
            mysql -u "$MYSQL_USER" -e "CREATE DATABASE test_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        else
            mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -e "CREATE DATABASE test_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        fi
        echo "✅ test_db veritabanı oluşturuldu."
    else
        echo "❌ İşlem iptal edildi."
        exit 1
    fi
fi

echo ""
echo "Test verileri yükleniyor..."

# SQL dosyasını yükle (USE test_db zaten dosyada var)
if [ -z "$MYSQL_PASS" ]; then
    mysql -u "$MYSQL_USER" test_db < test_database.sql
else
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" test_db < test_database.sql
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Test verileri başarıyla yüklendi!"
    echo "=========================================="
    echo ""
    echo "Veritabanı: test_db"
    echo ""
    echo "Yüklenen içerik:"
    echo "  ✅ 7 Tablo"
    echo "  ✅ 4 Trigger"
    echo "  ✅ 5 Stored Procedure"
    echo "  ✅ 3 Function"
    echo "  ✅ 3 View"
    echo "  ✅ 32 Örnek Kayıt"
    echo ""
    echo "Şimdi uygulamayı çalıştırabilirsiniz:"
    echo "  python main.py"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ Hata! Veriler yüklenemedi"
    echo "=========================================="
    echo ""
    echo "Olası nedenler:"
    echo "1. Tablolar zaten mevcut (DROP TABLE ekleyebilirsiniz)"
    echo "2. MySQL kullanıcı adı veya şifresi yanlış"
    echo "3. Kullanıcının CREATE/DROP yetkisi yok"
    echo ""
    echo "Çözüm:"
    echo "Mevcut tabloları silmek için:"
    echo "  mysql -u root -p test_db -e 'DROP DATABASE test_db; CREATE DATABASE test_db;'"
    echo ""
fi

