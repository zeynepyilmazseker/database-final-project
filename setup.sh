#!/bin/bash

# Database Migration Tool - Setup Script
# Bu script, projeyi çalıştırmak için gerekli ortamı hazırlar

echo "=========================================="
echo "Database Migration Tool - Kurulum"
echo "=========================================="
echo ""

# Python versiyonunu kontrol et
echo "Python versiyonu kontrol ediliyor..."
python3 --version

# Virtual environment oluştur (opsiyonel)
read -p "Virtual environment oluşturulsun mu? (y/n): " create_venv
if [ "$create_venv" = "y" ]; then
    echo "Virtual environment oluşturuluyor..."
    python3 -m venv venv
    echo "Virtual environment aktifleştiriliyor..."
    source venv/bin/activate
fi

# Gerekli paketleri yükle
echo ""
echo "Gerekli paketler yükleniyor..."
pip install -r requirements.txt

# Dizinleri oluştur
echo ""
echo "Gerekli dizinler oluşturuluyor..."
mkdir -p logs
mkdir -p reports

# Config dosyasını kontrol et
echo ""
if [ ! -f "config.yaml" ]; then
    echo "UYARI: config.yaml dosyası bulunamadı!"
    echo "Lütfen config.yaml dosyasını oluşturun ve düzenleyin."
else
    echo "config.yaml dosyası bulundu."
fi

echo ""
echo "=========================================="
echo "Kurulum tamamlandı!"
echo "=========================================="
echo ""
echo "Kullanım:"
echo "1. config.yaml dosyasını düzenleyin"
echo "2. python main.py komutu ile uygulamayı çalıştırın"
echo ""

