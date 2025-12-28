"""
Database Migration Tool - Main Application
MySQL/MSSQL veritabanından MongoDB'ye otomatik veri aktarım uygulaması.

Bu uygulama:
- SQL veritabanına bağlanır
- Şemayı dinamik olarak keşfeder
- Verileri MongoDB'ye aktarır
- Detaylı rapor oluşturur
"""

import sys
import os
import logging
import yaml
from pathlib import Path
import colorlog
from datetime import datetime

# Proje dizinini Python path'ine ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.database.sql_connector import SQLConnector
from src.database.schema_discovery import SchemaDiscovery
from src.database.mongodb_connector import MongoDBConnector
from src.migration.migrator import DataMigrator
from src.reporting.report_generator import ReportGenerator


def setup_logging(config: dict) -> None:
    """
    Logging sistemini yapılandırır.
    
    Args:
        config: Logging konfigürasyonu
    """
    log_level = getattr(logging, config.get('level', 'INFO').upper())
    log_file = config.get('file', 'logs/migration.log')
    console_output = config.get('console', True)
    
    # Log dizinini oluştur
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    # Root logger'ı yapılandır
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Formatter oluştur
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler
    if console_output:
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)


def load_config(config_path: str = 'config.yaml') -> dict:
    """
    Konfigürasyon dosyasını yükler.
    
    Args:
        config_path: Konfigürasyon dosyası yolu
        
    Returns:
        dict: Konfigürasyon bilgileri
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"HATA: Konfigürasyon dosyası bulunamadı: {config_path}")
        print("Lütfen config.yaml dosyasını oluşturun ve düzenleyin.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"HATA: Konfigürasyon dosyası okunamadı: {str(e)}")
        sys.exit(1)


def main():
    """
    Ana uygulama fonksiyonu.
    Migration sürecini yönetir.
    """
    print("=" * 60)
    print("SQL → MongoDB Migration Tool")
    print("=" * 60)
    print()
    
    # Konfigürasyonu yükle
    config = load_config()
    
    # Logging'i yapılandır
    setup_logging(config.get('logging', {}))
    logger = logging.getLogger(__name__)
    
    logger.info("Migration uygulaması başlatılıyor...")
    logger.info(f"Başlangıç zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # SQL veritabanı bağlantısı
    sql_config = config.get('sql_database', {})
    sql_connector = SQLConnector(sql_config)
    
    if not sql_connector.connect():
        logger.error("SQL veritabanına bağlanılamadı. Uygulama sonlandırılıyor.")
        sys.exit(1)
    
    try:
        # Şema keşfi
        logger.info("Şema keşfi başlatılıyor...")
        schema_discovery = SchemaDiscovery(sql_connector)
        schema_info = schema_discovery.discover_all()
        
        # Keşfedilen nesneleri logla
        logger.info(f"Keşif tamamlandı:")
        logger.info(f"  - Tablolar: {len(schema_info.get('tables', []))}")
        logger.info(f"  - Trigger'ler: {sum(len(v) for v in schema_info.get('triggers', {}).values())}")
        logger.info(f"  - Stored Procedure'ler: {len(schema_info.get('stored_procedures', []))}")
        logger.info(f"  - Function'lar: {len(schema_info.get('functions', []))}")
        
        # MongoDB bağlantısı
        mongodb_config = config.get('mongodb', {})
        mongodb_connector = MongoDBConnector(mongodb_config)
        
        if not mongodb_connector.connect():
            logger.error("MongoDB'ye bağlanılamadı. Uygulama sonlandırılıyor.")
            sys.exit(1)
        
        try:
            # Veri aktarımı
            migration_config = config.get('migration', {})
            migrator = DataMigrator(sql_connector, mongodb_connector, migration_config)
            
            logger.info("Veri aktarımı başlatılıyor...")
            migration_stats = migrator.migrate_all(schema_info)
            
            # Rapor oluşturma
            reporting_config = config.get('reporting', {})
            report_generator = ReportGenerator(
                output_dir=reporting_config.get('output_dir', 'reports'),
                format=reporting_config.get('format', 'markdown')
            )
            
            logger.info("Teknik rapor oluşturuluyor...")
            report_path = report_generator.generate_report(
                schema_info,
                migration_stats,
                sql_config,
                mongodb_config
            )
            
            logger.info(f"Rapor oluşturuldu: {report_path}")
            
            # Özet bilgiler
            print()
            print("=" * 60)
            print("MIGRATION TAMAMLANDI")
            print("=" * 60)
            print(f"Aktarılan Tablo Sayısı: {migration_stats.get('tables_migrated', 0)}")
            print(f"Aktarılan Belge Sayısı: {migration_stats.get('total_documents', 0)}")
            print(f"Hata Sayısı: {len(migration_stats.get('errors', []))}")
            print(f"Rapor: {report_path}")
            print("=" * 60)
            
        finally:
            mongodb_connector.close()
    
    finally:
        sql_connector.close()
    
    logger.info("Migration uygulaması başarıyla tamamlandı.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nKullanıcı tarafından iptal edildi.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Beklenmeyen hata: {str(e)}", exc_info=True)
        sys.exit(1)

