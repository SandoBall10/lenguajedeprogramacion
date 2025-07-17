"""
Autor: Sistema de Matrículas Universitarias
Módulo: DAO Usuario
Descripción: Acceso a datos para usuarios
Paradigma: POO con herencia
"""

from typing import List, Optional
from dao.base_dao import BaseDAO
from models.usuario import Usuario, RolUsuario

class UsuarioDAO(BaseDAO):
    """
    Clase para acceso a datos de usuarios
    Maneja autenticación y autorización
    """
    
    def create(self, usuario: Usuario) -> int:
        """Crea un nuevo usuario en la base de datos"""
        query = """
        INSERT INTO usuarios (email, password_hash, rol, nombre, apellido, codigo_estudiante, activo)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            usuario.email,
            usuario._password_hash,
            usuario.rol.value,
            usuario.nombre,
            usuario.apellido,
            usuario.codigo_estudiante,
            usuario.activo
        )
        
        return self._execute_insert_with_id(query, params)
    
    def read(self, id: int) -> Optional[Usuario]:
        """Lee un usuario por ID"""
        query = "SELECT * FROM usuarios WHERE id = %s"
        results = self._execute_query(query, (id,))
        
        if results:
            return self._row_to_usuario(results[0])
        return None
    
    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Busca un usuario por email"""
        query = "SELECT * FROM usuarios WHERE email = %s AND activo = TRUE"
        results = self._execute_query(query, (email.lower(),))
        
        if results:
            return self._row_to_usuario(results[0])
        return None
    
    def authenticate(self, email: str, password: str) -> Optional[Usuario]:
        """
        Autentica un usuario con email y contraseña
        Retorna el usuario si las credenciales son válidas
        """
        usuario = self.find_by_email(email)
        if usuario and usuario.verificar_password(password):
            return usuario
        return None
    
    def update(self, usuario: Usuario) -> bool:
        """Actualiza un usuario existente"""
        query = """
        UPDATE usuarios 
        SET nombre = %s, apellido = %s, codigo_estudiante = %s, activo = %s
        WHERE email = %s
        """
        params = (
            usuario.nombre,
            usuario.apellido,
            usuario.codigo_estudiante,
            usuario.activo,
            usuario.email
        )
        
        affected_rows = self._execute_update(query, params)
        return affected_rows > 0
    
    def delete(self, id: int) -> bool:
        """Desactiva un usuario (soft delete)"""
        query = "UPDATE usuarios SET activo = FALSE WHERE id = %s"
        affected_rows = self._execute_update(query, (id,))
        return affected_rows > 0
    
    def find_all(self) -> List[Usuario]:
        """Obtiene todos los usuarios activos"""
        query = "SELECT * FROM usuarios WHERE activo = TRUE ORDER BY email"
        results = self._execute_query(query)
        
        return list(map(self._row_to_usuario, results))
    
    def find_by_rol(self, rol: RolUsuario) -> List[Usuario]:
        """Busca usuarios por rol"""
        query = "SELECT * FROM usuarios WHERE rol = %s AND activo = TRUE ORDER BY email"
        results = self._execute_query(query, (rol.value,))
        
        return list(map(self._row_to_usuario, results))
    
    def exists_email(self, email: str) -> bool:
        """Verifica si existe un usuario con el email dado"""
        query = "SELECT COUNT(*) FROM usuarios WHERE email = %s"
        results = self._execute_query(query, (email.lower(),))
        return results[0][0] > 0 if results else False
    
    def _row_to_usuario(self, row: tuple) -> Usuario:
        """
        Convierte una fila de la base de datos a objeto Usuario
        """
        # row = (id, email, password_hash, rol, nombre, apellido, codigo_estudiante, activo, fecha_creacion)
        usuario = Usuario.__new__(Usuario)  # Crear sin llamar __init__
        usuario._id = row[0]
        usuario._email = row[1]
        usuario._password_hash = row[2]
        usuario._rol = RolUsuario(row[3])
        usuario._nombre = row[4] or ""
        usuario._apellido = row[5] or ""
        usuario._codigo_estudiante = row[6] or ""
        usuario._activo = bool(row[7])
        usuario._fecha_creacion = row[8] if row[8] else None
        
        return usuario