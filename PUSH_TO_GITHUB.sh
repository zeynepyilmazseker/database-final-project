#!/bin/bash

# GitHub'a Push Script
# Bu script, projeyi GitHub'a yüklemek için kullanılır

echo "=========================================="
echo "GitHub'a Push İşlemi"
echo "=========================================="
echo ""

# GitHub kullanıcı adı
GITHUB_USER="zeynepyilmazseker"

# Repository ismini sor
read -p "GitHub repository ismini girin (örn: database-final-project): " REPO_NAME

if [ -z "$REPO_NAME" ]; then
    echo "HATA: Repository ismi boş olamaz!"
    exit 1
fi

echo ""
echo "Repository: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""

# Remote ekle (eğer yoksa)
if git remote get-url origin > /dev/null 2>&1; then
    echo "Remote 'origin' zaten mevcut. Güncelleniyor..."
    git remote set-url origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
else
    echo "Remote 'origin' ekleniyor..."
    git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
fi

# Branch'i main olarak ayarla
git branch -M main

echo ""
echo "GitHub'a push ediliyor..."
echo "NOT: İlk push'ta GitHub kullanıcı adı ve şifre (veya token) istenebilir."
echo ""

# Push yap
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Başarılı! Proje GitHub'a yüklendi."
    echo "=========================================="
    echo ""
    echo "Repository URL: https://github.com/$GITHUB_USER/$REPO_NAME"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ Push işlemi başarısız oldu!"
    echo "=========================================="
    echo ""
    echo "Olası nedenler:"
    echo "1. GitHub'da repository oluşturulmamış olabilir"
    echo "2. Authentication hatası olabilir"
    echo "3. İnternet bağlantısı sorunu olabilir"
    echo ""
    echo "Çözüm:"
    echo "1. https://github.com/new adresinden repository oluşturun"
    echo "2. Personal Access Token kullanın (Settings > Developer settings > Personal access tokens)"
    echo ""
fi

