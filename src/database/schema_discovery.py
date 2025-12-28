"""
Schema Discovery Module
SQL veritabanı şemasını dinamik olarak keşfeder.
Tablolar, kolonlar, indexler, constraintler, triggerler ve stored procedure'leri tespit eder.
"""

import logging
from typing import Dict, List, Any, Optional
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


class SchemaDiscovery:
    """
    Veritabanı şema keşif sınıfı.
    Tüm yapısal bileşenleri otomatik olarak tespit eder.
    """
    
    def __init__(self, connector):
        """
        Şema keşif sınıfını başlatır.
        
        Args:
            connector: SQLConnector instance
        """
        self.connector = connector
        self.engine: Engine = connector.get_engine()
        self.inspector = connector.get_inspector()
        self.db_type = connector.db_type
        self.schema_info: Dict[str, Any] = {}
        
    def discover_all(self) -> Dict[str, Any]:
        """
        Tüm veritabanı şemasını keşfeder.
        
        Returns:
            dict: Keşfedilen tüm şema bilgileri
        """
        logger.info("Veritabanı şeması keşfediliyor...")
        
        self.schema_info = {
            'tables': self.discover_tables(),
            'columns': self.discover_columns(),
            'primary_keys': self.discover_primary_keys(),
            'foreign_keys': self.discover_foreign_keys(),
            'indexes': self.discover_indexes(),
            'constraints': self.discover_constraints(),
            'triggers': self.discover_triggers(),
            'stored_procedures': self.discover_stored_procedures(),
            'functions': self.discover_functions(),
            'views': self.discover_views()
        }
        
        logger.info("Şema keşfi tamamlandı")
        return self.schema_info
    
    def discover_tables(self) -> List[str]:
        """
        Veritabanındaki tüm tabloları keşfeder.
        
        Returns:
            list: Tablo isimleri listesi
        """
        try:
            tables = self.inspector.get_table_names()
            logger.info(f"{len(tables)} tablo bulundu: {', '.join(tables)}")
            return tables
        except Exception as e:
            logger.error(f"Tablo keşif hatası: {str(e)}")
            return []
    
    def discover_columns(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Tüm tablolardaki kolonları keşfeder.
        
        Returns:
            dict: Tablo isimlerine göre kolon bilgileri
        """
        columns_info = {}
        
        try:
            tables = self.discover_tables()
            for table_name in tables:
                columns = self.inspector.get_columns(table_name)
                columns_info[table_name] = []
                
                for col in columns:
                    col_info = {
                        'name': col['name'],
                        'type': str(col['type']),
                        'nullable': col.get('nullable', True),
                        'default': str(col.get('default', '')),
                        'autoincrement': col.get('autoincrement', False)
                    }
                    columns_info[table_name].append(col_info)
                
                logger.debug(f"{table_name} tablosunda {len(columns)} kolon bulundu")
            
            return columns_info
            
        except Exception as e:
            logger.error(f"Kolon keşif hatası: {str(e)}")
            return {}
    
    def discover_primary_keys(self) -> Dict[str, List[str]]:
        """
        Tüm tablolardaki primary key'leri keşfeder.
        
        Returns:
            dict: Tablo isimlerine göre primary key kolonları
        """
        pk_info = {}
        
        try:
            tables = self.discover_tables()
            for table_name in tables:
                pk_constraint = self.inspector.get_pk_constraint(table_name)
                if pk_constraint and pk_constraint.get('constrained_columns'):
                    pk_info[table_name] = pk_constraint['constrained_columns']
                    logger.debug(f"{table_name} tablosunda PK: {pk_info[table_name]}")
            
            return pk_info
            
        except Exception as e:
            logger.error(f"Primary key keşif hatası: {str(e)}")
            return {}
    
    def discover_foreign_keys(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Tüm tablolardaki foreign key'leri keşfeder.
        
        Returns:
            dict: Tablo isimlerine göre foreign key bilgileri
        """
        fk_info = {}
        
        try:
            tables = self.discover_tables()
            for table_name in tables:
                foreign_keys = self.inspector.get_foreign_keys(table_name)
                if foreign_keys:
                    fk_info[table_name] = []
                    for fk in foreign_keys:
                        fk_data = {
                            'name': fk.get('name', ''),
                            'constrained_columns': fk.get('constrained_columns', []),
                            'referred_table': fk.get('referred_table', ''),
                            'referred_columns': fk.get('referred_columns', [])
                        }
                        fk_info[table_name].append(fk_data)
                    logger.debug(f"{table_name} tablosunda {len(foreign_keys)} FK bulundu")
            
            return fk_info
            
        except Exception as e:
            logger.error(f"Foreign key keşif hatası: {str(e)}")
            return {}
    
    def discover_indexes(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Tüm tablolardaki index'leri keşfeder.
        
        Returns:
            dict: Tablo isimlerine göre index bilgileri
        """
        indexes_info = {}
        
        try:
            tables = self.discover_tables()
            for table_name in tables:
                indexes = self.inspector.get_indexes(table_name)
                if indexes:
                    indexes_info[table_name] = []
                    for idx in indexes:
                        idx_data = {
                            'name': idx.get('name', ''),
                            'columns': idx.get('column_names', []),
                            'unique': idx.get('unique', False)
                        }
                        indexes_info[table_name].append(idx_data)
                    logger.debug(f"{table_name} tablosunda {len(indexes)} index bulundu")
            
            return indexes_info
            
        except Exception as e:
            logger.error(f"Index keşif hatası: {str(e)}")
            return {}
    
    def discover_constraints(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Check constraint'leri keşfeder.
        
        Returns:
            dict: Tablo isimlerine göre constraint bilgileri
        """
        constraints_info = {}
        
        try:
            if self.db_type == 'mysql':
                # MySQL için check constraint sorgusu
                query = """
                    SELECT 
                        TABLE_NAME,
                        CONSTRAINT_NAME,
                        CHECK_CLAUSE
                    FROM INFORMATION_SCHEMA.CHECK_CONSTRAINTS
                    WHERE CONSTRAINT_SCHEMA = DATABASE()
                """
            elif self.db_type == 'mssql':
                # MSSQL için check constraint sorgusu
                query = """
                    SELECT 
                        OBJECT_NAME(parent_object_id) AS TABLE_NAME,
                        name AS CONSTRAINT_NAME,
                        definition AS CHECK_CLAUSE
                    FROM sys.check_constraints
                """
            else:
                return {}
            
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                rows = result.fetchall()
                
                for row in rows:
                    table_name = row[0]
                    if table_name not in constraints_info:
                        constraints_info[table_name] = []
                    
                    constraint_data = {
                        'name': row[1],
                        'check_clause': row[2] if len(row) > 2 else ''
                    }
                    constraints_info[table_name].append(constraint_data)
            
            logger.info(f"{sum(len(v) for v in constraints_info.values())} check constraint bulundu")
            return constraints_info
            
        except Exception as e:
            logger.warning(f"Constraint keşif hatası (bazı veritabanlarında desteklenmeyebilir): {str(e)}")
            return {}
    
    def discover_triggers(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Tüm trigger'leri keşfeder.
        
        Returns:
            dict: Tablo isimlerine göre trigger bilgileri
        """
        triggers_info = {}
        
        try:
            if self.db_type == 'mysql':
                query = """
                    SELECT 
                        TRIGGER_NAME,
                        EVENT_MANIPULATION,
                        EVENT_OBJECT_TABLE,
                        ACTION_STATEMENT,
                        ACTION_TIMING
                    FROM INFORMATION_SCHEMA.TRIGGERS
                    WHERE TRIGGER_SCHEMA = DATABASE()
                """
            elif self.db_type == 'mssql':
                query = """
                    SELECT 
                        t.name AS TRIGGER_NAME,
                        te.type_desc AS EVENT_MANIPULATION,
                        OBJECT_NAME(t.parent_id) AS EVENT_OBJECT_TABLE,
                        OBJECT_DEFINITION(t.object_id) AS ACTION_STATEMENT,
                        CASE 
                            WHEN te.is_after = 1 THEN 'AFTER'
                            WHEN te.is_instead_of = 1 THEN 'INSTEAD OF'
                            ELSE 'BEFORE'
                        END AS ACTION_TIMING
                    FROM sys.triggers t
                    INNER JOIN sys.trigger_events te ON t.object_id = te.object_id
                    WHERE t.parent_class = 1
                """
            else:
                return {}
            
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                rows = result.fetchall()
                
                for row in rows:
                    table_name = row[2] if len(row) > 2 else 'UNKNOWN'
                    if table_name not in triggers_info:
                        triggers_info[table_name] = []
                    
                    trigger_data = {
                        'name': row[0],
                        'event': row[1] if len(row) > 1 else '',
                        'timing': row[4] if len(row) > 4 else '',
                        'statement': row[3] if len(row) > 3 else ''
                    }
                    triggers_info[table_name].append(trigger_data)
            
            logger.info(f"{sum(len(v) for v in triggers_info.values())} trigger bulundu")
            return triggers_info
            
        except Exception as e:
            logger.warning(f"Trigger keşif hatası: {str(e)}")
            return {}
    
    def discover_stored_procedures(self) -> List[Dict[str, Any]]:
        """
        Tüm stored procedure'leri keşfeder.
        
        Returns:
            list: Stored procedure bilgileri
        """
        procedures = []
        
        try:
            if self.db_type == 'mysql':
                query = """
                    SELECT 
                        ROUTINE_NAME,
                        ROUTINE_DEFINITION,
                        ROUTINE_TYPE
                    FROM INFORMATION_SCHEMA.ROUTINES
                    WHERE ROUTINE_SCHEMA = DATABASE()
                    AND ROUTINE_TYPE = 'PROCEDURE'
                """
            elif self.db_type == 'mssql':
                query = """
                    SELECT 
                        name AS ROUTINE_NAME,
                        OBJECT_DEFINITION(object_id) AS ROUTINE_DEFINITION,
                        'PROCEDURE' AS ROUTINE_TYPE
                    FROM sys.procedures
                    WHERE is_ms_shipped = 0
                """
            else:
                return []
            
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                rows = result.fetchall()
                
                for row in rows:
                    proc_data = {
                        'name': row[0],
                        'definition': row[1] if len(row) > 1 else '',
                        'type': row[2] if len(row) > 2 else 'PROCEDURE'
                    }
                    procedures.append(proc_data)
            
            logger.info(f"{len(procedures)} stored procedure bulundu")
            return procedures
            
        except Exception as e:
            logger.warning(f"Stored procedure keşif hatası: {str(e)}")
            return []
    
    def discover_functions(self) -> List[Dict[str, Any]]:
        """
        Tüm function'ları keşfeder.
        
        Returns:
            list: Function bilgileri
        """
        functions = []
        
        try:
            if self.db_type == 'mysql':
                query = """
                    SELECT 
                        ROUTINE_NAME,
                        ROUTINE_DEFINITION,
                        ROUTINE_TYPE
                    FROM INFORMATION_SCHEMA.ROUTINES
                    WHERE ROUTINE_SCHEMA = DATABASE()
                    AND ROUTINE_TYPE = 'FUNCTION'
                """
            elif self.db_type == 'mssql':
                query = """
                    SELECT 
                        name AS ROUTINE_NAME,
                        OBJECT_DEFINITION(object_id) AS ROUTINE_DEFINITION,
                        'FUNCTION' AS ROUTINE_TYPE
                    FROM sys.objects
                    WHERE type IN ('FN', 'IF', 'TF')
                    AND is_ms_shipped = 0
                """
            else:
                return []
            
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                rows = result.fetchall()
                
                for row in rows:
                    func_data = {
                        'name': row[0],
                        'definition': row[1] if len(row) > 1 else '',
                        'type': row[2] if len(row) > 2 else 'FUNCTION'
                    }
                    functions.append(func_data)
            
            logger.info(f"{len(functions)} function bulundu")
            return functions
            
        except Exception as e:
            logger.warning(f"Function keşif hatası: {str(e)}")
            return []
    
    def discover_views(self) -> List[Dict[str, Any]]:
        """
        Tüm view'leri keşfeder.
        
        Returns:
            list: View bilgileri
        """
        views = []
        
        try:
            view_names = self.inspector.get_view_names()
            for view_name in view_names:
                view_data = {
                    'name': view_name,
                    'definition': ''  # View definition'ı almak için ek sorgu gerekebilir
                }
                views.append(view_data)
            
            logger.info(f"{len(views)} view bulundu")
            return views
            
        except Exception as e:
            logger.warning(f"View keşif hatası: {str(e)}")
            return []
    
    def get_schema_info(self) -> Dict[str, Any]:
        """
        Keşfedilen şema bilgilerini döndürür.
        
        Returns:
            dict: Şema bilgileri
        """
        return self.schema_info

