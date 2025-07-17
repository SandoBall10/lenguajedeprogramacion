"""
Autor: Sistema de Matrículas Universitarias
Módulo: Servicio de Autenticación
Descripción: Lógica de negocio para autenticación y autorización
Paradigmas: POO, Funcional, Lógico
"""

from typing import Optional, Tuple, Dict
from models.usuario import Usuario, RolUsuario, es_email_utp, validar_estudiante_utp
from dao.usuario_dao import UsuarioDAO
from dao.estudiante_dao import EstudianteDAO
import logging

class AuthService:
    """
    Servicio que maneja la autenticación y autorización
    Implementa reglas de negocio para login y permisos
    """
    
    def __init__(self):
        """Constructor del servicio de autenticación"""
        self.usuario_dao = UsuarioDAO()
        self.estudiante_dao = EstudianteDAO()
        self.logger = logging.getLogger(__name__)
        self._usuario_actual = None
    
    def login(self, email: str, password: str) -> Tuple[bool, str, Optional[Usuario]]:
        """
        Autentica un usuario en el sistema
        Retorna (éxito, mensaje, usuario)
        """
        try:
            if not email or not password:
                return False, "Email y contraseña son requeridos", None
            
            # Intentar autenticar
            usuario = self.usuario_dao.authenticate(email, password)
            
            if not usuario:
                return False, "Credenciales inválidas", None
            
            if not usuario.activo:
                return False, "Usuario desactivado", None
            
            # Validaciones específicas para estudiantes
            if usuario.es_estudiante():
                if not es_email_utp(email):
                    return False, "Los estudiantes deben usar email @utp.edu.pe", None
                
                if not usuario.codigo_estudiante:
                    return False, "Estudiante sin código asignado", None
                
                # Verificar que el estudiante existe en la base de datos
                estudiante = self.estudiante_dao.find_by_codigo(usuario.codigo_estudiante)
                if not estudiante:
                    return False, "Estudiante no encontrado en el sistema", None
            
            self._usuario_actual = usuario
            self.logger.info(f"Login exitoso: {usuario.email} ({usuario.rol.value})")
            
            return True, f"Bienvenido {usuario.nombre or usuario.email}", usuario
            
        except Exception as e:
            self.logger.error(f"Error en login: {e}")
            return False, f"Error interno: {str(e)}", None
    
    def logout(self):
        """Cierra la sesión del usuario actual"""
        if self._usuario_actual:
            self.logger.info(f"Logout: {self._usuario_actual.email}")
            self._usuario_actual = None
    
    def get_usuario_actual(self) -> Optional[Usuario]:
        """Retorna el usuario actualmente logueado"""
        return self._usuario_actual
    
    def esta_logueado(self) -> bool:
        """Predicado: verifica si hay un usuario logueado"""
        return self._usuario_actual is not None
    
    def es_administrador_actual(self) -> bool:
        """Predicado: verifica si el usuario actual es administrador"""
        return (self._usuario_actual is not None and 
                self._usuario_actual.puede_acceder_admin())
    
    def es_estudiante_actual(self) -> bool:
        """Predicado: verifica si el usuario actual es estudiante"""
        return (self._usuario_actual is not None and 
                self._usuario_actual.puede_matricularse())
    
    def crear_usuario_admin(self, email: str, password: str, 
                           nombre: str = "", apellido: str = "") -> Tuple[bool, str]:
        """Crea un usuario administrador"""
        try:
            if self.usuario_dao.exists_email(email):
                return False, "Ya existe un usuario con ese email"
            
            usuario = Usuario(email, password, RolUsuario.ADMINISTRADOR, nombre, apellido)
            user_id = self.usuario_dao.create(usuario)
            
            return True, f"Administrador creado con ID: {user_id}"
            
        except Exception as e:
            self.logger.error(f"Error creando admin: {e}")
            return False, f"Error: {str(e)}"
    
    def crear_usuario_estudiante(self, email: str, password: str, codigo_estudiante: str,
                                nombre: str = "", apellido: str = "") -> Tuple[bool, str]:
        """Crea un usuario estudiante"""
        try:
            if not es_email_utp(email):
                return False, "Los estudiantes deben usar email @utp.edu.pe"
            
            if self.usuario_dao.exists_email(email):
                return False, "Ya existe un usuario con ese email"
            
            # Verificar que el estudiante existe
            estudiante = self.estudiante_dao.find_by_codigo(codigo_estudiante)
            if not estudiante:
                return False, f"No existe estudiante con código {codigo_estudiante}"
            
            # Usar datos del estudiante si no se proporcionan
            if not nombre:
                nombre = estudiante.nombre
            if not apellido:
                apellido = estudiante.apellido
            
            usuario = Usuario(email, password, RolUsuario.ESTUDIANTE, 
                            nombre, apellido, codigo_estudiante)
            user_id = self.usuario_dao.create(usuario)
            
            return True, f"Usuario estudiante creado con ID: {user_id}"
            
        except Exception as e:
            self.logger.error(f"Error creando estudiante: {e}")
            return False, f"Error: {str(e)}"
    
    def verificar_permisos_admin(self) -> Tuple[bool, str]:
        """Verifica si el usuario actual tiene permisos de administrador"""
        if not self.esta_logueado():
            return False, "Debe iniciar sesión"
        
        if not self.es_administrador_actual():
            return False, "Acceso denegado: se requieren permisos de administrador"
        
        return True, "Permisos verificados"
    
    def verificar_permisos_estudiante(self) -> Tuple[bool, str]:
        """Verifica si el usuario actual es un estudiante válido"""
        if not self.esta_logueado():
            return False, "Debe iniciar sesión"
        
        if not self.es_estudiante_actual():
            return False, "Acceso denegado: solo para estudiantes"
        
        return True, "Permisos verificados"
    
    def get_info_usuario_actual(self) -> Dict:
        """Retorna información del usuario actual"""
        if not self._usuario_actual:
            return {}
        
        info = {
            'email': self._usuario_actual.email,
            'rol': self._usuario_actual.rol.value,
            'nombre': self._usuario_actual.nombre,
            'apellido': self._usuario_actual.apellido
        }
        
        if self._usuario_actual.es_estudiante():
            info['codigo_estudiante'] = self._usuario_actual.codigo_estudiante
        
        return info