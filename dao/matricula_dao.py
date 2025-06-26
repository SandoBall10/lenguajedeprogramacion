"""
Autor: Sistema de Matrículas Universitarias
Módulo: DAO Matrícula
Descripción: Acceso a datos para matrículas
Paradigma: POO con herencia
"""

from typing import List, Optional, Tuple
from dao.base_dao import BaseDAO
from models.matricula import Matricula, EstadoMatricula

class MatriculaDAO(BaseDAO):
    """
    Clase para acceso a datos de matrículas
    Maneja las relaciones entre estudiantes y cursos
    """
    
    def create(self, matricula: Matricula) -> int:
        """Crea una nueva matrícula en la base de datos"""
        # Primero obtener los IDs de estudiante y curso
        estudiante_id = self._get_estudiante_id(matricula.estudiante_codigo)
        curso_id = self._get_curso_id(matricula.curso_codigo)
        
        if not estudiante_id or not curso_id:
            raise ValueError("Estudiante o curso no encontrado")
        
        query = """
        INSERT INTO matriculas (estudiante_id, curso_id, estado)
        VALUES (%s, %s, %s)
        """
        params = (estudiante_id, curso_id, matricula.estado.value)
        
        matricula_id = self._execute_insert_with_id(query, params)
        matricula.id = matricula_id
        return matricula_id
    
    def read(self, id: int) -> Optional[Matricula]:
        """Lee una matrícula por ID"""
        query = """
        SELECT m.id, e.codigo as estudiante_codigo, c.codigo as curso_codigo, 
               m.fecha_matricula, m.estado
        FROM matriculas m
        JOIN estudiantes e ON m.estudiante_id = e.id
        JOIN cursos c ON m.curso_id = c.id
        WHERE m.id = %s
        """
        results = self._execute_query(query, (id,))
        
        if results:
            return self._row_to_matricula(results[0])
        return None
    
    def update(self, matricula: Matricula) -> bool:
        """Actualiza una matrícula existente"""
        if not matricula.id:
            return False
        
        query = "UPDATE matriculas SET estado = %s WHERE id = %s"
        params = (matricula.estado.value, matricula.id)
        
        affected_rows = self._execute_update(query, params)
        return affected_rows > 0
    
    def delete(self, id: int) -> bool:
        """Elimina una matrícula por ID"""
        query = "DELETE FROM matriculas WHERE id = %s"
        affected_rows = self._execute_update(query, (id,))
        return affected_rows > 0
    
    def find_all(self) -> List[Matricula]:
        """Obtiene todas las matrículas"""
        query = """
        SELECT m.id, e.codigo as estudiante_codigo, c.codigo as curso_codigo, 
               m.fecha_matricula, m.estado
        FROM matriculas m
        JOIN estudiantes e ON m.estudiante_id = e.id
        JOIN cursos c ON m.curso_id = c.id
        ORDER BY m.fecha_matricula DESC
        """
        results = self._execute_query(query)
        
        return list(map(self._row_to_matricula, results))
    
    def find_by_estudiante(self, estudiante_codigo: str) -> List[Matricula]:
        """Busca matrículas de un estudiante específico"""
        query = """
        SELECT m.id, e.codigo as estudiante_codigo, c.codigo as curso_codigo, 
               m.fecha_matricula, m.estado
        FROM matriculas m
        JOIN estudiantes e ON m.estudiante_id = e.id
        JOIN cursos c ON m.curso_id = c.id
        WHERE e.codigo = %s
        ORDER BY m.fecha_matricula DESC
        """
        results = self._execute_query(query, (estudiante_codigo,))
        
        return list(map(self._row_to_matricula, results))
    
    def find_by_curso(self, curso_codigo: str) -> List[Matricula]:
        """Busca matrículas de un curso específico"""
        query = """
        SELECT m.id, e.codigo as estudiante_codigo, c.codigo as curso_codigo, 
               m.fecha_matricula, m.estado
        FROM matriculas m
        JOIN estudiantes e ON m.estudiante_id = e.id
        JOIN cursos c ON m.curso_id = c.id
        WHERE c.codigo = %s
        ORDER BY m.fecha_matricula DESC
        """
        results = self._execute_query(query, (curso_codigo,))
        
        return list(map(self._row_to_matricula, results))
    
    def find_active_matriculas(self) -> List[Matricula]:
        """Busca todas las matrículas activas"""
        query = """
        SELECT m.id, e.codigo as estudiante_codigo, c.codigo as curso_codigo, 
               m.fecha_matricula, m.estado
        FROM matriculas m
        JOIN estudiantes e ON m.estudiante_id = e.id
        JOIN cursos c ON m.curso_id = c.id
        WHERE m.estado = 'ACTIVA'
        ORDER BY m.fecha_matricula DESC
        """
        results = self._execute_query(query)
        
        return list(map(self._row_to_matricula, results))
    
    def exists_matricula(self, estudiante_codigo: str, curso_codigo: str, estado: EstadoMatricula = None) -> bool:
        """
        Verifica si existe una matrícula específica
        Predicado lógico para validación de reglas de negocio
        """
        if estado:
            query = """
            SELECT COUNT(*) FROM matriculas m
            JOIN estudiantes e ON m.estudiante_id = e.id
            JOIN cursos c ON m.curso_id = c.id
            WHERE e.codigo = %s AND c.codigo = %s AND m.estado = %s
            """
            params = (estudiante_codigo, curso_codigo, estado.value)
        else:
            query = """
            SELECT COUNT(*) FROM matriculas m
            JOIN estudiantes e ON m.estudiante_id = e.id
            JOIN cursos c ON m.curso_id = c.id
            WHERE e.codigo = %s AND c.codigo = %s
            """
            params = (estudiante_codigo, curso_codigo)
        
        results = self._execute_query(query, params)
        return results[0][0] > 0 if results else False
    
    def count_active_matriculas_by_student(self, estudiante_codigo: str) -> int:
        """Cuenta las matrículas activas de un estudiante"""
        query = """
        SELECT COUNT(*) FROM matriculas m
        JOIN estudiantes e ON m.estudiante_id = e.id
        WHERE e.codigo = %s AND m.estado = 'ACTIVA'
        """
        results = self._execute_query(query, (estudiante_codigo,))
        return results[0][0] if results else 0
    
    def get_enrollment_report(self) -> List[dict]:
        """
        Genera reporte completo de matrículas
        Uso de JOINs complejos y funciones de agregación
        """
        query = """
        SELECT 
            e.codigo as estudiante_codigo,
            CONCAT(e.nombre, ' ', e.apellido) as estudiante_nombre,
            e.carrera,
            c.codigo as curso_codigo,
            c.nombre as curso_nombre,
            c.creditos,
            m.fecha_matricula,
            m.estado
        FROM matriculas m
        JOIN estudiantes e ON m.estudiante_id = e.id
        JOIN cursos c ON m.curso_id = c.id
        ORDER BY e.apellido, e.nombre, m.fecha_matricula
        """
        results = self._execute_query(query)
        
        # Convertir a lista de diccionarios para fácil manejo
        report = []
        for row in results:
            report.append({
                'estudiante_codigo': row[0],
                'estudiante_nombre': row[1],
                'carrera': row[2],
                'curso_codigo': row[3],
                'curso_nombre': row[4],
                'creditos': row[5],
                'fecha_matricula': row[6],
                'estado': row[7]
            })
        
        return report
    
    def get_statistics(self) -> dict:
        """
        Obtiene estadísticas generales de matrículas
        Uso de funciones de agregación y subconsultas
        """
        queries = {
            'total_matriculas': "SELECT COUNT(*) FROM matriculas",
            'matriculas_activas': "SELECT COUNT(*) FROM matriculas WHERE estado = 'ACTIVA'",
            'matriculas_canceladas': "SELECT COUNT(*) FROM matriculas WHERE estado = 'CANCELADA'",
            'matriculas_completadas': "SELECT COUNT(*) FROM matriculas WHERE estado = 'COMPLETADA'",
            'estudiantes_con_matriculas': """
                SELECT COUNT(DISTINCT estudiante_id) FROM matriculas WHERE estado = 'ACTIVA'
            """,
            'cursos_con_matriculas': """
                SELECT COUNT(DISTINCT curso_id) FROM matriculas WHERE estado = 'ACTIVA'
            """
        }
        
        stats = {}
        for key, query in queries.items():
            results = self._execute_query(query)
            stats[key] = results[0][0] if results else 0
        
        # Calcular porcentajes
        total = stats['total_matriculas']
        if total > 0:
            stats['porcentaje_activas'] = round((stats['matriculas_activas'] / total) * 100, 2)
            stats['porcentaje_canceladas'] = round((stats['matriculas_canceladas'] / total) * 100, 2)
            stats['porcentaje_completadas'] = round((stats['matriculas_completadas'] / total) * 100, 2)
        else:
            stats['porcentaje_activas'] = 0
            stats['porcentaje_canceladas'] = 0
            stats['porcentaje_completadas'] = 0
        
        return stats
    
    def _get_estudiante_id(self, codigo: str) -> Optional[int]:
        """Obtiene el ID de un estudiante por su código"""
        query = "SELECT id FROM estudiantes WHERE codigo = %s"
        results = self._execute_query(query, (codigo,))
        return results[0][0] if results else None
    
    def _get_curso_id(self, codigo: str) -> Optional[int]:
        """Obtiene el ID de un curso por su código"""
        query = "SELECT id FROM cursos WHERE codigo = %s"
        results = self._execute_query(query, (codigo,))
        return results[0][0] if results else None
    
    def _row_to_matricula(self, row: tuple) -> Matricula:
        """
        Convierte una fila de la base de datos a objeto Matrícula
        """
        # row = (id, estudiante_codigo, curso_codigo, fecha_matricula, estado)
        matricula = Matricula(
            estudiante_codigo=row[1],
            curso_codigo=row[2],
            estado=EstadoMatricula(row[4])
        )
        
        matricula.id = row[0]
        matricula._fecha_matricula = row[3]
        
        return matricula
    
    def cancel_matricula(self, estudiante_codigo: str, curso_codigo: str) -> bool:
        """
        Cancela una matrícula activa
        Aplicación de reglas de negocio
        """
        query = """
        UPDATE matriculas m
        JOIN estudiantes e ON m.estudiante_id = e.id
        JOIN cursos c ON m.curso_id = c.id
        SET m.estado = 'CANCELADA'
        WHERE e.codigo = %s AND c.codigo = %s AND m.estado = 'ACTIVA'
        """
        
        affected_rows = self._execute_update(query, (estudiante_codigo, curso_codigo))
        return affected_rows > 0