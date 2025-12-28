"""
Report Generator Module
Migration sürecini ve sonuçlarını raporlar.
Teknik rapor oluşturur.
"""

import logging
import os
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Rapor oluşturucu sınıfı.
    Migration sürecini ve sonuçlarını detaylı raporlar.
    """
    
    def __init__(self, output_dir: str = "reports", format: str = "markdown"):
        """
        Rapor oluşturucu sınıfını başlatır.
        
        Args:
            output_dir: Raporların kaydedileceği dizin
            format: Rapor formatı ("markdown" veya "html")
        """
        self.output_dir = output_dir
        self.format = format.lower()
        
        # Output dizinini oluştur
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_report(self, schema_info: Dict[str, Any], 
                       migration_stats: Dict[str, Any],
                       sql_config: Dict[str, Any],
                       mongodb_config: Dict[str, Any]) -> str:
        """
        Tam teknik rapor oluşturur.
        
        Args:
            schema_info: Keşfedilen şema bilgileri
            migration_stats: Migration istatistikleri
            sql_config: SQL veritabanı konfigürasyonu
            mongodb_config: MongoDB konfigürasyonu
            
        Returns:
            str: Oluşturulan rapor dosyasının yolu
        """
        logger.info("Teknik rapor oluşturuluyor...")
        
        if self.format == "markdown":
            return self._generate_markdown_report(
                schema_info, migration_stats, sql_config, mongodb_config
            )
        elif self.format == "html":
            return self._generate_html_report(
                schema_info, migration_stats, sql_config, mongodb_config
            )
        else:
            raise ValueError(f"Desteklenmeyen format: {self.format}")
    
    def _generate_markdown_report(self, schema_info: Dict[str, Any],
                                  migration_stats: Dict[str, Any],
                                  sql_config: Dict[str, Any],
                                  mongodb_config: Dict[str, Any]) -> str:
        """
        Markdown formatında rapor oluşturur.
        
        Returns:
            str: Rapor dosyası yolu
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"migration_report_{timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# SQL → MongoDB Migration Teknik Raporu\n\n")
            f.write(f"**Oluşturulma Tarihi:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            # 1. Veritabanı Keşif Süreci
            f.write("## 1. Veritabanı Keşif Süreci\n\n")
            f.write("### Bağlantı Bilgileri\n\n")
            f.write(f"- **Veritabanı Tipi:** {sql_config.get('type', 'N/A').upper()}\n")
            f.write(f"- **Host:** {sql_config.get('host', 'N/A')}\n")
            f.write(f"- **Port:** {sql_config.get('port', 'N/A')}\n")
            f.write(f"- **Database:** {sql_config.get('database', 'N/A')}\n")
            f.write(f"- **Username:** {sql_config.get('username', 'N/A')}\n\n")
            
            f.write("### Keşif Metodolojisi\n\n")
            f.write("Veritabanı şeması aşağıdaki adımlarla keşfedilmiştir:\n\n")
            f.write("1. SQLAlchemy Inspector kullanılarak tablo listesi alındı\n")
            f.write("2. Her tablo için kolon bilgileri, veri tipleri ve özellikler tespit edildi\n")
            f.write("3. Primary Key ve Foreign Key ilişkileri analiz edildi\n")
            f.write("4. Index'ler ve constraint'ler keşfedildi\n")
            f.write("5. Trigger'ler ve stored procedure'ler tespit edildi\n")
            f.write("6. View'ler ve function'lar analiz edildi\n\n")
            
            # 2. Tespit Edilen Nesnelerin Listesi
            f.write("## 2. Tespit Edilen Nesnelerin Listesi\n\n")
            
            tables = schema_info.get('tables', [])
            f.write(f"### Tablolar ({len(tables)})\n\n")
            for table in tables:
                f.write(f"- `{table}`\n")
            f.write("\n")
            
            columns = schema_info.get('columns', {})
            f.write("### Kolonlar ve Veri Tipleri\n\n")
            for table_name, cols in columns.items():
                f.write(f"#### Tablo: `{table_name}`\n\n")
                f.write("| Kolon | Tip | Nullable | Default |\n")
                f.write("|-------|-----|----------|----------|\n")
                for col in cols:
                    f.write(f"| {col['name']} | {col['type']} | "
                           f"{'Evet' if col['nullable'] else 'Hayır'} | "
                           f"{col.get('default', '')} |\n")
                f.write("\n")
            
            primary_keys = schema_info.get('primary_keys', {})
            f.write("### Primary Key'ler\n\n")
            for table_name, pk_cols in primary_keys.items():
                f.write(f"- **{table_name}:** {', '.join(pk_cols)}\n")
            f.write("\n")
            
            foreign_keys = schema_info.get('foreign_keys', {})
            f.write("### Foreign Key'ler\n\n")
            for table_name, fks in foreign_keys.items():
                if fks:
                    f.write(f"#### Tablo: `{table_name}`\n\n")
                    for fk in fks:
                        f.write(f"- **{fk.get('name', 'N/A')}:** "
                               f"{', '.join(fk.get('constrained_columns', []))} → "
                               f"{fk.get('referred_table', 'N/A')}."
                               f"{', '.join(fk.get('referred_columns', []))}\n")
                    f.write("\n")
            
            indexes = schema_info.get('indexes', {})
            f.write("### Index'ler\n\n")
            for table_name, idxs in indexes.items():
                if idxs:
                    f.write(f"#### Tablo: `{table_name}`\n\n")
                    for idx in idxs:
                        unique_str = " (Unique)" if idx.get('unique') else ""
                        f.write(f"- **{idx.get('name', 'N/A')}:** "
                               f"{', '.join(idx.get('columns', []))}{unique_str}\n")
                    f.write("\n")
            
            constraints = schema_info.get('constraints', {})
            f.write("### Check Constraint'ler\n\n")
            constraint_count = sum(len(v) for v in constraints.values())
            if constraint_count > 0:
                for table_name, consts in constraints.items():
                    if consts:
                        f.write(f"#### Tablo: `{table_name}`\n\n")
                        for const in consts:
                            f.write(f"- **{const.get('name', 'N/A')}:** "
                                   f"{const.get('check_clause', 'N/A')}\n")
                        f.write("\n")
            else:
                f.write("Check constraint bulunamadı.\n\n")
            
            triggers = schema_info.get('triggers', {})
            f.write("### Trigger'ler\n\n")
            trigger_count = sum(len(v) for v in triggers.values())
            if trigger_count > 0:
                for table_name, trigs in triggers.items():
                    if trigs:
                        f.write(f"#### Tablo: `{table_name}`\n\n")
                        for trig in trigs:
                            f.write(f"- **{trig.get('name', 'N/A')}:** "
                                   f"{trig.get('timing', 'N/A')} {trig.get('event', 'N/A')}\n")
                        f.write("\n")
            else:
                f.write("Trigger bulunamadı.\n\n")
            
            stored_procedures = schema_info.get('stored_procedures', [])
            f.write("### Stored Procedure'ler\n\n")
            if stored_procedures:
                for sp in stored_procedures:
                    f.write(f"- `{sp.get('name', 'N/A')}`\n")
            else:
                f.write("Stored procedure bulunamadı.\n\n")
            f.write("\n")
            
            functions = schema_info.get('functions', [])
            f.write("### Function'lar\n\n")
            if functions:
                for func in functions:
                    f.write(f"- `{func.get('name', 'N/A')}`\n")
            else:
                f.write("Function bulunamadı.\n\n")
            f.write("\n")
            
            views = schema_info.get('views', [])
            f.write("### View'ler\n\n")
            if views:
                for view in views:
                    f.write(f"- `{view.get('name', 'N/A')}`\n")
            else:
                f.write("View bulunamadı.\n\n")
            f.write("\n")
            
            # 3. MongoDB Veri Modeli
            f.write("## 3. MongoDB Veri Modeli\n\n")
            f.write("### Dönüşüm Stratejisi\n\n")
            f.write("SQL veritabanı yapıları MongoDB'ye aşağıdaki şekilde dönüştürülmüştür:\n\n")
            f.write("- **Tablolar → Collections:** Her SQL tablosu bir MongoDB collection'ına dönüştürülmüştür\n")
            f.write("- **Satırlar → Belgeler:** Her SQL satırı bir MongoDB belgesine (document) dönüştürülmüştür\n")
            f.write("- **Kolonlar → Alanlar:** SQL kolonları MongoDB belge alanlarına dönüştürülmüştür\n")
            f.write("- **Primary Key → _id:** Primary key kolonları MongoDB `_id` alanına dönüştürülmüştür\n")
            f.write("- **Foreign Key → Referans:** Foreign key ilişkileri belge içinde referans olarak saklanmıştır\n")
            f.write("- **Index'ler:** SQL index'leri MongoDB index'lerine dönüştürülmüştür\n\n")
            
            f.write("### Örnek Belge Yapısı\n\n")
            if tables:
                example_table = tables[0]
                example_cols = columns.get(example_table, [])
                if example_cols:
                    f.write(f"**Collection:** `{example_table}`\n\n")
                    f.write("```json\n{\n")
                    for i, col in enumerate(example_cols):
                        comma = "," if i < len(example_cols) - 1 else ""
                        f.write(f'  "{col["name"]}": <{col["type"]}>{comma}\n')
                    f.write("}\n```\n\n")
            
            # 4. Dönüştürülen Yapılar
            f.write("## 4. Dönüştürülen Yapılar\n\n")
            f.write("Aşağıdaki yapılar başarıyla MongoDB'ye dönüştürülmüştür:\n\n")
            f.write(f"- ✅ **Tablolar:** {len(tables)} tablo collection'a dönüştürüldü\n")
            f.write(f"- ✅ **Kolonlar:** Tüm kolonlar belge alanlarına dönüştürüldü\n")
            f.write(f"- ✅ **Primary Key'ler:** Primary key'ler `_id` alanına dönüştürüldü\n")
            f.write(f"- ✅ **Index'ler:** {sum(len(v) for v in indexes.values())} index oluşturuldu\n")
            f.write(f"- ✅ **Veri:** {migration_stats.get('total_documents', 0)} belge aktarıldı\n\n")
            
            # 5. Dönüştürülemeyen Yapılar
            f.write("## 5. Dönüştürülemeyen Yapılar ve Gerekçeleri\n\n")
            
            f.write("### Foreign Key İlişkileri\n\n")
            f.write("**Durum:** Foreign key constraint'leri MongoDB'de doğrudan desteklenmez.\n\n")
            f.write("**Çözüm Önerisi:**\n")
            f.write("- Foreign key referansları belge içinde alan olarak saklanır\n")
            f.write("- Uygulama katmanında referans bütünlüğü kontrol edilmelidir\n")
            f.write("- Gerekirse MongoDB'de referans kontrolü için validation kuralları eklenebilir\n\n")
            
            f.write("### Check Constraint'ler\n\n")
            constraint_count = sum(len(v) for v in constraints.values())
            if constraint_count > 0:
                f.write("**Durum:** Check constraint'ler MongoDB'de doğrudan desteklenmez.\n\n")
                f.write("**Çözüm Önerisi:**\n")
                f.write("- MongoDB 3.6+ sürümlerinde JSON Schema validation kullanılabilir\n")
                f.write("- Uygulama katmanında veri doğrulama yapılmalıdır\n")
                f.write("- Mongoose (Node.js) veya Pydantic (Python) gibi ODM/ORM araçları kullanılabilir\n\n")
            else:
                f.write("Check constraint bulunmadığı için dönüşüm gerekmedi.\n\n")
            
            f.write("### Trigger'ler\n\n")
            trigger_count = sum(len(v) for v in triggers.values())
            if trigger_count > 0:
                f.write("**Durum:** Trigger'ler MongoDB'de doğrudan desteklenmez.\n\n")
                f.write("**Çözüm Önerisi:**\n")
                f.write("- MongoDB Change Streams kullanılarak değişiklikler izlenebilir\n")
                f.write("- Uygulama katmanında event-driven mimari kullanılabilir\n")
                f.write("- MongoDB Realm Functions veya serverless functions kullanılabilir\n\n")
            else:
                f.write("Trigger bulunmadığı için dönüşüm gerekmedi.\n\n")
            
            f.write("### Stored Procedure'ler\n\n")
            if stored_procedures:
                f.write("**Durum:** Stored procedure'ler MongoDB'de doğrudan desteklenmez.\n\n")
                f.write("**Çözüm Önerisi:**\n")
                f.write("- Stored procedure mantığı uygulama katmanına taşınmalıdır\n")
                f.write("- MongoDB'de aggregation pipeline'lar kullanılabilir\n")
                f.write("- MongoDB Realm Functions veya serverless functions kullanılabilir\n")
                f.write("- Uygulama kodunda fonksiyonlar olarak implement edilmelidir\n\n")
            else:
                f.write("Stored procedure bulunmadığı için dönüşüm gerekmedi.\n\n")
            
            f.write("### Function'lar\n\n")
            if functions:
                f.write("**Durum:** SQL function'ları MongoDB'de doğrudan desteklenmez.\n\n")
                f.write("**Çözüm Önerisi:**\n")
                f.write("- Function mantığı uygulama katmanına taşınmalıdır\n")
                f.write("- MongoDB aggregation pipeline'lar kullanılabilir\n")
                f.write("- Uygulama kodunda fonksiyonlar olarak implement edilmelidir\n\n")
            else:
                f.write("Function bulunmadığı için dönüşüm gerekmedi.\n\n")
            
            f.write("### View'ler\n\n")
            if views:
                f.write("**Durum:** SQL view'leri MongoDB'de doğrudan desteklenmez.\n\n")
                f.write("**Çözüm Önerisi:**\n")
                f.write("- View mantığı MongoDB aggregation pipeline'larına dönüştürülebilir\n")
                f.write("- MongoDB View'leri (MongoDB 3.4+) kullanılabilir\n")
                f.write("- Uygulama katmanında sorgu fonksiyonları olarak implement edilmelidir\n\n")
            else:
                f.write("View bulunmadığı için dönüşüm gerekmedi.\n\n")
            
            # 6. Karşılaşılan Problemler ve Çözüm Önerileri
            f.write("## 6. Karşılaşılan Problemler ve Çözüm Önerileri\n\n")
            
            errors = migration_stats.get('errors', [])
            if errors:
                f.write("### Migration Sırasında Karşılaşılan Hatalar\n\n")
                for i, error in enumerate(errors, 1):
                    f.write(f"{i}. {error}\n")
                f.write("\n")
            else:
                f.write("Migration sırasında kritik hata ile karşılaşılmadı.\n\n")
            
            f.write("### Genel Problemler ve Çözümler\n\n")
            f.write("#### 1. Veri Tipi Uyumsuzlukları\n\n")
            f.write("**Problem:** Bazı SQL veri tipleri MongoDB'de doğrudan karşılık bulmaz.\n\n")
            f.write("**Çözüm:** Veri tipleri uygun MongoDB BSON tiplerine dönüştürülmüştür:\n")
            f.write("- DATETIME → ISO 8601 string formatı\n")
            f.write("- DECIMAL → Double\n")
            f.write("- ENUM → String\n\n")
            
            f.write("#### 2. İlişkisel Veri Yapısı\n\n")
            f.write("**Problem:** SQL ilişkisel model, MongoDB dokümantasyon modelinden farklıdır.\n\n")
            f.write("**Çözüm:** İlişkiler referans veya embedded document olarak saklanabilir:\n")
            f.write("- One-to-Many: Referans kullanılabilir\n")
            f.write("- Many-to-Many: Referans dizisi kullanılabilir\n")
            f.write("- Küçük ilişkili veriler: Embedded document olarak saklanabilir\n\n")
            
            f.write("#### 3. Transaction Desteği\n\n")
            f.write("**Problem:** MongoDB'de multi-document transaction'lar sınırlıdır.\n\n")
            f.write("**Çözüm:** MongoDB 4.0+ sürümlerinde transaction desteği mevcuttur.\n")
            f.write("Kritik işlemler için transaction kullanılmalıdır.\n\n")
            
            # Migration İstatistikleri
            f.write("## Migration İstatistikleri\n\n")
            f.write(f"- **Aktarılan Tablo Sayısı:** {migration_stats.get('tables_migrated', 0)}\n")
            f.write(f"- **Aktarılan Belge Sayısı:** {migration_stats.get('total_documents', 0)}\n")
            
            start_time = migration_stats.get('start_time')
            end_time = migration_stats.get('end_time')
            if start_time and end_time:
                duration = (end_time - start_time).total_seconds()
                f.write(f"- **Toplam Süre:** {duration:.2f} saniye\n")
            
            f.write(f"- **Hata Sayısı:** {len(migration_stats.get('errors', []))}\n\n")
            
            # MongoDB Bağlantı Bilgileri
            f.write("## MongoDB Bağlantı Bilgileri\n\n")
            f.write(f"- **Host:** {mongodb_config.get('host', 'N/A')}\n")
            f.write(f"- **Port:** {mongodb_config.get('port', 'N/A')}\n")
            f.write(f"- **Database:** {mongodb_config.get('database', 'N/A')}\n\n")
            
            f.write("---\n\n")
            f.write("*Bu rapor otomatik olarak oluşturulmuştur.*\n")
        
        logger.info(f"Rapor oluşturuldu: {filepath}")
        return filepath
    
    def _generate_html_report(self, schema_info: Dict[str, Any],
                             migration_stats: Dict[str, Any],
                             sql_config: Dict[str, Any],
                             mongodb_config: Dict[str, Any]) -> str:
        """
        HTML formatında rapor oluşturur.
        Şimdilik markdown raporu oluşturup HTML'e çevirebiliriz.
        """
        # HTML raporu için basit bir implementasyon
        # Detaylı HTML raporu için ek geliştirme yapılabilir
        markdown_path = self._generate_markdown_report(
            schema_info, migration_stats, sql_config, mongodb_config
        )
        # HTML'e çevirme işlemi burada yapılabilir
        return markdown_path

