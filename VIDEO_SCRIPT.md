# Video Sunum Scripti - SQL → MongoDB Migration Tool

## 🎬 Video İçeriği (10 Dakika)

### 1. Giriş (30 saniye)

"Merhaba, bugün sizlere final projem olan SQL'den MongoDB'ye otomatik veri aktarım uygulamasını tanıtacağım. Bu uygulama, MySQL veya MSSQL veritabanlarından MongoDB'ye dinamik olarak veri ve şema aktarımı yapıyor."

### 2. Proje Amacı ve Özellikler (1 dakika)

"Projenin temel amacı:
- Sadece connection string bilgileriyle veritabanına bağlanmak
- Veritabanı şemasını otomatik keşfetmek
- Tüm yapısal bileşenleri tespit etmek
- Verileri MongoDB'ye aktarmak
- Dönüştürülemeyen yapılar için çözüm önerileri sunmak

Özellikler:
- MySQL ve MSSQL desteği
- Dinamik şema keşfi
- İdempotent çalışma (tekrar çalıştırılabilir)
- Detaylı hata loglama
- Teknik rapor oluşturma"

### 3. Proje Yapısı (1 dakika)

"Proje modüler bir yapıda tasarlanmış:
- Database modülü: SQL ve MongoDB bağlantıları, şema keşfi
- Migration modülü: Veri aktarım işlemleri
- Reporting modülü: Teknik rapor oluşturma

Tüm kod Türkçe yorumlarla yazılmış ve GitHub'da paylaşılmıştır."

### 4. Demo - Test Veritabanı (2 dakika)

"Şimdi test veritabanımızı görelim. MySQL'de e-ticaret sistemine ait bir test veritabanı hazırladım. Bu veritabanında:
- 6 tablo
- Foreign key ilişkileri
- 4 trigger
- 5 stored procedure
- 3 function
- 3 view
- 32 örnek kayıt bulunuyor."

[Terminal'de MySQL'e bağlan ve tabloları göster]

### 5. Demo - Migration Çalıştırma (2 dakika)

"Şimdi migration uygulamasını çalıştıralım. Config dosyasında veritabanı bilgileri zaten ayarlanmış durumda."

[Terminal'de uygulamayı çalıştır]

"Gördüğünüz gibi:
- Veritabanına bağlandı
- Şemayı keşfetti
- 6 tablo, 4 trigger, 5 SP, 3 function tespit etti
- Verileri MongoDB'ye aktardı
- 32 belge başarıyla aktarıldı
- Detaylı rapor oluşturuldu"

### 6. MongoDB'de Sonuçları Gösterme (1.5 dakika)

"MongoDB'de sonuçları kontrol edelim."

[Terminal'de MongoDB'ye bağlan ve collection'ları göster]

"Gördüğünüz gibi:
- 6 collection oluşturuldu
- Her collection'da veriler mevcut
- Primary key'ler _id olarak saklandı
- Index'ler oluşturuldu"

### 7. Teknik Rapor (1.5 dakika)

"Oluşturulan teknik raporu görelim. Raporda:
- Keşif süreci detayları
- Tespit edilen tüm nesneler
- Dönüştürülen yapılar
- Dönüştürülemeyen yapılar ve çözüm önerileri
- Migration istatistikleri

Özellikle dikkat çekmek istediğim nokta: Trigger'ler, stored procedure'ler ve function'lar MongoDB'de doğrudan desteklenmediği için rapor içinde bunların nasıl çözülebileceğine dair detaylı öneriler sunuluyor."

[Rapor dosyasını aç ve önemli bölümleri göster]

### 8. İdempotent Çalışma (1 dakika)

"Projenin önemli özelliklerinden biri idempotent çalışması. Yani aynı migration'ı tekrar çalıştırabilirsiniz. MongoDB'deki veritabanını silsem bile, uygulamayı tekrar çalıştırdığımda aynı veritabanı ve veriler oluşturulur. Bunu göstereyim:"

[MongoDB veritabanını sil ve tekrar çalıştır]

"Gördüğünüz gibi, aynı sonuçlar elde edildi. Bu, production ortamında güvenli bir şekilde migration'ı tekrar çalıştırabileceğiniz anlamına gelir."

### 9. Sonuç ve Özet (30 saniye)

"Özetlemek gerekirse:
- Proje dinamik olarak herhangi bir MySQL/MSSQL veritabanını MongoDB'ye dönüştürebilir
- Tüm şema bileşenleri otomatik keşfedilir
- Dönüştürülemeyen yapılar için çözüm önerileri sunulur
- Detaylı teknik rapor oluşturulur
- İdempotent çalışma sayesinde güvenli bir şekilde tekrar çalıştırılabilir

Proje GitHub'da paylaşılmıştır ve tüm kaynak kodlar açık kaynaklıdır. Teşekkürler!"

---

## 📝 Video Çekimi İçin Notlar

- Her bölüm arasında 2-3 saniye duraklama yapın
- Terminal ekranını büyük ve net gösterin
- Kod yazarken yavaş ve açıklayıcı olun
- Hata durumlarında ne yapılacağını gösterin
- Rapor dosyasını açarken önemli bölümleri vurgulayın

