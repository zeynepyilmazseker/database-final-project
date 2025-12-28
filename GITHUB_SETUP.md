# GitHub Repository Kurulum Talimatları

## 1. GitHub'da Yeni Repository Oluşturun

1. GitHub'a giriş yapın: https://github.com
2. Sağ üstteki "+" butonuna tıklayın
3. "New repository" seçin
4. Repository bilgilerini doldurun:
   - **Repository name**: `database-final-project` (veya istediğiniz isim)
   - **Description**: "SQL to MongoDB Migration Tool - Final Project"
   - **Visibility**: Public veya Private (tercihinize göre)
   - **Initialize repository**: ❌ Boş bırakın (README, .gitignore eklemeyin)
5. "Create repository" butonuna tıklayın

## 2. Local Repository'yi GitHub'a Bağlayın

Terminal'de aşağıdaki komutları çalıştırın:

```bash
# Remote repository ekle (YOUR_REPO_NAME yerine oluşturduğunuz repo ismini yazın)
git remote add origin https://github.com/zeynepyilmazseker/YOUR_REPO_NAME.git

# Branch'i main olarak değiştir (GitHub'ın varsayılan branch ismi)
git branch -M main

# İlk push
git push -u origin main
```

## 3. Alternatif: SSH Kullanıyorsanız

```bash
git remote add origin git@github.com:zeynepyilmazseker/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## 4. Sonraki Değişiklikler İçin

```bash
git add .
git commit -m "Değişiklik açıklaması"
git push
```

## Notlar

- İlk push'tan önce GitHub'da repository oluşturmanız gerekiyor
- Repository ismini `YOUR_REPO_NAME` yerine gerçek isimle değiştirmeyi unutmayın
- Eğer authentication sorunu yaşarsanız, GitHub Personal Access Token kullanmanız gerekebilir

