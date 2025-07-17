"""
Autor: Sistema de Matrículas Universitarias
Módulo: Modelo Usuario
Descripción: Clase para representar usuarios del sistema con roles
Paradigmas: POO, Funcional
"""

from datetime import datetime
from typing import Dict, Optional
from enum import Enum
import hashlib
import re

class RolUsuario(Enum):
    """Enumeración para roles de usuario"""
    ADMINISTRADOR = "ADMINISTRADOR"
    ESTUDIANTE = "ESTUDIANTE"

class Usuario:
    """
    Clase para representar un usuario del sistema
    Implementa autenticación y autorización básica
    """
    
    def __init__(self, email: str, password: str, rol: RolUsuario, 
                 nombre: str = "", apellido: str = "", codigo_estudiante: str = ""):
        """Constructor de la clase Usuario"""
        self._id = None
        self._email = self._validar_email(email)
        self._password_hash = self._hash_password(password)
        self._rol = rol
        self._nombre = nombre
        self._apellido = apellido
        self._codigo_estudiante = codigo_estudiante if rol == RolUsuario.ESTUDIANTE else ""
        self._fecha_creacion = datetime.now()
        self._activo = True
    
    def _validar_email(self, email: str) -> str:
        """Validación de formato de email"""
        if not email or not isinstance(email, str):
            raise ValueError("El email debe ser una cadena no vacía")
        
        # Patrón básico de email
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            raise ValueError("Formato de email inválido")
        
        return email.lower()
    
    def _hash_password(self, password: str) -> str:
        """Hash de la contraseña usando SHA-256"""
        if not password or len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verificar_password(self, password: str) -> bool:
        """Verifica si la contraseña es correcta"""
        return self._password_hash == self._hash_password(password)
    
    def es_administrador(self) -> bool:
        """Predicado: verifica si el usuario es administrador"""
        return self._rol == RolUsuario.ADMINISTRADOR
    
    def es_estudiante(self) -> bool:
        """Predicado: verifica si el usuario es estudiante"""
        return self._rol == RolUsuario.ESTUDIANTE
    
    def puede_acceder_admin(self) -> bool:
        """Predicado: verifica si puede acceder a funciones de admin"""
        return self.es_administrador() and self._activo
    
    def puede_matricularse(self) -> bool:
        """Predicado: verifica si puede matricularse"""
        return self.es_estudiante() and self._activo and self._codigo_estudiante
    
    @property
    def id(self) -> Optional[int]:
        return self._id
    
    @id.setter
    def id(self, value: int):
        self._id = value
    
    @property
    def email(self) -> str:
        return self._email
    
    @property
    def rol(self) -> RolUsuario:
        return self._rol
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def apellido(self) -> str:
        return self._apellido
    
    @property
    def codigo_estudiante(self) -> str:
        return self._codigo_estudiante
    
    @property
    def activo(self) -> bool:
        return self._activo
    
    def to_dict(self) -> Dict:
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'email': self.email,
            'rol': self.rol.value,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'codigo_estudiante': self.codigo_estudiante,
            'activo': self.activo,
            'fecha_creacion': self._fecha_creacion.isoformat()
        }
    
    def __str__(self) -> str:
        """Representación en cadena del usuario"""
        return f"{self.email} ({self.rol.value})"
    
    def __repr__(self) -> str:
        """Representación técnica del objeto"""
        return f"Usuario(email='{self.email}', rol='{self.rol.value}')"

# Funciones de validación para estudiantes UTP
def es_email_utp(email: str) -> bool:
    """Predicado: verifica si el email es de dominio UTP"""
    return email.lower().endswith('@utp.edu.pe')

def validar_estudiante_utp(email: str, codigo: str) -> bool:
    """Valida que un estudiante pertenezca a UTP"""
    return es_email_utp(email) and codigo and len(codigo) >= 5