"""
Autor: Sistema de Matrículas Universitarias
Módulo: Modelo Curso
Descripción: Clase para representar y manejar cursos
Paradigmas: POO, Funcional
"""

from typing import List, Dict, Optional
from datetime import datetime

class Curso:
    """
    Clase para representar un curso universitario
    Aplicación de principios de POO: encapsulación y abstracción
    """
    
    def __init__(self, codigo: str, nombre: str, creditos: int, 
                 profesor: str = "", horario: str = "", cupos_disponibles: int = 30):
        """Constructor de la clase Curso"""
        self._codigo = self._validar_codigo(codigo)
        self._nombre = self._validar_nombre(nombre)
        self._creditos = self._validar_creditos(creditos)
        self._profesor = profesor
        self._horario = horario
        self._cupos_disponibles = cupos_disponibles
        self._cupos_ocupados = 0
        self._estudiantes_matriculados = []
    
    def _validar_codigo(self, codigo: str) -> str:
        """Validación del código del curso"""
        if not codigo or len(codigo) < 3:
            raise ValueError("El código del curso debe tener al menos 3 caracteres")
        return codigo.upper()
    
    def _validar_nombre(self, nombre: str) -> str:
        """Validación del nombre del curso"""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del curso no puede estar vacío")
        return nombre.strip().title()
    
    def _validar_creditos(self, creditos: int) -> int:
        """Validación del número de créditos"""
        if not isinstance(creditos, int) or creditos <= 0 or creditos > 6:
            raise ValueError("Los créditos deben ser un número entero entre 1 y 6")
        return creditos
    
    # Propiedades (getters) - Encapsulación
    @property
    def codigo(self) -> str:
        return self._codigo
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def creditos(self) -> int:
        return self._creditos
    
    @property
    def profesor(self) -> str:
        return self._profesor
    
    @property
    def horario(self) -> str:
        return self._horario
    
    @property
    def cupos_disponibles(self) -> int:
        return self._cupos_disponibles - self._cupos_ocupados
    
    @property
    def cupos_ocupados(self) -> int:
        return self._cupos_ocupados
    
    def tiene_cupos_disponibles(self) -> bool:
        """
        Predicado lógico: verifica si hay cupos disponibles
        Simulación de programación lógica
        """
        return self.cupos_disponibles > 0
    
    def puede_matricular_estudiante(self, estudiante_codigo: str) -> bool:
        """
        Predicado lógico: verifica si un estudiante puede matricularse
        Reglas de negocio simulando programación lógica
        """
        # Regla 1: Debe haber cupos disponibles
        if not self.tiene_cupos_disponibles():
            return False
        
        # Regla 2: El estudiante no debe estar ya matriculado
        if estudiante_codigo in self._estudiantes_matriculados:
            return False
        
        return True
    
    def matricular_estudiante(self, estudiante_codigo: str) -> bool:
        """
        Matricula un estudiante en el curso
        Aplicación de reglas lógicas
        """
        if self.puede_matricular_estudiante(estudiante_codigo):
            self._estudiantes_matriculados.append(estudiante_codigo)
            self._cupos_ocupados += 1
            return True
        return False
    
    def desmatricular_estudiante(self, estudiante_codigo: str) -> bool:
        """Desmatricula un estudiante del curso"""
        if estudiante_codigo in self._estudiantes_matriculados:
            self._estudiantes_matriculados.remove(estudiante_codigo)
            self._cupos_ocupados -= 1
            return True
        return False
    
    def obtener_estudiantes_matriculados(self) -> List[str]:
        """Retorna copia de la lista de estudiantes matriculados (inmutabilidad)"""
        return self._estudiantes_matriculados.copy()
    
    def to_dict(self) -> Dict:
        """Convierte el objeto a diccionario"""
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'creditos': self.creditos,
            'profesor': self.profesor,
            'horario': self.horario,
            'cupos_disponibles': self.cupos_disponibles,
            'cupos_ocupados': self.cupos_ocupados,
            'estudiantes_matriculados': self.obtener_estudiantes_matriculados()
        }
    
    def __str__(self) -> str:
        """Representación en cadena del curso"""
        return f"{self.codigo} - {self.nombre} ({self.creditos} créditos) - Cupos: {self.cupos_disponibles}"
    
    def __repr__(self) -> str:
        """Representación técnica del objeto"""
        return f"Curso(codigo='{self.codigo}', nombre='{self.nombre}', creditos={self.creditos})"

# Funciones de orden superior para manejo de cursos
def filtrar_cursos_por_creditos(cursos: List[Curso], min_creditos: int) -> List[Curso]:
    """
    Programación funcional: filtra cursos por número mínimo de créditos
    """
    return list(filter(lambda curso: curso.creditos >= min_creditos, cursos))

def obtener_cursos_con_cupos(cursos: List[Curso]) -> List[Curso]:
    """
    Programación funcional: filtra cursos que tienen cupos disponibles
    """
    return list(filter(lambda curso: curso.tiene_cupos_disponibles(), cursos))

def calcular_total_creditos(cursos: List[Curso]) -> int:
    """
    Programación funcional: calcula el total de créditos usando map y sum
    """
    creditos_list = list(map(lambda curso: curso.creditos, cursos))
    return sum(creditos_list)

def agrupar_cursos_por_creditos(cursos: List[Curso]) -> Dict[int, List[Curso]]:
    """
    Agrupa cursos por número de créditos
    Simulación de reduce usando programación imperativa
    """
    grupos = {}
    for curso in cursos:
        creditos = curso.creditos
        if creditos not in grupos:
            grupos[creditos] = []
        grupos[creditos].append(curso)
    return grupos