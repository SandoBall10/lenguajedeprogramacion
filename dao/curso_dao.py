"""
Autor: Sistema de Matrículas Universitarias
Módulo: DAO Curso
Descripción: Acceso a datos para cursos
Paradigma: POO con herencia
"""

from typing import List, Optional
from dao.base_dao import BaseDAO
from models.curso import Curso

class CursoDAO(BaseDAO):
    """
    Clase para acceso a datos de cursos
    Hereda de BaseDAO e implementa métodos específicos
    """
    
    def create(self, curso: Curso) -> int:
        """Crea un nuevo curso en la base de datos"""
        query = """
        INSERT INTO cursos (codigo, nombre, creditos, profesor, horario, cupos_disponibles)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            curso.codigo,
            curso.nombre,
            curso.creditos,
            curso.profesor,
            curso.horario,
            curso._cupos_disponibles  # Acceso al atributo privado para obtener cupos totales
        )
        
        return self._execute_insert_with_id(query, params)
    
    def read(self, id: int) -> Optional[Curso]:
        """Lee un curso por ID"""
        query = "SELECT * FROM cursos WHERE id = %s"
        results = self._execute_query(query, (id,))
        
        if results:
            return self._row_to_curso(results[0])
        return None
    
    def find_by_codigo(self, codigo: str) -> Optional[Curso]:
        """Busca un curso por código"""
        query = "SELECT * FROM cursos WHERE codigo = %s"
        results = self._execute_query(query, (codigo,))
        
        if results:
            return self._row_to_curso(results[0])
        return None
    
    def update(self, curso: Curso) -> bool:
        """Actualiza un curso existente"""
        query = """
        UPDATE cursos 
        SET nombre = %s, creditos = %s, profesor = %s, horario = %s, cupos_disponibles = %s
        WHERE codigo = %s
        """
        params = (
            curso.nombre,
            curso.creditos,
            curso.profesor,
            curso.horario,
            curso._cupos_disponibles,
            curso.codigo
        )
        
        affected_rows = self._execute_update(query, params)
        return affected_rows > 0
    
    def delete(self, id: int) -> bool:
        """Elimina un curso por ID"""
        query = "DELETE FROM cursos WHERE id = %s"
        affected_rows = self._execute_update(query, (id,))
        return affected_rows > 0
    
    def delete_by_codigo(self, codigo: str) -> bool:
        """Elimina un curso por código"""
        query = "DELETE FROM cursos WHERE codigo = %s"
        affected_rows = self._execute_update(query, (codigo,))
        return affected_rows > 0
    
    def find_all(self) -> List[Curso]:
        """Obtiene todos los cursos"""
        query = "SELECT * FROM cursos ORDER BY nombre"
        results = self._execute_query(query)
        
        return list(map(self._row_to_curso, results))
    
    def find_by_creditos(self, creditos: int) -> List[Curso]:
        """Busca cursos por número de créditos"""
        query = "SELECT * FROM cursos WHERE creditos = %s ORDER BY nombre"
        results = self._execute_query(query, (creditos,))
        
        return list(map(self._row_to_curso, results))
    
    def find_with_available_spots(self) -> List[Curso]:
        """
        Busca cursos con cupos disponibles
        Uso de subconsultas y funciones de agregación
        """
        query = """
        SELECT c.* FROM cursos c
        WHERE c.cupos_disponibles > (
            SELECT COUNT(*) FROM matriculas m 
            WHERE m.curso_id = c.id AND m.estado = 'ACTIVA'
        )
        ORDER BY c.nombre
        """
        results = self._execute_query(query)
        
        return list(map(self._row_to_curso, results))
    
    def get_enrollment_stats(self) -> List[dict]:
        """
        Obtiene estadísticas de matrícula por curso
        Uso de JOINs y funciones de agregación
        """
        query = """
        SELECT 
            c.codigo,
            c.nombre,
            c.cupos_disponibles,
            COUNT(m.id) as matriculados,
            (c.cupos_disponibles - COUNT(m.id)) as cupos_libres,
            ROUND((COUNT(m.id) * 100.0 / c.cupos_disponibles), 2) as porcentaje_ocupacion
        FROM cursos c
        LEFT JOIN matriculas m ON c.id = m.curso_id AND m.estado = 'ACTIVA'
        GROUP BY c.id, c.codigo, c.nombre, c.cupos_disponibles
        ORDER BY porcentaje_ocupacion DESC
        """
        results = self._execute_query(query)
        
        # Convertir a lista de diccionarios
        stats = []
        for row in results:
            stats.append({
                'codigo': row[0],
                'nombre': row[1],
                'cupos_totales': row[2],
                'matriculados': row[3],
                'cupos_libres': row[4],
                'porcentaje_ocupacion': float(row[5])
            })
        
        return stats
    
    def search_by_name(self, nombre: str) -> List[Curso]:
        """Busca cursos por nombre (búsqueda parcial)"""
        query = """
        SELECT * FROM cursos 
        WHERE LOWER(nombre) LIKE %s
        ORDER BY nombre
        """
        search_term = f"%{nombre.lower()}%"
        results = self._execute_query(query, (search_term,))
        
        return list(map(self._row_to_curso, results))
    
    def _row_to_curso(self, row: tuple) -> Curso:
        """
        Convierte una fila de la base de datos a objeto Curso
        Mapeo objeto-relacional
        """
        # row = (id, codigo, nombre, creditos, profesor, horario, cupos_disponibles)
        curso = Curso(
            codigo=row[1],
            nombre=row[2],
            creditos=row[3],
            profesor=row[4] or "",
            horario=row[5] or "",
            cupos_disponibles=row[6]
        )
        
        # Calcular cupos ocupados basado en matrículas activas
        query_ocupados = """
        SELECT COUNT(*) FROM matriculas 
        WHERE curso_id = (SELECT id FROM cursos WHERE codigo = %s) 
        AND estado = 'ACTIVA'
        """
        try:
            results = self._execute_query(query_ocupados, (curso.codigo,))
            if results:
                curso._cupos_ocupados = results[0][0]
        except:
            # Si hay error, mantener en 0
            curso._cupos_ocupados = 0
        
        return curso
    
    def exists_codigo(self, codigo: str) -> bool:
        """Verifica si existe un curso con el código dado"""
        query = "SELECT COUNT(*) FROM cursos WHERE codigo = %s"
        results = self._execute_query(query, (codigo,))
        return results[0][0] > 0 if results else False
    
    def update_cupos_ocupados(self, curso_codigo: str) -> bool:
        """
        Actualiza el conteo de cupos ocupados para un curso
        Se llama después de cambios en matrículas
        """
        try:
            # Esta función se maneja automáticamente por las consultas
            # pero se puede usar para sincronización manual si es necesario
            return True
        except Exception as e:
            self.logger.error(f"Error actualizando cupos ocupados: {e}")
            return False