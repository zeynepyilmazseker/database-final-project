"""
Örnek Kullanım Senaryoları
Bu dosya, uygulamanın farklı senaryolarda nasıl kullanılacağını gösterir.
"""

import sys
from pathlib import Path

# Proje dizinini Python path'ine ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.database.sql_connector import SQLConnector
from src.database.schema_discovery import SchemaDiscovery
from src.database.mongodb_connector import MongoDBConnector
from src.migration.migrator import DataMigrator


def example_mysql_migration():
    """
    MySQL veritabanından MongoDB'ye migration örneği.
    """
    # MySQL konfigürasyonu
    mysql_config = {
        'type': 'mysql',
        'host': 'localhost',
        'port': 3306,
        'database': 'example_db',
        'username': 'root',
        'password': 'password'
    }
    
    # MongoDB konfigürasyonu
    mongodb_config = {
        'host': 'localhost',
        'port': 27017,
        'database': 'migrated_db'
    }
    
    # Migration konfigürasyonu
    migration_config = {
        'batch_size': 1000,
        'drop_existing': False,
        'preserve_ids': True
    }
    
    # Bağlantıları oluştur
    sql_connector = SQLConnector(mysql_config)
    if not sql_connector.connect():
        print("MySQL'e bağlanılamadı!")
        return
    
    mongodb_connector = MongoDBConnector(mongodb_config)
    if not mongodb_connector.connect():
        print("MongoDB'ye bağlanılamadı!")
        sql_connector.close()
        return
    
    try:
        # Şema keşfi
        schema_discovery = SchemaDiscovery(sql_connector)
        schema_info = schema_discovery.discover_all()
        
        # Veri aktarımı
        migrator = DataMigrator(sql_connector, mongodb_connector, migration_config)
        stats = migrator.migrate_all(schema_info)
        
        print(f"Migration tamamlandı: {stats['tables_migrated']} tablo, "
              f"{stats['total_documents']} belge aktarıldı.")
    
    finally:
        sql_connector.close()
        mongodb_connector.close()


def example_mssql_migration():
    """
    MSSQL veritabanından MongoDB'ye migration örneği.
    """
    # MSSQL konfigürasyonu
    mssql_config = {
        'type': 'mssql',
        'host': 'localhost',
        'port': 1433,
        'database': 'example_db',
        'username': 'sa',
        'password': 'password',
        'driver': 'ODBC Driver 17 for SQL Server',
        'trust_server_certificate': 'yes'
    }
    
    # MongoDB konfigürasyonu
    mongodb_config = {
        'host': 'localhost',
        'port': 27017,
        'database': 'migrated_db'
    }
    
    # Migration konfigürasyonu
    migration_config = {
        'batch_size': 500,
        'drop_existing': True,
        'preserve_ids': True
    }
    
    # Bağlantıları oluştur
    sql_connector = SQLConnector(mssql_config)
    if not sql_connector.connect():
        print("MSSQL'e bağlanılamadı!")
        return
    
    mongodb_connector = MongoDBConnector(mongodb_config)
    if not mongodb_connector.connect():
        print("MongoDB'ye bağlanılamadı!")
        sql_connector.close()
        return
    
    try:
        # Şema keşfi
        schema_discovery = SchemaDiscovery(sql_connector)
        schema_info = schema_discovery.discover_all()
        
        # Veri aktarımı
        migrator = DataMigrator(sql_connector, mongodb_connector, migration_config)
        stats = migrator.migrate_all(schema_info)
        
        print(f"Migration tamamlandı: {stats['tables_migrated']} tablo, "
              f"{stats['total_documents']} belge aktarıldı.")
    
    finally:
        sql_connector.close()
        mongodb_connector.close()


if __name__ == "__main__":
    print("Örnek kullanım senaryoları")
    print("Bu dosyayı çalıştırmak için önce config.yaml dosyasını düzenleyin")
    print("ve ardından main.py'yi çalıştırın.")

