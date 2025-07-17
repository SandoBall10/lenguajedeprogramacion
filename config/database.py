"""
Autor: Sistema de Matrículas Universitarias
Módulo: Configuración de Base de Datos
Descripción: Manejo de conexión a MySQL usando XAMPP
Paradigma: Orientado a Objetos
"""

import mysql.connector
from mysql.connector import Error
import logging

class DatabaseConfig:
    """
    Clase para manejar la configuración y conexión a la base de datos MySQL
    Aplica principios de POO: encapsulación y abstracción
    """
    
    def __init__(self):
        """Constructor de la clase DatabaseConfig"""
        self.host = 'localhost'
        self.database = 'sistema_matriculas'
        self.user = 'root'
        self.password = ''  # XAMPP por defecto no tiene contraseña
        self.port = 3306
        self.connection = None
        
        # Configurar logging para manejo de errores
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        """
        Establece conexión con la base de datos MySQL
        Manejo de errores y validaciones de entrada
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            
            if self.connection.is_connected():
                self.logger.info("Conexión exitosa a MySQL")
                return True
                
        except Error as e:
            self.logger.error(f"Error al conectar a MySQL: {e}")
            return False
    
    def disconnect(self):
        """Cierra la conexión a la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("Conexión cerrada")
    
    def get_connection(self):
        """Retorna la conexión activa"""
        return self.connection
    
    def create_database_and_tables(self):
        """
        Crea la base de datos y tablas necesarias
        Simulación de fases de traducción: definición de esquema
        """
        try:
            # Conectar sin especificar base de datos
            temp_connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )
            
            cursor = temp_connection.cursor()
            
            # Crear base de datos si no existe
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")
            
            # Crear tabla estudiantes
            create_estudiantes_table = """
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(10) UNIQUE NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                carrera VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                telefono VARCHAR(15),
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            # Crear tabla cursos
            create_cursos_table = """
            CREATE TABLE IF NOT EXISTS cursos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(10) UNIQUE NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                creditos INT NOT NULL,
                profesor VARCHAR(100),
                horario VARCHAR(50),
                cupos_disponibles INT DEFAULT 30
            )
            """
            
            # Crear tabla matriculas
            create_matriculas_table = """
            CREATE TABLE IF NOT EXISTS matriculas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                estudiante_id INT,
                curso_id INT,
                fecha_matricula TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                estado ENUM('ACTIVA', 'CANCELADA', 'COMPLETADA') DEFAULT 'ACTIVA',
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
                FOREIGN KEY (curso_id) REFERENCES cursos(id),
                UNIQUE KEY unique_matricula (estudiante_id, curso_id)
            )
            """
            
            # Ejecutar creación de tablas
            cursor.execute(create_estudiantes_table)
            cursor.execute(create_cursos_table)
            cursor.execute(create_matriculas_table)
            
            temp_connection.commit()
            cursor.close()
            temp_connection.close()
            
            self.logger.info("Base de datos y tablas creadas exitosamente")
            return True
            
        except Error as e:
            self.logger.error(f"Error al crear base de datos: {e}")
            return False
    
    def get_new_connection(self):
        """
        Obtiene una nueva conexión a la base de datos
        Método público para uso externo
        """
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            
            if connection.is_connected():
                return connection
            else:
                return None
                
        except Error as e:
            self.logger.error(f"Error al obtener nueva conexión: {e}")
            return None