"""
Autor: Sistema de Matrículas Universitarias
Módulo: Modelo Estudiante
Descripción: Clase para representar y manejar estudiantes
Paradigmas: POO (herencia, encapsulación), Funcional (funciones de orden superior)
"""

from datetime import datetime
from typing import List, Dict, Optional
import re

class Persona:
    """
    Clase base para representar una persona
    Aplicación de herencia en POO
    """
    
    def __init__(self, nombre: str, apellido: str, email: str = "", telefono: str = ""):
        """Constructor de la clase Persona"""
        self._nombre = self._validar_nombre(nombre)
        self._apellido = self._validar_nombre(apellido)
        self._email = self._validar_email(email) if email else ""
        self._telefono = telefono
    
    def _validar_nombre(self, nombre: str) -> str:
        """
        Validación de entrada para nombres
        Manejo de errores y validaciones
        """
        if not nombre or not isinstance(nombre, str):
            raise ValueError("El nombre debe ser una cadena no vacía")
        
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
            
        return nombre.strip().title()
    
    def _validar_email(self, email: str) -> str:
        """Validación de formato de email usando expresiones regulares"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if email and not re.match(patron, email):
            raise ValueError("Formato de email inválido")
        return email.lower()
    
    # Propiedades (getters y setters) - Encapsulación
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def apellido(self) -> str:
        return self._apellido
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def telefono(self) -> str:
        return self._telefono

class Estudiante(Persona):
    """
    Clase Estudiante que hereda de Persona
    Implementa herencia y polimorfismo
    """
    
    def __init__(self, codigo: str, nombre: str, apellido: str, carrera: str, 
                 email: str = "", telefono: str = ""):
        """Constructor de la clase Estudiante"""
        super().__init__(nombre, apellido, email, telefono)
        self._codigo = self._validar_codigo(codigo)
        self._carrera = self._validar_carrera(carrera)
        self._fecha_registro = datetime.now()
        self._cursos_matriculados = []
    
    def _validar_codigo(self, codigo: str) -> str:
        """Validación del código de estudiante"""
        if not codigo or len(codigo) < 5:
            raise ValueError("El código debe tener al menos 5 caracteres")
        return codigo.upper()
    
    def _validar_carrera(self, carrera: str) -> str:
        """Validación de la carrera"""
        carreras_validas = [
            'INGENIERIA DE SISTEMAS', 'INGENIERIA INDUSTRIAL', 
            'ADMINISTRACION', 'CONTADURIA', 'DERECHO', 'MEDICINA',
            'PSICOLOGIA', 'ARQUITECTURA'
        ]
        
        carrera_upper = carrera.upper()
        if carrera_upper not in carreras_validas:
            # Programación funcional: uso de filter
            sugerencias = list(filter(lambda c: carrera_upper in c, carreras_validas))
            if sugerencias:
                print(f"¿Quizás quisiste decir: {', '.join(sugerencias)}?")
        
        return carrera.upper()
    
    @property
    def codigo(self) -> str:
        return self._codigo
    
    @property
    def carrera(self) -> str:
        return self._carrera
    
    @property
    def fecha_registro(self) -> datetime:
        return self._fecha_registro
    
    def agregar_curso(self, curso_codigo: str):
        """Agrega un curso a la lista de cursos matriculados"""
        if curso_codigo not in self._cursos_matriculados:
            self._cursos_matriculados.append(curso_codigo)
    
    def obtener_cursos(self) -> List[str]:
        """Retorna la lista de cursos matriculados"""
        return self._cursos_matriculados.copy()  # Inmutabilidad
    
    def to_dict(self) -> Dict:
        """
        Convierte el objeto a diccionario
        Útil para serialización y manejo de datos
        """
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'carrera': self.carrera,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_registro': self.fecha_registro.isoformat(),
            'cursos_matriculados': self.obtener_cursos()
        }
    
    def __str__(self) -> str:
        """Representación en cadena del estudiante"""
        return f"{self.codigo} - {self.nombre} {self.apellido} ({self.carrera})"
    
    def __repr__(self) -> str:
        """Representación técnica del objeto"""
        return f"Estudiante(codigo='{self.codigo}', nombre='{self.nombre}', apellido='{self.apellido}', carrera='{self.carrera}')"

# Funciones de orden superior para manejo de estudiantes
def filtrar_estudiantes_por_carrera(estudiantes: List[Estudiante], carrera: str) -> List[Estudiante]:
    """
    Programación funcional: función de orden superior usando filter
    Filtra estudiantes por carrera específica
    """
    return list(filter(lambda est: est.carrera == carrera.upper(), estudiantes))

def mapear_nombres_estudiantes(estudiantes: List[Estudiante]) -> List[str]:
    """
    Programación funcional: función de orden superior usando map
    Extrae solo los nombres completos de los estudiantes
    """
    return list(map(lambda est: f"{est.nombre} {est.apellido}", estudiantes))

def contar_estudiantes_por_carrera(estudiantes: List[Estudiante]) -> Dict[str, int]:
    """
    Función que cuenta estudiantes por carrera
    Uso de programación funcional con reduce conceptual
    """
    contador = {}
    for estudiante in estudiantes:
        carrera = estudiante.carrera
        contador[carrera] = contador.get(carrera, 0) + 1
    return contador