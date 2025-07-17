"""
Autor: Sistema de Matrículas Universitarias
Módulo: DAO Estudiante
Descripción: Acceso a datos para estudiantes
Paradigma: POO con herencia
"""

from typing import List, Optional
from dao.base_dao import BaseDAO
from models.estudiante import Estudiante

class EstudianteDAO(BaseDAO):
    """
    Clase para acceso a datos de estudiantes
    Hereda de BaseDAO e implementa métodos específicos
    """
    
    def create(self, estudiante: Estudiante) -> int:
        """
        Crea un nuevo estudiante en la base de datos
        Retorna el ID del estudiante creado
        """
        query = """
        INSERT INTO estudiantes (codigo, nombre, apellido, carrera, email, telefono)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            estudiante.codigo,
            estudiante.nombre,
            estudiante.apellido,
            estudiante.carrera,
            estudiante.email,
            estudiante.telefono
        )
        
        return self._execute_insert_with_id(query, params)
    
    def read(self, id: int) -> Optional[Estudiante]:
        """Lee un estudiante por ID"""
        query = "SELECT * FROM estudiantes WHERE id = %s"
        results = self._execute_query(query, (id,))
        
        if results:
            return self._row_to_estudiante(results[0])
        return None
    
    def find_by_codigo(self, codigo: str) -> Optional[Estudiante]:
        """Busca un estudiante por código"""
        query = "SELECT * FROM estudiantes WHERE codigo = %s"
        results = self._execute_query(query, (codigo,))
        
        if results:
            return self._row_to_estudiante(results[0])
        return None
    
    def update(self, estudiante: Estudiante) -> bool:
        """Actualiza un estudiante existente"""
        query = """
        UPDATE estudiantes 
        SET nombre = %s, apellido = %s, carrera = %s, email = %s, telefono = %s
        WHERE codigo = %s
        """
        params = (
            estudiante.nombre,
            estudiante.apellido,
            estudiante.carrera,
            estudiante.email,
            estudiante.telefono,
            estudiante.codigo
        )
        
        affected_rows = self._execute_update(query, params)
        return affected_rows > 0
    
    def delete(self, id: int) -> bool:
        """Elimina un estudiante por ID"""
        query = "DELETE FROM estudiantes WHERE id = %s"
        affected_rows = self._execute_update(query, (id,))
        return affected_rows > 0
    
    def delete_by_codigo(self, codigo: str) -> bool:
        """Elimina un estudiante por código"""
        query = "DELETE FROM estudiantes WHERE codigo = %s"
        affected_rows = self._execute_update(query, (codigo,))
        return affected_rows > 0
    
    def find_all(self) -> List[Estudiante]:
        """Obtiene todos los estudiantes"""
        query = "SELECT * FROM estudiantes ORDER BY nombre, apellido"
        results = self._execute_query(query)
        
        # Programación funcional: uso de map
        return list(map(self._row_to_estudiante, results))
    
    def find_by_carrera(self, carrera: str) -> List[Estudiante]:
        """Busca estudiantes por carrera"""
        query = "SELECT * FROM estudiantes WHERE carrera = %s ORDER BY nombre, apellido"
        results = self._execute_query(query, (carrera.upper(),))
        
        return list(map(self._row_to_estudiante, results))
    
    def count_by_carrera(self) -> dict:
        """
        Cuenta estudiantes por carrera
        Uso de funciones de agregación SQL
        """
        query = """
        SELECT carrera, COUNT(*) as cantidad 
        FROM estudiantes 
        GROUP BY carrera 
        ORDER BY cantidad DESC
        """
        results = self._execute_query(query)
        
        # Convertir a diccionario usando programación funcional
        return dict(map(lambda row: (row[0], row[1]), results))
    
    def search_by_name(self, nombre: str) -> List[Estudiante]:
        """Busca estudiantes por nombre (búsqueda parcial)"""
        query = """
        SELECT * FROM estudiantes 
        WHERE LOWER(nombre) LIKE %s OR LOWER(apellido) LIKE %s
        ORDER BY nombre, apellido
        """
        search_term = f"%{nombre.lower()}%"
        results = self._execute_query(query, (search_term, search_term))
        
        return list(map(self._row_to_estudiante, results))
    
    def _row_to_estudiante(self, row: tuple) -> Estudiante:
        """
        Convierte una fila de la base de datos a objeto Estudiante
        Mapeo objeto-relacional básico
        """
        # row = (id, codigo, nombre, apellido, carrera, email, telefono, fecha_registro)
        estudiante = Estudiante(
            codigo=row[1],
            nombre=row[2],
            apellido=row[3],
            carrera=row[4],
            email=row[5] or "",
            telefono=row[6] or ""
        )
        
        # Establecer fecha de registro desde la base de datos
        if row[7]:
            estudiante._fecha_registro = row[7]
        
        return estudiante
    
    def exists_codigo(self, codigo: str) -> bool:
        """Verifica si existe un estudiante con el código dado"""
        query = "SELECT COUNT(*) FROM estudiantes WHERE codigo = %s"
        results = self._execute_query(query, (codigo,))
        return results[0][0] > 0 if results else False