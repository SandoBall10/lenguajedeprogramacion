"""
Autor: Sistema de Matrículas Universitarias
Módulo: Modelo Matrícula
Descripción: Clase para representar y manejar matrículas
Paradigmas: POO, Funcional, Lógico
"""

from datetime import datetime
from typing import List, Dict, Optional, Tuple
from enum import Enum

class EstadoMatricula(Enum):
    """
    Enumeración para estados de matrícula
    Aplicación de tipos de datos y semántica del lenguaje
    """
    ACTIVA = "ACTIVA"
    CANCELADA = "CANCELADA"
    COMPLETADA = "COMPLETADA"

class Matricula:
    """
    Clase para representar una matrícula
    Relación entre estudiante y curso
    """
    
    def __init__(self, estudiante_codigo: str, curso_codigo: str, 
                 estado: EstadoMatricula = EstadoMatricula.ACTIVA):
        """Constructor de la clase Matrícula"""
        self._id = None  # Se asignará por la base de datos
        self._estudiante_codigo = self._validar_codigo(estudiante_codigo)
        self._curso_codigo = self._validar_codigo(curso_codigo)
        self._fecha_matricula = datetime.now()
        self._estado = estado
    
    def _validar_codigo(self, codigo: str) -> str:
        """Validación de códigos"""
        if not codigo or not codigo.strip():
            raise ValueError("El código no puede estar vacío")
        return codigo.strip().upper()
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, value: int):
        self._id = value
    
    @property
    def estudiante_codigo(self) -> str:
        return self._estudiante_codigo
    
    @property
    def curso_codigo(self) -> str:
        return self._curso_codigo
    
    @property
    def fecha_matricula(self) -> datetime:
        return self._fecha_matricula
    
    @property
    def estado(self) -> EstadoMatricula:
        return self._estado
    
    def cambiar_estado(self, nuevo_estado: EstadoMatricula) -> bool:
        """
        Cambia el estado de la matrícula aplicando reglas de negocio
        Simulación de programación lógica con reglas
        """
        # Reglas de transición de estados
        transiciones_validas = {
            EstadoMatricula.ACTIVA: [EstadoMatricula.CANCELADA, EstadoMatricula.COMPLETADA],
            EstadoMatricula.CANCELADA: [],  # No se puede cambiar desde cancelada
            EstadoMatricula.COMPLETADA: []  # No se puede cambiar desde completada
        }
        
        if nuevo_estado in transiciones_validas.get(self._estado, []):
            self._estado = nuevo_estado
            return True
        return False
    
    def esta_activa(self) -> bool:
        """Predicado: verifica si la matrícula está activa"""
        return self._estado == EstadoMatricula.ACTIVA
    
    def puede_ser_cancelada(self) -> bool:
        """Predicado: verifica si la matrícula puede ser cancelada"""
        return self._estado == EstadoMatricula.ACTIVA
    
    def to_dict(self) -> Dict:
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'estudiante_codigo': self.estudiante_codigo,
            'curso_codigo': self.curso_codigo,
            'fecha_matricula': self.fecha_matricula.isoformat(),
            'estado': self.estado.value
        }
    
    def __str__(self) -> str:
        """Representación en cadena de la matrícula"""
        return f"Matrícula: {self.estudiante_codigo} -> {self.curso_codigo} ({self.estado.value})"
    
    def __repr__(self) -> str:
        """Representación técnica del objeto"""
        return f"Matricula(estudiante='{self.estudiante_codigo}', curso='{self.curso_codigo}', estado='{self.estado.value}')"

# Funciones de orden superior y lógicas para manejo de matrículas
def filtrar_matriculas_activas(matriculas: List[Matricula]) -> List[Matricula]:
    """
    Programación funcional: filtra matrículas activas
    """
    return list(filter(lambda m: m.esta_activa(), matriculas))

def filtrar_matriculas_por_estudiante(matriculas: List[Matricula], estudiante_codigo: str) -> List[Matricula]:
    """
    Programación funcional: filtra matrículas de un estudiante específico
    """
    return list(filter(lambda m: m.estudiante_codigo == estudiante_codigo.upper(), matriculas))

def filtrar_matriculas_por_curso(matriculas: List[Matricula], curso_codigo: str) -> List[Matricula]:
    """
    Programación funcional: filtra matrículas de un curso específico
    """
    return list(filter(lambda m: m.curso_codigo == curso_codigo.upper(), matriculas))

def contar_matriculas_por_estado(matriculas: List[Matricula]) -> Dict[str, int]:
    """
    Cuenta matrículas agrupadas por estado
    Simulación de reduce
    """
    contador = {}
    for matricula in matriculas:
        estado = matricula.estado.value
        contador[estado] = contador.get(estado, 0) + 1
    return contador

def obtener_estadisticas_matriculas(matriculas: List[Matricula]) -> Dict[str, any]:
    """
    Genera estadísticas completas de matrículas
    Combinación de programación funcional y análisis de datos
    """
    total = len(matriculas)
    activas = len(filtrar_matriculas_activas(matriculas))
    
    # Usar funciones lambda para cálculos
    canceladas = len(list(filter(lambda m: m.estado == EstadoMatricula.CANCELADA, matriculas)))
    completadas = len(list(filter(lambda m: m.estado == EstadoMatricula.COMPLETADA, matriculas)))
    
    return {
        'total_matriculas': total,
        'matriculas_activas': activas,
        'matriculas_canceladas': canceladas,
        'matriculas_completadas': completadas,
        'porcentaje_activas': (activas / total * 100) if total > 0 else 0,
        'por_estado': contar_matriculas_por_estado(matriculas)
    }

# Predicados lógicos para validación de reglas de negocio
def puede_matricularse(estudiante_codigo: str, curso_codigo: str, matriculas_existentes: List[Matricula]) -> Tuple[bool, str]:
    """
    Predicado complejo que verifica si un estudiante puede matricularse en un curso
    Simulación de programación lógica con múltiples reglas
    """
    # Regla 1: No debe existir una matrícula activa previa
    matriculas_estudiante = filtrar_matriculas_por_estudiante(matriculas_existentes, estudiante_codigo)
    matriculas_activas_curso = list(filter(
        lambda m: m.curso_codigo == curso_codigo.upper() and m.esta_activa(), 
        matriculas_estudiante
    ))
    
    if matriculas_activas_curso:
        return False, "El estudiante ya está matriculado en este curso"
    
    # Regla 2: El estudiante no debe tener más de 6 materias activas (límite académico)
    matriculas_activas_estudiante = filtrar_matriculas_activas(matriculas_estudiante)
    if len(matriculas_activas_estudiante) >= 6:
        return False, "El estudiante ha alcanzado el límite máximo de materias (6)"
    
    return True, "Puede matricularse"

def validar_cancelacion_matricula(matricula: Matricula) -> Tuple[bool, str]:
    """
    Predicado que valida si una matrícula puede ser cancelada
    Aplicación de reglas de negocio
    """
    if not matricula.puede_ser_cancelada():
        return False, "La matrícula no está en estado activo"
    
    # Regla: No se puede cancelar después de cierto tiempo (ejemplo: 30 días)
    dias_transcurridos = (datetime.now() - matricula.fecha_matricula).days
    if dias_transcurridos > 30:
        return False, "No se puede cancelar después de 30 días de la matrícula"
    
    return True, "La matrícula puede ser cancelada"