"""
Autor: Sistema de Matrículas Universitarias
Módulo: Servicio de Matrículas
Descripción: Lógica de negocio para matrículas
Paradigmas: POO, Funcional, Lógico
"""

from typing import List, Tuple, Dict, Optional
from models.estudiante import Estudiante
from models.curso import Curso
from models.matricula import Matricula, EstadoMatricula
from dao.estudiante_dao import EstudianteDAO
from dao.curso_dao import CursoDAO
from dao.matricula_dao import MatriculaDAO
import logging

class MatriculaService:
    """
    Servicio que maneja la lógica de negocio para matrículas
    Implementa reglas de negocio y validaciones complejas
    """
    
    def __init__(self):
        """Constructor del servicio de matrículas"""
        self.estudiante_dao = EstudianteDAO()
        self.curso_dao = CursoDAO()
        self.matricula_dao = MatriculaDAO()
        self.logger = logging.getLogger(__name__)
    
    def matricular_estudiante(self, estudiante_codigo: str, curso_codigo: str) -> Tuple[bool, str]:
        """
        Matricula un estudiante en un curso aplicando todas las reglas de negocio
        Simulación de programación lógica con múltiples predicados
        """
        try:
            # Predicado 1: Verificar que el estudiante existe
            estudiante = self.estudiante_dao.find_by_codigo(estudiante_codigo)
            if not estudiante:
                return False, f"Estudiante con código {estudiante_codigo} no encontrado"
            
            # Predicado 2: Verificar que el curso existe
            curso = self.curso_dao.find_by_codigo(curso_codigo)
            if not curso:
                return False, f"Curso con código {curso_codigo} no encontrado"
            
            # Predicado 3: Verificar que el curso tiene cupos disponibles
            if not curso.tiene_cupos_disponibles():
                return False, f"El curso {curso.nombre} no tiene cupos disponibles"
            
            # Predicado 4: Verificar que el estudiante no esté ya matriculado en el curso
            if self.matricula_dao.exists_matricula(estudiante_codigo, curso_codigo, EstadoMatricula.ACTIVA):
                return False, f"El estudiante ya está matriculado en el curso {curso.nombre}"
            
            # Predicado 5: Verificar límite de materias por estudiante (máximo 6)
            matriculas_activas = self.matricula_dao.count_active_matriculas_by_student(estudiante_codigo)
            if matriculas_activas >= 6:
                return False, "El estudiante ha alcanzado el límite máximo de 6 materias activas"
            
            # Predicado 6: Verificar prerrequisitos (simulación)
            if not self._verificar_prerrequisitos(estudiante, curso):
                return False, f"El estudiante no cumple los prerrequisitos para {curso.nombre}"
            
            # Si todas las validaciones pasan, crear la matrícula
            matricula = Matricula(estudiante_codigo, curso_codigo)
            matricula_id = self.matricula_dao.create(matricula)
            
            self.logger.info(f"Matrícula creada exitosamente: ID {matricula_id}")
            return True, f"Estudiante {estudiante.nombre} {estudiante.apellido} matriculado exitosamente en {curso.nombre}"
            
        except Exception as e:
            self.logger.error(f"Error en matrícula: {e}")
            return False, f"Error interno: {str(e)}"
    
    def cancelar_matricula(self, estudiante_codigo: str, curso_codigo: str) -> Tuple[bool, str]:
        """
        Cancela una matrícula aplicando reglas de negocio
        """
        try:
            # Verificar que existe la matrícula activa
            if not self.matricula_dao.exists_matricula(estudiante_codigo, curso_codigo, EstadoMatricula.ACTIVA):
                return False, "No existe una matrícula activa para cancelar"
            
            # Aplicar reglas de cancelación (ejemplo: no después de 30 días)
            matriculas = self.matricula_dao.find_by_estudiante(estudiante_codigo)
            matricula_activa = None
            
            # Programación funcional: filtrar matrícula específica
            matriculas_curso = list(filter(
                lambda m: m.curso_codigo == curso_codigo and m.esta_activa(), 
                matriculas
            ))
            
            if not matriculas_curso:
                return False, "No se encontró la matrícula activa"
            
            matricula_activa = matriculas_curso[0]
            
            # Verificar reglas de cancelación
            from models.matricula import validar_cancelacion_matricula
            puede_cancelar, mensaje = validar_cancelacion_matricula(matricula_activa)
            
            if not puede_cancelar:
                return False, mensaje
            
            # Proceder con la cancelación
            if self.matricula_dao.cancel_matricula(estudiante_codigo, curso_codigo):
                return True, "Matrícula cancelada exitosamente"
            else:
                return False, "Error al cancelar la matrícula"
                
        except Exception as e:
            self.logger.error(f"Error cancelando matrícula: {e}")
            return False, f"Error interno: {str(e)}"
    
    def obtener_matriculas_estudiante(self, estudiante_codigo: str) -> List[Dict]:
        """
        Obtiene todas las matrículas de un estudiante con información detallada
        """
        try:
            matriculas = self.matricula_dao.find_by_estudiante(estudiante_codigo)
            resultado = []
            
            for matricula in matriculas:
                curso = self.curso_dao.find_by_codigo(matricula.curso_codigo)
                if curso:
                    resultado.append({
                        'matricula_id': matricula.id,
                        'curso_codigo': curso.codigo,
                        'curso_nombre': curso.nombre,
                        'creditos': curso.creditos,
                        'profesor': curso.profesor,
                        'horario': curso.horario,
                        'fecha_matricula': matricula.fecha_matricula,
                        'estado': matricula.estado.value
                    })
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error obteniendo matrículas del estudiante: {e}")
            return []
    
    def obtener_estudiantes_curso(self, curso_codigo: str) -> List[Dict]:
        """
        Obtiene todos los estudiantes matriculados en un curso
        """
        try:
            matriculas = self.matricula_dao.find_by_curso(curso_codigo)
            resultado = []
            
            # Filtrar solo matrículas activas
            matriculas_activas = list(filter(lambda m: m.esta_activa(), matriculas))
            
            for matricula in matriculas_activas:
                estudiante = self.estudiante_dao.find_by_codigo(matricula.estudiante_codigo)
                if estudiante:
                    resultado.append({
                        'estudiante_codigo': estudiante.codigo,
                        'estudiante_nombre': f"{estudiante.nombre} {estudiante.apellido}",
                        'carrera': estudiante.carrera,
                        'email': estudiante.email,
                        'fecha_matricula': matricula.fecha_matricula
                    })
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error obteniendo estudiantes del curso: {e}")
            return []
    
    def generar_reporte_matriculas(self) -> Dict:
        """
        Genera un reporte completo de matrículas
        Uso de programación funcional para análisis de datos
        """
        try:
            # Obtener todas las matrículas
            matriculas = self.matricula_dao.find_all()
            
            # Estadísticas básicas
            total_matriculas = len(matriculas)
            matriculas_activas = list(filter(lambda m: m.esta_activa(), matriculas))
            matriculas_canceladas = list(filter(lambda m: m.estado == EstadoMatricula.CANCELADA, matriculas))
            matriculas_completadas = list(filter(lambda m: m.estado == EstadoMatricula.COMPLETADA, matriculas))
            
            # Análisis por carrera
            estudiantes_matriculados = set()
            carreras_stats = {}
            
            for matricula in matriculas_activas:
                estudiante = self.estudiante_dao.find_by_codigo(matricula.estudiante_codigo)
                if estudiante:
                    estudiantes_matriculados.add(estudiante.codigo)
                    carrera = estudiante.carrera
                    if carrera not in carreras_stats:
                        carreras_stats[carrera] = 0
                    carreras_stats[carrera] += 1
            
            # Análisis por curso
            cursos_stats = {}
            for matricula in matriculas_activas:
                curso_codigo = matricula.curso_codigo
                if curso_codigo not in cursos_stats:
                    cursos_stats[curso_codigo] = 0
                cursos_stats[curso_codigo] += 1
            
            return {
                'resumen': {
                    'total_matriculas': total_matriculas,
                    'matriculas_activas': len(matriculas_activas),
                    'matriculas_canceladas': len(matriculas_canceladas),
                    'matriculas_completadas': len(matriculas_completadas),
                    'estudiantes_con_matriculas': len(estudiantes_matriculados)
                },
                'por_carrera': carreras_stats,
                'por_curso': cursos_stats,
                'porcentajes': {
                    'activas': round((len(matriculas_activas) / total_matriculas * 100), 2) if total_matriculas > 0 else 0,
                    'canceladas': round((len(matriculas_canceladas) / total_matriculas * 100), 2) if total_matriculas > 0 else 0,
                    'completadas': round((len(matriculas_completadas) / total_matriculas * 100), 2) if total_matriculas > 0 else 0
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generando reporte: {e}")
            return {}
    
    def _verificar_prerrequisitos(self, estudiante: Estudiante, curso: Curso) -> bool:
        """
        Verifica prerrequisitos para un curso (simulación)
        Predicado lógico complejo
        """
        # Simulación de verificación de prerrequisitos
        # En un sistema real, esto consultaría una tabla de prerrequisitos
        
        # Reglas simuladas:
        # 1. Cursos avanzados requieren cursos básicos
        cursos_avanzados = ['MAT301', 'FIS301', 'QUI301']
        cursos_basicos_requeridos = ['MAT101', 'FIS101', 'QUI101']
        
        if curso.codigo in cursos_avanzados:
            # Verificar si el estudiante ha completado cursos básicos
            matriculas_estudiante = self.matricula_dao.find_by_estudiante(estudiante.codigo)
            cursos_completados = [
                m.curso_codigo for m in matriculas_estudiante 
                if m.estado == EstadoMatricula.COMPLETADA
            ]
            
            # Verificar si tiene al menos un curso básico completado
            tiene_basico = any(curso_basico in cursos_completados for curso_basico in cursos_basicos_requeridos)
            if not tiene_basico:
                return False
        
        # 2. Límite por carrera (simulación)
        if estudiante.carrera == 'MEDICINA' and curso.codigo.startswith('ING'):
            return False  # Estudiantes de medicina no pueden tomar cursos de ingeniería
        
        return True
    
    def obtener_cursos_disponibles_para_estudiante(self, estudiante_codigo: str) -> List[Dict]:
        """
        Obtiene cursos disponibles para un estudiante específico
        Aplicación de múltiples filtros y reglas de negocio
        """
        try:
            # Obtener estudiante
            estudiante = self.estudiante_dao.find_by_codigo(estudiante_codigo)
            if not estudiante:
                return []
            
            # Obtener todos los cursos con cupos
            cursos_con_cupos = self.curso_dao.find_with_available_spots()
            
            # Obtener cursos ya matriculados por el estudiante
            matriculas_activas = self.matricula_dao.find_by_estudiante(estudiante_codigo)
            cursos_matriculados = [m.curso_codigo for m in matriculas_activas if m.esta_activa()]
            
            # Filtrar cursos disponibles
            cursos_disponibles = []
            for curso in cursos_con_cupos:
                # No debe estar ya matriculado
                if curso.codigo in cursos_matriculados:
                    continue
                
                # Verificar prerrequisitos
                if not self._verificar_prerrequisitos(estudiante, curso):
                    continue
                
                cursos_disponibles.append({
                    'codigo': curso.codigo,
                    'nombre': curso.nombre,
                    'creditos': curso.creditos,
                    'profesor': curso.profesor,
                    'horario': curso.horario,
                    'cupos_disponibles': curso.cupos_disponibles
                })
            
            return cursos_disponibles
            
        except Exception as e:
            self.logger.error(f"Error obteniendo cursos disponibles: {e}")
            return []