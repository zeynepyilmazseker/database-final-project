"""
Data Migration Module
SQL veritabanından MongoDB'ye veri aktarımını yönetir.
İdempotent çalışma sağlar (tekrar çalıştırılabilir).
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, date
from sqlalchemy import text
from pymongo import UpdateOne

logger = logging.getLogger(__name__)


class DataMigrator:
    """
    Veri aktarım sınıfı.
    SQL veritabanından MongoDB'ye veri aktarımını gerçekleştirir.
    """
    
    def __init__(self, sql_connector, mongodb_connector, config: Dict[str, Any]):
        """
        Migrator sınıfını başlatır.
        
        Args:
            sql_connector: SQLConnector instance
            mongodb_connector: MongoDBConnector instance
            config: Migration konfigürasyonu
        """
        self.sql_connector = sql_connector
        self.mongodb_connector = mongodb_connector
        self.config = config
        self.batch_size = config.get('batch_size', 1000)
        self.drop_existing = config.get('drop_existing', False)
        self.preserve_ids = config.get('preserve_ids', True)
        self.db_type = sql_connector.db_type  # Veritabanı tipini al
        
        # Migration istatistikleri
        self.migration_stats = {
            'tables_migrated': 0,
            'total_documents': 0,
            'errors': [],
            'start_time': None,
            'end_time': None
        }
    
    def migrate_all(self, schema_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tüm tabloları MongoDB'ye aktarır.
        
        Args:
            schema_info: Keşfedilen şema bilgileri
            
        Returns:
            dict: Migration istatistikleri
        """
        self.migration_stats['start_time'] = datetime.now()
        logger.info("Veri aktarımı başlatılıyor...")
        
        tables = schema_info.get('tables', [])
        columns_info = schema_info.get('columns', {})
        primary_keys = schema_info.get('primary_keys', {})
        
        for table_name in tables:
            try:
                self._migrate_table(
                    table_name,
                    columns_info.get(table_name, []),
                    primary_keys.get(table_name, [])
                )
                self.migration_stats['tables_migrated'] += 1
            except Exception as e:
                error_msg = f"{table_name} tablosu aktarım hatası: {str(e)}"
                logger.error(error_msg)
                self.migration_stats['errors'].append(error_msg)
        
        # Index'leri oluştur
        self._create_indexes(schema_info)
        
        self.migration_stats['end_time'] = datetime.now()
        duration = (self.migration_stats['end_time'] - 
                   self.migration_stats['start_time']).total_seconds()
        
        logger.info(f"Veri aktarımı tamamlandı. "
                   f"{self.migration_stats['tables_migrated']} tablo, "
                   f"{self.migration_stats['total_documents']} belge aktarıldı. "
                   f"Süre: {duration:.2f} saniye")
        
        return self.migration_stats
    
    def _migrate_table(self, table_name: str, columns: List[Dict], 
                      primary_keys: List[str]):
        """
        Tek bir tabloyu MongoDB'ye aktarır.
        
        Args:
            table_name: Aktarılacak tablo ismi
            columns: Tablo kolon bilgileri
            primary_keys: Primary key kolonları
        """
        logger.info(f"{table_name} tablosu aktarılıyor...")
        
        collection_name = table_name  # Collection ismi tablo ismiyle aynı
        
        # Mevcut collection'ı sil (eğer drop_existing True ise)
        if self.drop_existing and self.mongodb_connector.collection_exists(collection_name):
            self.mongodb_connector.drop_collection(collection_name)
            logger.info(f"Mevcut collection '{collection_name}' silindi")
        
        # SQL'den verileri çek
        engine = self.sql_connector.get_engine()
        if not engine:
            raise Exception("SQL engine bulunamadı")
        
        # Tüm verileri çek
        # Tablo ismini veritabanı tipine göre quote et
        if self.db_type == 'mysql':
            # MySQL için backtick kullan
            quoted_table = f"`{table_name}`"
        elif self.db_type == 'mssql':
            # MSSQL için köşeli parantez kullan
            quoted_table = f"[{table_name}]"
        else:
            quoted_table = table_name
        
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {quoted_table}"))
            rows = result.fetchall()
            column_names = list(result.keys())
        
        if not rows:
            logger.warning(f"{table_name} tablosu boş, atlanıyor")
            return
        
        # MongoDB belgelerine dönüştür
        documents = []
        for row in rows:
            doc = {}
            
            # Row'u dict'e çevir (SQLAlchemy 2.0 uyumluluğu için)
            row_dict = dict(row._mapping) if hasattr(row, '_mapping') else dict(zip(column_names, row))
            
            # Primary key'i _id olarak kullan (eğer preserve_ids True ise)
            if self.preserve_ids and primary_keys:
                if len(primary_keys) == 1:
                    # Tek kolonlu PK
                    doc['_id'] = self._convert_value(row_dict[primary_keys[0]])
                else:
                    # Composite PK - string olarak birleştir
                    pk_value = '_'.join([str(row_dict[pk]) for pk in primary_keys])
                    doc['_id'] = pk_value
            
            # Tüm kolonları ekle
            for col_name in column_names:
                # Primary key'i _id olarak kullandıysak, belge içinde de tut (None yerine gerçek değer)
                if col_name in primary_keys and self.preserve_ids:
                    # Primary key değerini belge içinde de sakla
                    doc[col_name] = self._convert_value(row_dict[col_name])
                elif col_name not in primary_keys:
                    value = row_dict[col_name]
                    doc[col_name] = self._convert_value(value)
            
            documents.append(doc)
        
        # MongoDB'ye ekle (upsert kullanarak idempotent yap)
        if self.preserve_ids and primary_keys:
            # Upsert kullan (idempotent)
            self._upsert_documents(collection_name, documents)
        else:
            # Normal insert
            inserted = self.mongodb_connector.insert_documents(
                collection_name, documents, self.batch_size
            )
            self.migration_stats['total_documents'] += inserted
    
    def _upsert_documents(self, collection_name: str, documents: List[Dict[str, Any]]):
        """
        Belgeleri upsert eder (idempotent çalışma için).
        
        Args:
            collection_name: Collection ismi
            documents: Upsert edilecek belgeler
        """
        collection = self.mongodb_connector.get_collection(collection_name)
        if collection is None:
            return
        
        operations = []
        for doc in documents:
            # _id'yi al
            doc_id = doc.pop('_id', None)
            if doc_id is not None:
                # Upsert operation
                operations.append(
                    UpdateOne(
                        {'_id': doc_id},
                        {'$set': doc},
                        upsert=True
                    )
                )
            else:
                # _id yoksa normal insert
                operations.append(UpdateOne({}, {'$set': doc}, upsert=False))
        
        # Batch halinde çalıştır
        if operations:
            for i in range(0, len(operations), self.batch_size):
                batch = operations[i:i + self.batch_size]
                result = collection.bulk_write(batch, ordered=False)
                self.migration_stats['total_documents'] += (
                    result.inserted_count + result.modified_count + result.upserted_count
                )
                logger.debug(f"{collection_name}: {i + len(batch)}/{len(operations)} belge işlendi")
    
    def _convert_value(self, value: Any) -> Any:
        """
        SQL değerini MongoDB uyumlu değere dönüştürür.
        
        Args:
            value: Dönüştürülecek değer
            
        Returns:
            MongoDB uyumlu değer
        """
        if value is None:
            return None
        
        # DateTime objelerini string'e çevir
        if isinstance(value, datetime):
            return value.isoformat()
        
        # Date objelerini string'e çevir
        if isinstance(value, date):
            return value.isoformat()
        
        # Binary/BLOB verilerini base64 string'e çevir
        if isinstance(value, (bytes, bytearray)):
            import base64
            return base64.b64encode(value).decode('utf-8')
        
        # Decimal, float gibi tipleri düzelt
        if hasattr(value, '__float__'):
            try:
                return float(value)
            except (ValueError, TypeError):
                pass
        
        # Diğer tipleri olduğu gibi döndür
        return value
    
    def _create_indexes(self, schema_info: Dict[str, Any]):
        """
        MongoDB'de index'leri oluşturur.
        
        Args:
            schema_info: Şema bilgileri
        """
        logger.info("Index'ler oluşturuluyor...")
        
        indexes_info = schema_info.get('indexes', {})
        primary_keys = schema_info.get('primary_keys', {})
        
        # Primary key index'lerini oluştur
        for table_name, pk_columns in primary_keys.items():
            if pk_columns:
                collection_name = table_name
                self.mongodb_connector.create_index(
                    collection_name, pk_columns, unique=True
                )
        
        # Diğer index'leri oluştur
        for table_name, indexes in indexes_info.items():
            collection_name = table_name
            for index in indexes:
                index_fields = index.get('columns', [])
                unique = index.get('unique', False)
                if index_fields:
                    self.mongodb_connector.create_index(
                        collection_name, index_fields, unique=unique
                    )
        
        logger.info("Index oluşturma tamamlandı")
    
    def get_migration_stats(self) -> Dict[str, Any]:
        """
        Migration istatistiklerini döndürür.
        
        Returns:
            dict: Migration istatistikleri
        """
        return self.migration_stats

