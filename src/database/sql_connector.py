"""
SQL Database Connector Module
MySQL ve MSSQL veritabanlarına bağlanmak için kullanılır.
"""

import logging
from typing import Optional, Dict, Any
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
import pymysql
import pyodbc

logger = logging.getLogger(__name__)


class SQLConnector:
    """
    SQL veritabanı bağlantı sınıfı.
    MySQL ve MSSQL veritabanlarına bağlanmayı sağlar.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        SQL bağlantı sınıfını başlatır.
        
        Args:
            config: Veritabanı konfigürasyon bilgileri
        """
        self.config = config
        self.engine: Optional[Engine] = None
        self.inspector = None
        self.db_type = config.get('type', 'mysql').lower()
        
    def connect(self) -> bool:
        """
        Veritabanına bağlanır.
        
        Returns:
            bool: Bağlantı başarılı ise True, değilse False
        """
        try:
            connection_string = self._build_connection_string()
            logger.info(f"{self.db_type.upper()} veritabanına bağlanılıyor...")
            
            # SQLAlchemy engine oluştur
            self.engine = create_engine(connection_string, echo=False)
            
            # Bağlantıyı test et
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            # Inspector oluştur (şema keşfi için)
            self.inspector = inspect(self.engine)
            
            logger.info(f"{self.db_type.upper()} veritabanına başarıyla bağlanıldı")
            return True
            
        except Exception as e:
            logger.error(f"Veritabanı bağlantı hatası: {str(e)}")
            return False
    
    def _build_connection_string(self) -> str:
        """
        Veritabanı tipine göre connection string oluşturur.
        
        Returns:
            str: Connection string
        """
        host = self.config.get('host', 'localhost')
        port = self.config.get('port', 3306)
        database = self.config.get('database')
        username = self.config.get('username')
        password = self.config.get('password')
        
        if self.db_type == 'mysql':
            # MySQL connection string
            return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8mb4"
        
        elif self.db_type == 'mssql':
            # MSSQL connection string
            driver = self.config.get('driver', 'ODBC Driver 17 for SQL Server')
            trust_cert = self.config.get('trust_server_certificate', 'yes')
            return (
                f"mssql+pyodbc://{username}:{password}@{host}:{port}/{database}"
                f"?driver={driver.replace(' ', '+')}"
                f"&TrustServerCertificate={trust_cert}"
            )
        
        else:
            raise ValueError(f"Desteklenmeyen veritabanı tipi: {self.db_type}")
    
    def get_engine(self) -> Optional[Engine]:
        """
        SQLAlchemy engine'i döndürür.
        
        Returns:
            Engine: SQLAlchemy engine
        """
        return self.engine
    
    def get_inspector(self):
        """
        SQLAlchemy inspector'ı döndürür.
        
        Returns:
            Inspector: SQLAlchemy inspector
        """
        return self.inspector
    
    def execute_query(self, query: str) -> list:
        """
        SQL sorgusu çalıştırır ve sonuçları döndürür.
        
        Args:
            query: Çalıştırılacak SQL sorgusu
            
        Returns:
            list: Sorgu sonuçları
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                return result.fetchall()
        except Exception as e:
            logger.error(f"Sorgu çalıştırma hatası: {str(e)}")
            return []
    
    def close(self):
        """
        Veritabanı bağlantısını kapatır.
        """
        if self.engine:
            self.engine.dispose()
            logger.info("Veritabanı bağlantısı kapatıldı")

