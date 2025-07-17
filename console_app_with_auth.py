"""
Módulo: Aplicación de Consola con Autenticación
Descripción: Interfaz de consola con sistema de login y roles
Paradigmas: POO, Funcional, Lógico
"""

import os
import sys
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

# Importar módulos del sistema
from config.database import DatabaseConfig
from dao.estudiante_dao import EstudianteDAO
from dao.curso_dao import CursoDAO
from dao.matricula_dao import MatriculaDAO
from dao.usuario_dao import UsuarioDAO
from services.matricula_service import MatriculaService
from services.auth_service import AuthService
from models.estudiante import Estudiante
from models.curso import Curso
from models.matricula import EstadoMatricula
from models.usuario import Usuario, RolUsuario
from utils.data_analysis import DataAnalyzer
from utils.language_comparison import print_languages_comparison

# Códigos de colores ANSI
class Colors:
    """Clase para manejar colores en consola"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Colores de texto
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Colores de fondo
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'

def colored_text(text: str, color: str, bold: bool = False) -> str:
    """Retorna texto con color"""
    style = Colors.BOLD if bold else ""
    return f"{style}{color}{text}{Colors.RESET}"

class ConsoleAppWithAuth:
    """
    Aplicación de consola con sistema de autenticación
    Implementa diferentes interfaces según el rol del usuario
    """
    
    def __init__(self):
        """Constructor de la aplicación"""
        self.db_config = DatabaseConfig()
        self.estudiante_dao = EstudianteDAO()
        self.curso_dao = CursoDAO()
        self.matricula_dao = MatriculaDAO()
        self.usuario_dao = UsuarioDAO()
        self.matricula_service = MatriculaService()
        self.auth_service = AuthService()
        self.data_analyzer = DataAnalyzer()
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        self.running = True
    
    def initialize_database(self) -> bool:
        """Inicializa la base de datos incluyendo tabla de usuarios"""
        try:
            print(colored_text("Inicializando base de datos...", Colors.CYAN))
            
            if self.db_config.create_database_and_tables():
                # Crear tabla de usuarios
                self._create_users_table()
                # Crear usuario admin por defecto
                self._create_default_admin()
                print(colored_text("✓ Base de datos inicializada correctamente", Colors.GREEN))
                return True
            else:
                print(colored_text("✗ Error inicializando base de datos", Colors.RED))
                return False
                
        except Exception as e:
            print(colored_text(f"✗ Error crítico: {str(e)}", Colors.RED))
            return False
    
    def _create_users_table(self):
        """Crea la tabla de usuarios"""
        try:
            connection = self.db_config._get_connection()
            cursor = connection.cursor()
            
            create_users_table = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(64) NOT NULL,
                rol ENUM('ADMINISTRADOR', 'ESTUDIANTE') NOT NULL,
                nombre VARCHAR(100),
                apellido VARCHAR(100),
                codigo_estudiante VARCHAR(10),
                activo BOOLEAN DEFAULT TRUE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(create_users_table)
            connection.commit()
            cursor.close()
            connection.close()
            
        except Exception as e:
            self.logger.error(f"Error creando tabla usuarios: {e}")
    
    def _create_default_admin(self):
        """Crea un usuario administrador por defecto"""
        try:
            if not self.usuario_dao.exists_email("admin@sistema.com"):
                success, message = self.auth_service.crear_usuario_admin(
                    "admin@sistema.com", 
                    "admin123", 
                    "Administrador", 
                    "Sistema"
                )
                if success:
                    print(colored_text("✓ Usuario administrador creado: admin@sistema.com / admin123", Colors.GREEN))
        except Exception as e:
            self.logger.error(f"Error creando admin por defecto: {e}")
    
    def show_welcome_message(self):
        """Muestra mensaje de bienvenida"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        welcome_text = f"""
{colored_text('╔══════════════════════════════════════════════════════════════╗', Colors.CYAN, True)}
{colored_text('║              SISTEMA DE MATRÍCULAS UNIVERSITARIAS            ║', Colors.CYAN, True)}
{colored_text('║                        🎓 UTP - 2024 🎓                       ║', Colors.YELLOW, True)}
{colored_text('║                                                              ║', Colors.CYAN)}
{colored_text('║  Autor: Sistema de Matrículas Universitarias                 ║', Colors.WHITE)}
{colored_text('║  Lenguaje: Python 3.x                                        ║', Colors.WHITE)}
{colored_text('║  Paradigmas: POO, Funcional, Lógico                          ║', Colors.WHITE)}
{colored_text('║  Base de Datos: MySQL (XAMPP)                                ║', Colors.WHITE)}
{colored_text('║  Interfaz: Consola + GUI (tkinter)                           ║', Colors.WHITE)}
{colored_text('║                                                              ║', Colors.CYAN)}
{colored_text('╚══════════════════════════════════════════════════════════════╝', Colors.CYAN, True)}
        """
        
        print(welcome_text)
        print(colored_text("\nPresione Enter para continuar...", Colors.YELLOW))
        input()
    
    def show_login_screen(self) -> bool:
        """Muestra pantalla de login y maneja autenticación"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(colored_text("╔" + "═" * 50 + "╗", Colors.BLUE, True))
            print(colored_text("║" + " INICIAR SESIÓN".center(50) + "║", Colors.BLUE, True))
            print(colored_text("╚" + "═" * 50 + "╝", Colors.BLUE, True))
            
            print(colored_text("\n🔐 Credenciales por defecto:", Colors.YELLOW))
            print(colored_text("   Admin: admin@sistema.com / admin123", Colors.CYAN))
            print(colored_text("   Estudiante: Crear desde admin o usar existente", Colors.CYAN))
            
            email = input(colored_text("\n📧 Email: ", Colors.GREEN)).strip()
            if not email:
                continue
            
            import getpass
            password = getpass.getpass(colored_text("🔑 Contraseña: ", Colors.GREEN))
            if not password:
                continue
            
            # Intentar login
            success, message, usuario = self.auth_service.login(email, password)
            
            if success:
                print(colored_text(f"\n✓ {message}", Colors.GREEN, True))
                print(colored_text(f"Rol: {usuario.rol.value}", Colors.CYAN))
                input(colored_text("\nPresione Enter para continuar...", Colors.YELLOW))
                return True
            else:
                print(colored_text(f"\n✗ {message}", Colors.RED, True))
                
                retry = input(colored_text("\n¿Intentar nuevamente? (s/n): ", Colors.YELLOW)).strip().lower()
                if retry not in ['s', 'si', 'y', 'yes']:
                    return False
    
    def show_main_menu(self):
        """Muestra el menú principal según el rol del usuario"""
        while self.running:
            usuario = self.auth_service.get_usuario_actual()
            if not usuario:
                if not self.show_login_screen():
                    self.running = False
                    break
                continue
            
            if usuario.es_administrador():
                self.show_admin_menu()
            elif usuario.es_estudiante():
                self.show_student_menu()
    
    def show_admin_menu(self):
        """Menú principal para administradores"""
        usuario = self.auth_service.get_usuario_actual()
        
        while self.auth_service.esta_logueado():
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(colored_text("╔" + "═" * 60 + "╗", Colors.MAGENTA, True))
            print(colored_text("║" + f" PANEL ADMINISTRADOR - {usuario.nombre or usuario.email}".center(60) + "║", Colors.MAGENTA, True))
            print(colored_text("╚" + "═" * 60 + "╝", Colors.MAGENTA, True))
            
            menu_options = {
                '1': ('👥 Gestión de Estudiantes', Colors.CYAN),
                '2': ('📚 Gestión de Cursos', Colors.BLUE),
                '3': ('📝 Gestión de Matrículas', Colors.GREEN),
                '4': ('👤 Gestión de Usuarios', Colors.YELLOW),
                '5': ('📊 Reportes y Estadísticas', Colors.MAGENTA),
                '6': ('🖼️  Interfaz Gráfica', Colors.CYAN),
                '7': ('🔧 Configuración', Colors.WHITE),
                '8': ('🚪 Cerrar Sesión', Colors.RED),
                '0': ('❌ Salir', Colors.RED)
            }
            
            for key, (text, color) in menu_options.items():
                print(colored_text(f" {key}. {text}", color))
            
            choice = input(colored_text("\n🔹 Seleccione una opción: ", Colors.WHITE)).strip()
            
            if choice == '1':
                self.student_management_menu()
            elif choice == '2':
                self.course_management_menu()
            elif choice == '3':
                self.enrollment_management_menu()
            elif choice == '4':
                self.user_management_menu()
            elif choice == '5':
                self.reports_menu()
            elif choice == '6':
                self.launch_gui()
            elif choice == '7':
                self.configuration_menu()
            elif choice == '8':
                self.auth_service.logout()
                print(colored_text("✓ Sesión cerrada", Colors.GREEN))
                input(colored_text("Presione Enter para continuar...", Colors.YELLOW))
                break
            elif choice == '0':
                self.exit_application()
            else:
                print(colored_text("❌ Opción inválida", Colors.RED))
                input(colored_text("Presione Enter para continuar...", Colors.YELLOW))
    
    def show_student_menu(self):
        """Menú principal para estudiantes"""
        usuario = self.auth_service.get_usuario_actual()
        
        while self.auth_service.esta_logueado():
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(colored_text("╔" + "═" * 60 + "╗", Colors.BLUE, True))
            print(colored_text("║" + f" PORTAL ESTUDIANTE - {usuario.nombre or usuario.email}".center(60) + "║", Colors.BLUE, True))
            print(colored_text("║" + f" Código: {usuario.codigo_estudiante}".center(60) + "║", Colors.CYAN))
            print(colored_text("╚" + "═" * 60 + "╝", Colors.BLUE, True))
            
            menu_options = {
                '1': ('📚 Mis Cursos Matriculados', Colors.GREEN),
                '2': ('➕ Matricularme en Cursos', Colors.BLUE),
                '3': ('❌ Cancelar Matrícula', Colors.RED),
                '4': ('📊 Mi Historial Académico', Colors.MAGENTA),
                '5': ('🔍 Buscar Cursos Disponibles', Colors.CYAN),
                '6': ('🚪 Cerrar Sesión', Colors.RED),
                '0': ('❌ Salir', Colors.RED)
            }
            
            for key, (text, color) in menu_options.items():
                print(colored_text(f" {key}. {text}", color))
            
            choice = input(colored_text("\n🔹 Seleccione una opción: ", Colors.WHITE)).strip()
            
            if choice == '1':
                self.show_student_enrollments()
            elif choice == '2':
                self.student_enroll_in_course()
            elif choice == '3':
                self.student_cancel_enrollment()
            elif choice == '4':
                self.show_student_history()
            elif choice == '5':
                self.show_available_courses_for_student()
            elif choice == '6':
                self.auth_service.logout()
                print(colored_text("✓ Sesión cerrada", Colors.GREEN))
                input(colored_text("Presione Enter para continuar...", Colors.YELLOW))
                break
            elif choice == '0':
                self.exit_application()
            else:
                print(colored_text("❌ Opción inválida", Colors.RED))
                input(colored_text("Presione Enter para continuar...", Colors.YELLOW))
    
    def show_student_enrollments(self):
        """Muestra los cursos matriculados del estudiante"""
        print(colored_text("\n" + "═" * 80, Colors.BLUE))
        print(colored_text("📚 MIS CURSOS MATRICULADOS", Colors.BLUE, True))
        print(colored_text("═" * 80, Colors.BLUE))
        
        try:
            usuario = self.auth_service.get_usuario_actual()
            matriculas = self.matricula_service.obtener_matriculas_estudiante(usuario.codigo_estudiante)
            
            if not matriculas:
                print(colored_text("📝 No tienes cursos matriculados actualmente.", Colors.YELLOW))
            else:
                # Filtrar solo matrículas activas
                matriculas_activas = [m for m in matriculas if m['estado'] == 'ACTIVA']
                
                if not matriculas_activas:
                    print(colored_text("📝 No tienes cursos activos actualmente.", Colors.YELLOW))
                else:
                    print(colored_text(f"{'Código':<10} {'Curso':<30} {'Créd.':<6} {'Profesor':<20} {'Fecha':<12} {'Estado':<10}", Colors.CYAN, True))
                    print(colored_text("-" * 100, Colors.WHITE))
                    
                    for matricula in matriculas_activas:
                        fecha_str = matricula['fecha_matricula'].strftime('%Y-%m-%d')
                        estado_color = Colors.GREEN if matricula['estado'] == 'ACTIVA' else Colors.RED
                        
                        print(f"{colored_text(matricula['curso_codigo'], Colors.BLUE):<20} "
                              f"{colored_text(matricula['curso_nombre'][:28], Colors.WHITE):<40} "
                              f"{colored_text(str(matricula['creditos']), Colors.YELLOW):<10} "
                              f"{colored_text(matricula['profesor'][:18], Colors.CYAN):<30} "
                              f"{colored_text(fecha_str, Colors.MAGENTA):<20} "
                              f"{colored_text(matricula['estado'], estado_color):<20}")
                    
                    total_creditos = sum(m['creditos'] for m in matriculas_activas)
                    print(colored_text(f"\n📊 Total de créditos matriculados: {total_creditos}", Colors.GREEN, True))
                
                # Mostrar también historial completo
                matriculas_historicas = [m for m in matriculas if m['estado'] != 'ACTIVA']
                if matriculas_historicas:
                    print(colored_text(f"\n📜 HISTORIAL DE MATRÍCULAS:", Colors.MAGENTA, True))
                    for matricula in matriculas_historicas:
                        fecha_str = matricula['fecha_matricula'].strftime('%Y-%m-%d')
                        estado_color = Colors.YELLOW if matricula['estado'] == 'COMPLETADA' else Colors.RED
                        print(f"  {colored_text(matricula['curso_codigo'], Colors.BLUE)} - "
                              f"{colored_text(matricula['curso_nombre'], Colors.WHITE)} "
                              f"({colored_text(matricula['estado'], estado_color)}) - {fecha_str}")
                
        except Exception as e:
            print(colored_text(f"❌ Error obteniendo matrículas: {str(e)}", Colors.RED))
        
        input(colored_text("\nPresione Enter para continuar...", Colors.YELLOW))
    
    def student_enroll_in_course(self):
        """Permite al estudiante matricularse en un curso"""
        print(colored_text("\n" + "═" * 60, Colors.GREEN))
        print(colored_text("➕ MATRICULARME EN CURSO", Colors.GREEN, True))
        print(colored_text("═" * 60, Colors.GREEN))
        
        try:
            usuario = self.auth_service.get_usuario_actual()
            cursos_disponibles = self.matricula_service.obtener_cursos_disponibles_para_estudiante(usuario.codigo_estudiante)
            
            if not cursos_disponibles:
                print(colored_text("📝 No hay cursos disponibles para matrícula en este momento.", Colors.YELLOW))
                input(colored_text("\nPresione Enter para continuar...", Colors.YELLOW))
                return
            
            print(colored_text("📚 CURSOS DISPONIBLES PARA MATRÍCULA:", Colors.CYAN, True))
            print(colored_text(f"{'#':<3} {'Código':<10} {'Curso':<35} {'Créd.':<6} {'Profesor':<20} {'Cupos':<8}", Colors.CYAN))
            print(colored_text("-" * 90, Colors.WHITE))
            
            for i, curso in enumerate(cursos_disponibles, 1):
                print(f"{colored_text(str(i), Colors.YELLOW):<5} "
                      f"{colored_text(curso['codigo'], Colors.BLUE):<12} "
                      f"{colored_text(curso['nombre'][:33], Colors.WHITE):<37} "
                      f"{colored_text(str(curso['creditos']), Colors.GREEN):<8} "
                      f"{colored_text(curso['profesor'][:18], Colors.CYAN):<22} "
                      f"{colored_text(str(curso['cupos_disponibles']), Colors.MAGENTA):<10}")
            
            # Seleccionar curso
            while True:
                try:
                    seleccion = input(colored_text(f"\n🔹 Seleccione curso (1-{len(cursos_disponibles)}) o 0 para cancelar: ", Colors.WHITE)).strip()
                    
                    if seleccion == '0':
                        return
                    
                    curso_idx = int(seleccion) - 1
                    if 0 <= curso_idx < len(cursos_disponibles):
                        curso_seleccionado = cursos_disponibles[curso_idx]
                        break
                    else:
                        print(colored_text("❌ Número inválido. Intente nuevamente.", Colors.RED))
                except ValueError:
                    print(colored_text("❌ Ingrese un número válido.", Colors.RED))
            
            # Mostrar detalles y confirmar
            print(colored_text(f"\n📋 DETALLES DEL CURSO SELECCIONADO:", Colors.CYAN, True))
            print(f"  {colored_text('Código:', Colors.BLUE)} {curso_seleccionado['codigo']}")
            print(f"  {colored_text('Nombre:', Colors.BLUE)} {curso_seleccionado['nombre']}")
            print(f"  {colored_text('Créditos:', Colors.BLUE)} {curso_seleccionado['creditos']}")
            print(f"  {colored_text('Profesor:', Colors.BLUE)} {curso_seleccionado['profesor']}")
            print(f"  {colored_text('Horario:', Colors.BLUE)} {curso_seleccionado['horario']}")
            print(f"  {colored_text('Cupos disponibles:', Colors.BLUE)} {curso_seleccionado['cupos_disponibles']}")
            
            confirmar = input(colored_text(f"\n✅ ¿Confirmar matrícula en {curso_seleccionado['nombre']}? (s/n): ", Colors.GREEN)).strip().lower()
            
            if confirmar in ['s', 'si', 'y', 'yes']:
                success, message = self.matricula_service.matricular_estudiante(
                    usuario.codigo_estudiante,
                    curso_seleccionado['codigo']
                )
                
                if success:
                    print(colored_text(f"\n🎉 {message}", Colors.GREEN, True))
                else:
                    print(colored_text(f"\n❌ {message}", Colors.RED, True))
            else:
                print(colored_text("❌ Matrícula cancelada.", Colors.YELLOW))
                
        except Exception as e:
            print(colored_text(f"❌ Error en matrícula: {str(e)}", Colors.RED))
        
        input(colored_text("\nPresione Enter para continuar...", Colors.YELLOW))
    
    def student_cancel_enrollment(self):
        """Permite al estudiante cancelar una matrícula"""
        print(colored_text("\n" + "═" * 60, Colors.RED))
        print(colored_text("❌ CANCELAR MATRÍCULA", Colors.RED, True))
        print(colored_text("═" * 60, Colors.RED))
        
        try:
            usuario = self.auth_service.get_usuario_actual()
            matriculas = self.matricula_service.obtener_matriculas_estudiante(usuario.codigo_estudiante)
            matriculas_activas = [m for m in matriculas if m['estado'] == 'ACTIVA']
            
            if not matriculas_activas:
                print(colored_text("📝 No tienes matrículas activas para cancelar.", Colors.YELLOW))
                input(colored_text("\nPresione Enter para continuar...", Colors.YELLOW))
                return
            
            print(colored_text("📚 TUS MATRÍCULAS ACTIVAS:", Colors.CYAN, True))
            print(colored_text(f"{'#':<3} {'Código':<10} {'Curso':<35} {'Profesor':<20} {'Fecha':<12}", Colors.CYAN))
            print(colored_text("-" * 85, Colors.WHITE))
            
            for i, matricula in enumerate(matriculas_activas, 1):
                fecha_str = matricula['fecha_matricula'].strftime('%Y-%m-%d')
                print(f"{colored_text(str(i), Colors.YELLOW):<5} "
                      f"{colored_text(matricula['curso_codigo'], Colors.BLUE):<12} "
                      f"{colored_text(matricula['curso_nombre'][:33], Colors.WHITE):<37} "
                      f"{colored_text(matricula['profesor'][:18], Colors.CYAN):<22} "
                      f"{colored_text(fecha_str, Colors.MAGENTA):<14}")
            
            # Seleccionar matrícula a cancelar
            while True:
                try:
                    seleccion = input(colored_text(f"\n🔹 Seleccione matrícula a cancelar (1-{len(matriculas_activas)}) o 0 para volver: ", Colors.WHITE)).strip()
                    
                    if seleccion == '0':
                        return
                    
                    matricula_idx = int(seleccion) - 1
                    if 0 <= matricula_idx < len(matriculas_activas):
                        matricula_seleccionada = matriculas_activas[matricula_idx]
                        break
                    else:
                        print(colored_text("❌ Número inválido. Intente nuevamente.", Colors.RED))
                except ValueError:
                    print(colored_text("❌ Ingrese un número válido.", Colors.RED))
            
            # Confirmar cancelación
            print(colored_text(f"\n⚠️  CONFIRMAR CANCELACIÓN:", Colors.YELLOW, True))
            print(f"  {colored_text('Curso:', Colors.RED)} {matricula_seleccionada['curso_nombre']}")
            print(f"  {colored_text('Código:', Colors.RED)} {matricula_seleccionada['curso_codigo']}")
            print(f"  {colored_text('Profesor:', Colors.RED)} {matricula_seleccionada['profesor']}")
            
            print(colored_text("\n⚠️  ADVERTENCIA: Esta acción no se puede deshacer.", Colors.RED, True))
            
            confirmar = input(colored_text(f"\n❌ ¿Confirmar cancelación de {matricula_seleccionada['curso_nombre']}? (s/n): ", Colors.RED)).strip().lower()
            
            if confirmar in ['s', 'si', 'y', 'yes']:
                success, message = self.matricula_service.cancelar_matricula(
                    usuario.codigo_estudiante,
                    matricula_seleccionada['curso_codigo']
                )
                
                if success:
                    print(colored_text(f"\n✅ {message}", Colors.GREEN, True))
                else:
                    print(colored_text(f"\n❌ {message}", Colors.RED, True))
            else:
                print(colored_text("✅ Cancelación abortada.", Colors.GREEN))
                
        except Exception as e:
            print(colored_text(f"❌ Error cancelando matrícula: {str(e)}", Colors.RED))
        
        input(colored_text("\nPresione Enter para continuar...", Colors.YELLOW))
    
    def show_student_history(self):
        """Muestra el historial académico completo del estudiante"""
        print(colored_text("\n" + "═" * 80, Colors.MAGENTA))
        print(colored_text("📊 MI HISTORIAL ACADÉMICO", Colors.MAGENTA, True))
        print(colored_text("═" * 80, Colors.MAGENTA))
        
        try:
            usuario = self.auth_service.get_usuario_actual()
            matriculas = self.matricula_service.obtener_matriculas_estudiante(usuario.codigo_estudiante)
            
            if not matriculas:
                print(colored_text("📝 No tienes historial académico registrado.", Colors.YELLOW))
                input(colored_text("\nPresione Enter para continuar...", Colors.YELLOW))
                return
            
            # Estadísticas generales
            total_matriculas = len(matriculas)
            activas = len([m for m in matriculas if m['estado'] == 'ACTIVA'])
            completadas = len([m for m in matriculas if m['estado'] == 'COMPLETADA'])
            canceladas = len([m for m in matriculas if m['estado'] == 'CANCELADA'])
            total_creditos = sum(m['creditos'] for m in matriculas if m['estado'] in ['ACTIVA', 'COMPLETADA'])
            
            print(colored_text("📈 RESUMEN ACADÉMICO:", Colors.CYAN, True))
            print(f"  {colored_text('Total de matrículas:', Colors.BLUE)} {total_matriculas}")
            print(f"  {colored_text('Cursos activos:', Colors.GREEN)} {activas}")
            print(f"  {colored_text('Cursos completados:', Colors.MAGENTA)} {completadas}")
            print(f"  {colored_text('Cursos cancelados:', Colors.RED)} {canceladas}")
            print(f"  {colored_text('Total créditos:', Colors.YELLOW)} {total_creditos}")
            
            # Historial detallado
            print(colored_text(f"\n📜 HISTORIAL DETALLADO:", Colors.CYAN, True))
            print(colored_text(f"{'Código':<10} {'Curso':<30} {'Créd.':<6} {'Profesor':<20} {'Fecha':<12} {'Estado':<12}", Colors.CYAN))
            print(colored_text("-" * 100, Colors.WHITE))
            
            # Ordenar por fecha (más reciente primero)
            matriculas_ordenadas = sorted(matriculas, key=lambda x: x['fecha_matricula'], reverse=True)
            
            for matricula in matriculas_ordenadas:
                fecha_str = matricula['fecha_matricula'].strftime('%Y-%m-%d')
                
                if matricula['estado'] == 'ACTIVA':
                    estado_color = Colors.GREEN
                elif matricula['estado'] == 'COMPLETADA':
                    estado_color = Colors.MAGENTA
                else:
                    estado_color = Colors.RED
                
                print(f"{colored_text(matricula['curso_codigo'], Colors.BLUE):<20} "
                      f"{colored_text(matricula['curso_nombre'][:28], Colors.WHITE):<40} "
                      f"{colored_text(str(matricula['creditos']), Colors.YELLOW):<10} "
                      f"{colored_text(matricula['profesor'][:18], Colors.CYAN):<30} "
                      f"{colored_text(fecha_str, Colors.WHITE):<20} "
                      f"{colored_text(matricula['estado'], estado_color):<20}")
            
        except Exception as e:
            print(colored_text(f"❌ Error obteniendo historial: {str(e)}", Colors.RED))
        
        input(colored_text("\nPresione Enter para continuar...", Colors.YELLOW))
    
    def show_available_courses_for_student(self):
        """Muestra cursos disponibles para el estudiante"""
        print(colored_text("\n" + "═" * 80, Colors.CYAN))
        print(colored_text("🔍 CURSOS DISPONIBLES", Colors.CYAN, True))
        print(colored_text("═" * 80, Colors.CYAN))
        
        try:
            usuario = self.auth_service.get_usuario_actual()
            cursos_disponibles = self.matricula_service.obtener_cursos_disponibles_para_estudiante(usuario.codigo_estudiante)
            
            if not cursos_disponibles:
                print(colored_text("📝 No hay cursos disponibles para matrícula en este momento.", Colors.YELLOW))
            else:
                print(colored_text(f"📚 Encontrados {len(cursos_disponibles)} cursos disponibles:", Colors.GREEN, True))
                print(colored_text(f"{'Código':<10} {'Curso':<35} {'Créd.':<6} {'Profesor':<20} {'Cupos':<8}", Colors.CYAN))
                print(colored_text("-" * 85, Colors.WHITE))
                
                for curso in cursos_disponibles:
                    print(f"{colored_text(curso['codigo'], Colors.BLUE):<20} "
                          f"{colored_text(curso['nombre'][:33], Colors.WHITE):<45} "
                          f"{colored_text(str(curso['creditos']), Colors.YELLOW):<10} "
                          f"{colored_text(curso['profesor'][:18], Colors.CYAN):<30} "
                          f"{colored_text(str(curso['cupos_disponibles']), Colors.MAGENTA):<10}")
                
                print(colored_text(f"\n💡 Tip: Usa la opción 'Matricularme en Cursos' para inscribirte.", Colors.YELLOW))
            
        except Exception as e:
            print(colored_text(f"❌ Error obteniendo cursos: {str(e)}", Colors.RED))
        
        input(colored_text("\nPresione Enter para continuar...", Colors.YELLOW))
    
    def user_management_menu(self):
        """Menú de gestión de usuarios (solo admin)"""
        if not self.auth_service.es_administrador_actual():
            print(colored_text("❌ Acceso denegado", Colors.RED))
            return
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(colored_text("╔" + "═" * 50 + "╗", Colors.YELLOW, True))
            print(colored_text("║" + " GESTIÓN DE USUARIOS".center(50) + "║", Colors.YELLOW, True))
            print(colored_text("╚" + "═" * 50 + "╝", Colors.YELLOW, True))
            
            menu_options = [
                ("1", "👤 Crear Usuario Administrador", Colors.MAGENTA),
                ("2", "🎓 Crear Usuario Estudiante", Colors.BLUE),
                ("3", "📋 Listar Usuarios", Colors.CYAN),
                ("4", "🔍 Buscar Usuario", Colors.GREEN),
                ("5", "❌ Desactivar Usuario", Colors.RED),
                ("0", "🔙 Volver", Colors.WHITE)
            ]
            
            for key, text, color in menu_options:
                print(colored_text(f" {key}. {text}", color))
            
            choice = input(colored_text("\n🔹 Seleccione una opción: ", Colors.WHITE)).strip()
            
            if choice == '1':
                self.create_admin_user()
            elif choice == '2':
                self.create_student_user()
            elif choice == '3':
                self.list_users()
            elif choice == '4':
                self.search_user()
            elif choice == '5':
                self.deactivate_user()
            elif choice == '0':
                break
            else:
                print(colored_text("❌ Opción inválida", Colors.RED))
                input(colored_text("Presione Enter para continuar...", Colors.YELLOW))
    
    def create_student_user(self):
        """Crea un usuario estudiante"""
        print(colored_text("\n" + "═" * 60, Colors.BLUE))
        print(colored_text("🎓 CREAR USUARIO ESTUDIANTE", Colors.BLUE, True))
        print(colored_text("═" * 60, Colors.BLUE))
        
        try:
            email = input(colored_text("📧 Email (@utp.edu.pe): ", Colors.GREEN)).strip()
            if not email.endswith('@utp.edu.pe'):
                print(colored_text("❌ Los estudiantes deben usar email @utp.edu.pe", Colors.RED))
                input(colored_text("Presione Enter para continuar...", Colors.YELLOW))
                return
            
            password = input(colored_text("🔑 Contraseña: ", Colors.GREEN)).strip()
            codigo = input(colored_text("🆔 Código de estudiante: ", Colors.GREEN)).strip().upper()
            nombre = input(colored_text("👤 Nombre (opcional): ", Colors.GREEN)).strip()
            apellido = input(colored_text("👤 Apellido (opcional): ", Colors.GREEN)).strip()
            
            success, message = self.auth_service.crear_usuario_estudiante(
                email, password, codigo, nombre, apellido
            )
            
            if success:
                print(colored_text(f"\n✅ {message}", Colors.GREEN, True))
            else:
                print(colored_text(f"\n❌ {message}", Colors.RED, True))
                
        except Exception as e:
            print(colored_text(f"❌ Error: {str(e)}", Colors.RED))
        
        input(colored_text("\nPresione Enter para continuar...", Colors.YELLOW))
    
    # Métodos heredados de la versión original (con colores añadidos)
    def student_management_menu(self):
        """Menú de gestión de estudiantes con colores"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(colored_text("╔" + "═" * 50 + "╗", Colors.CYAN, True))
            print(colored_text("║" + " GESTIÓN DE ESTUDIANTES".center(50) + "║", Colors.CYAN, True))
            print(colored_text("╚" + "═" * 50 + "╝", Colors.CYAN, True))
            
            menu_options = [
                ("1", "➕ Registrar Estudiante", Colors.GREEN),
                ("2", "📋 Listar Estudiantes", Colors.BLUE),
                ("3", "🔍 Buscar Estudiante", Colors.YELLOW),
                ("4", "✏️  Actualizar Estudiante", Colors.MAGENTA),
                ("5", "❌ Eliminar Estudiante", Colors.RED),
                ("6", "📊 Estadísticas por Carrera", Colors.CYAN),
                ("0", "🔙 Volver", Colors.WHITE)
            ]
            
            for key, text, color in menu_options:
                print(colored_text(f" {key}. {text}", color))
            
            choice = input(colored_text("\n🔹 Seleccione una opción: ", Colors.WHITE)).strip()
            
            if choice == '1':
                self.register_student()
            elif choice == '2':
                self.list_students()
            elif choice == '3':
                self.search_student()
            elif choice == '4':
                self.update_student()
            elif choice == '5':
                self.delete_student()
            elif choice == '6':
                self.student_statistics()
            elif choice == '0':
                break
            else:
                print(colored_text("❌ Opción inválida", Colors.RED))
                input(colored_text("Presione Enter para continuar...", Colors.YELLOW))
    
    # Implementar métodos faltantes con colores...
    def register_student(self):
        """Registra un nuevo estudiante con colores"""
        print(colored_text("\n" + "═" * 60, Colors.GREEN))
        print(colored_text("➕ REGISTRO DE NUEVO ESTUDIANTE", Colors.GREEN, True))
        print(colored_text("═" * 60, Colors.GREEN))
        
        try:
            codigo = input(colored_text("🆔 Código del estudiante: ", Colors.BLUE)).strip().upper()
            if not codigo:
                print(colored_text("❌ El código no puede estar vacío", Colors.RED))
                input(colored_text("Presione Enter para continuar...", Colors.YELLOW))
                return
            
            if self.estudiante_dao.exists_codigo(codigo):
                print(colored_text(f"❌ Ya existe un estudiante con código {codigo}", Colors.RED))
                input(colored_text("Presione Enter para continuar...", Colors.YELLOW))
                return
            
            nombre = input(colored_text("👤 Nombre: ", Colors.BLUE)).strip()
            apellido = input(colored_text("👤 Apellido: ", Colors.BLUE)).strip()
            
            carreras = [
                'INGENIERIA DE SISTEMAS', 'INGENIERIA INDUSTRIAL',
                'ADMINISTRACION', 'CONTADURIA', 'DERECHO',
                'MEDICINA', 'PSICOLOGIA', 'ARQUITECTURA'
            ]
            
            print(colored_text("\n🎓 Carreras disponibles:", Colors.CYAN, True))
            for i, carrera in enumerate(carreras, 1):
                print(colored_text(f"{i}. {carrera}", Colors.WHITE))
            
            while True:
                try:
                    carrera_idx = int(input(colored_text("\n🔹 Seleccione carrera (número): ", Colors.BLUE))) - 1
                    if 0 <= carrera_idx < len(carreras):
                        carrera = carreras[carrera_idx]
                        break
                    else:
                        print(colored_text("❌ Número inválido. Intente nuevamente.", Colors.RED))
                except ValueError:
                    print(colored_text("❌ Ingrese un número válido.", Colors.RED))
            
            email = input(colored_text("📧 Email (opcional): ", Colors.BLUE)).strip()
            telefono = input(colored_text("📱 Teléfono (opcional): ", Colors.BLUE)).strip()
            
            estudiante = Estudiante(codigo, nombre, apellido, carrera, email, telefono)
            estudiante_id = self.estudiante_dao.create(estudiante)
            
            print(colored_text(f"\n✅ Estudiante registrado exitosamente con ID: {estudiante_id}", Colors.GREEN, True))
            print(f"  {colored_text('Código:', Colors.BLUE)} {estudiante.codigo}")
            print(f"  {colored_text('Nombre:', Colors.BLUE)} {estudiante.nombre} {estudiante.apellido}")
            print(f"  {colored_text('Carrera:', Colors.BLUE)} {estudiante.carrera}")
            
        except Exception as e:
            print(colored_text(f"❌ Error registrando estudiante: {str(e)}", Colors.RED))
        
        input(colored_text("\nPresione Enter para continuar...", Colors.YELLOW))
    
    def run(self):
        """Ejecuta la aplicación principal"""
        try:
            self.show_welcome_message()
            
            if not self.initialize_database():
                print(colored_text("❌ No se pudo inicializar la base de datos. Saliendo...", Colors.RED))
                return
            
            self.show_main_menu()
            
        except KeyboardInterrupt:
            print(colored_text("\n\n⚠️  Interrupción por teclado. Saliendo...", Colors.YELLOW))
        except Exception as e:
            print(colored_text(f"\n❌ Error crítico: {str(e)}", Colors.RED))
        finally:
            if hasattr(self, 'db_config'):
                self.db_config.disconnect()
    
    def exit_application(self):
        """Sale de la aplicación"""
        print(colored_text("\n" + "═" * 60, Colors.MAGENTA))
        print(colored_text("🚪 SALIENDO DEL SISTEMA", Colors.MAGENTA, True))
        print(colored_text("═" * 60, Colors.MAGENTA))
        
        print(colored_text("Gracias por usar el Sistema de Matrículas Universitarias", Colors.CYAN))
        print(colored_text("Desarrollado con Python - Paradigmas: POO, Funcional, Lógico", Colors.WHITE))
        print(colored_text("🎓 Universidad Tecnológica del Perú - UTP", Colors.YELLOW, True))
        
        self.auth_service.logout()
        self.running = False

if __name__ == "__main__":
    app = ConsoleAppWithAuth()
    app.run()