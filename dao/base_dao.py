"""
Autor: Sistema de Matrículas Universitarias
Módulo: DAO Base
Descripción: Clase base para acceso a datos (Data Access Object)
Paradigma: POO con patrón DAO
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from config.database import DatabaseConfig
import logging

class BaseDAO(ABC):
    """
    Clase abstracta base para operaciones de acceso a datos
    Implementa el patrón DAO y principios de abstracción
    """
    
    def __init__(self):
        """Constructor de la clase base DAO"""
        self.db_config = DatabaseConfig()
        self.logger = logging.getLogger(__name__)
    
    def _get_connection(self):
        """Obtiene una conexión a la base de datos"""
        if not self.db_config.connect():
            raise Exception("No se pudo establecer conexión con la base de datos")
        return self.db_config.get_connection()
    
    def _close_connection(self):
        """Cierra la conexión a la base de datos"""
        self.db_config.disconnect()
    
    def _execute_query(self, query: str, params: tuple = None) -> List[tuple]:
        """
        Ejecuta una consulta SELECT y retorna los resultados
        Manejo de errores y logging
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            self.logger.info(f"Consulta ejecutada exitosamente: {len(results)} registros")
            return results
            
        except Exception as e:
            self.logger.error(f"Error ejecutando consulta: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def _execute_update(self, query: str, params: tuple = None) -> int:
        """
        Ejecuta una consulta INSERT, UPDATE o DELETE
        Retorna el número de filas afectadas
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            connection.commit()
            affected_rows = cursor.rowcount
            self.logger.info(f"Operación ejecutada exitosamente: {affected_rows} filas afectadas")
            return affected_rows
            
        except Exception as e:
            if connection:
                connection.rollback()
            self.logger.error(f"Error ejecutando operación: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def _execute_insert_with_id(self, query: str, params: tuple = None) -> int:
        """
        Ejecuta un INSERT y retorna el ID del registro insertado
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            connection.commit()
            last_id = cursor.lastrowid
            self.logger.info(f"Registro insertado con ID: {last_id}")
            return last_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            self.logger.error(f"Error insertando registro: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    # Métodos abstractos que deben implementar las clases hijas
    @abstractmethod
    def create(self, entity) -> int:
        """Crea un nuevo registro"""
        pass
    
    @abstractmethod
    def read(self, id: int):
        """Lee un registro por ID"""
        pass
    
    @abstractmethod
    def update(self, entity) -> bool:
        """Actualiza un registro existente"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Elimina un registro por ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List:
        """Obtiene todos los registros"""
        pass