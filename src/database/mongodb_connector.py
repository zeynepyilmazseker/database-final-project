"""
MongoDB Connector Module
MongoDB veritabanına bağlanmak ve işlem yapmak için kullanılır.
"""

import logging
from typing import Dict, Any, Optional, List
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

logger = logging.getLogger(__name__)


class MongoDBConnector:
    """
    MongoDB bağlantı sınıfı.
    MongoDB veritabanına bağlanmayı ve işlem yapmayı sağlar.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        MongoDB bağlantı sınıfını başlatır.
        
        Args:
            config: MongoDB konfigürasyon bilgileri
        """
        self.config = config
        self.client: Optional[MongoClient] = None
        self.database: Optional[Database] = None
        
    def connect(self) -> bool:
        """
        MongoDB'ye bağlanır.
        
        Returns:
            bool: Bağlantı başarılı ise True, değilse False
        """
        try:
            # Connection string varsa onu kullan
            if 'connection_string' in self.config and self.config['connection_string']:
                connection_string = self.config['connection_string']
            else:
                # Manuel bağlantı bilgilerinden connection string oluştur
                connection_string = self._build_connection_string()
            
            logger.info("MongoDB'ye bağlanılıyor...")
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            
            # Bağlantıyı test et
            self.client.server_info()
            
            # Database'i seç
            db_name = self.config.get('database', 'migrated_database')
            self.database = self.client[db_name]
            
            logger.info(f"MongoDB'ye başarıyla bağlanıldı (Database: {db_name})")
            return True
            
        except Exception as e:
            logger.error(f"MongoDB bağlantı hatası: {str(e)}")
            return False
    
    def _build_connection_string(self) -> str:
        """
        MongoDB connection string oluşturur.
        
        Returns:
            str: Connection string
        """
        host = self.config.get('host', 'localhost')
        port = self.config.get('port', 27017)
        username = self.config.get('username', '')
        password = self.config.get('password', '')
        database = self.config.get('database', 'migrated_database')
        
        if username and password:
            return f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin"
        else:
            return f"mongodb://{host}:{port}/{database}"
    
    def get_database(self) -> Optional[Database]:
        """
        MongoDB database instance'ını döndürür.
        
        Returns:
            Database: MongoDB database
        """
        return self.database
    
    def get_collection(self, collection_name: str) -> Optional[Collection]:
        """
        Belirtilen collection'ı döndürür.
        
        Args:
            collection_name: Collection ismi
            
        Returns:
            Collection: MongoDB collection
        """
        if self.database is not None:
            return self.database[collection_name]
        return None
    
    def drop_collection(self, collection_name: str) -> bool:
        """
        Belirtilen collection'ı siler.
        
        Args:
            collection_name: Silinecek collection ismi
            
        Returns:
            bool: Silme işlemi başarılı ise True
        """
        try:
            if self.database is not None:
                self.database.drop_collection(collection_name)
                logger.info(f"Collection '{collection_name}' silindi")
                return True
            return False
        except Exception as e:
            logger.error(f"Collection silme hatası: {str(e)}")
            return False
    
    def collection_exists(self, collection_name: str) -> bool:
        """
        Collection'ın var olup olmadığını kontrol eder.
        
        Args:
            collection_name: Kontrol edilecek collection ismi
            
        Returns:
            bool: Collection varsa True
        """
        if self.database is not None:
            return collection_name in self.database.list_collection_names()
        return False
    
    def create_index(self, collection_name: str, index_fields: List[str], unique: bool = False) -> bool:
        """
        Collection'da index oluşturur.
        
        Args:
            collection_name: Collection ismi
            index_fields: Index oluşturulacak alanlar
            unique: Unique index ise True
            
        Returns:
            bool: Index oluşturma başarılı ise True
        """
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                index_spec = [(field, 1) for field in index_fields]
                # Index zaten varsa hata verme (idempotent çalışma için)
                try:
                    collection.create_index(index_spec, unique=unique)
                    logger.debug(f"Index oluşturuldu: {collection_name}.{index_fields}")
                except Exception as idx_error:
                    # Index zaten varsa sadece logla, hata olarak sayma
                    if "existing index" in str(idx_error).lower() or "duplicate" in str(idx_error).lower():
                        logger.debug(f"Index zaten mevcut: {collection_name}.{index_fields}")
                    else:
                        raise
                return True
            return False
        except Exception as e:
            logger.error(f"Index oluşturma hatası: {str(e)}")
            return False
    
    def insert_documents(self, collection_name: str, documents: List[Dict[str, Any]], 
                        batch_size: int = 1000) -> int:
        """
        Collection'a belgeler ekler (batch insert).
        
        Args:
            collection_name: Collection ismi
            documents: Eklenecek belgeler listesi
            batch_size: Her batch'te eklenecek belge sayısı
            
        Returns:
            int: Eklenen belge sayısı
        """
        try:
            collection = self.get_collection(collection_name)
            if collection is None:
                return 0
            
            inserted_count = 0
            total_docs = len(documents)
            
            # Batch'ler halinde ekle
            for i in range(0, total_docs, batch_size):
                batch = documents[i:i + batch_size]
                result = collection.insert_many(batch, ordered=False)
                inserted_count += len(result.inserted_ids)
                logger.debug(f"{collection_name}: {inserted_count}/{total_docs} belge eklendi")
            
            logger.info(f"{collection_name} collection'ına {inserted_count} belge eklendi")
            return inserted_count
            
        except Exception as e:
            logger.error(f"Belge ekleme hatası ({collection_name}): {str(e)}")
            return 0
    
    def close(self):
        """
        MongoDB bağlantısını kapatır.
        """
        if self.client:
            self.client.close()
            logger.info("MongoDB bağlantısı kapatıldı")

