"""
Autor: Sistema de Matrículas Universitarias
Módulo: Punto de Entrada Principal con Autenticación
Descripción: Archivo principal con sistema de login y roles
Paradigma: Multiparadigma (POO, Funcional, Lógico)
"""

import sys
import os
import logging
from typing import Optional

def setup_logging():
    """Configura el sistema de logging para la aplicación"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('sistema_matriculas.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies() -> bool:
    """Verifica que todas las dependencias estén instaladas"""
    required_modules = [
        'mysql.connector',
        'pandas',
        'numpy',
        'matplotlib',
        'tkinter'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("❌ Faltan las siguientes dependencias:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\nInstale las dependencias con:")
        print("pip install mysql-connector-python pandas numpy matplotlib")
        print("tkinter viene incluido con Python")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def show_startup_banner():
    """Muestra el banner de inicio con colores"""
    # Códigos de colores ANSI
    CYAN = '\033[36m'
    YELLOW = '\033[33m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    
    banner = f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════════════════════╗{RESET}
{CYAN}{BOLD}║                    SISTEMA DE MATRÍCULAS UNIVERSITARIAS                      ║{RESET}
{CYAN}{BOLD}║                        🎓 UTP - 2024 🎓                                       ║{RESET}
{CYAN}║                                                                              ║{RESET}
{WHITE}║  📋 Características:                                                         ║{RESET}
{WHITE}║     • Sistema de Login con Roles (Admin/Estudiante)                          ║{RESET}
{WHITE}║     • Paradigmas: Orientado a Objetos, Funcional, Lógico                     ║{RESET}
{WHITE}║     • Lenguaje: Python 3.x                                                   ║{RESET}
{WHITE}║     • Base de Datos: MySQL (XAMPP)                                           ║{RESET}
{WHITE}║     • Interfaz: Gráfica (tkinter)                                            ║{RESET}
{WHITE}║     • Ciencia de Datos: pandas, numpy, matplotlib                            ║{RESET}
{CYAN}║                                                                              ║{RESET}
{YELLOW}║  🔐 Credenciales por defecto:                                               ║{RESET}
{YELLOW}║     • Admin: admin@sistema.com / admin123                                    ║{RESET}
{YELLOW}║     • Estudiantes: Crear desde panel admin                                   ║{RESET}
{CYAN}║                                                                              ║{RESET}
{CYAN}{BOLD}╚══════════════════════════════════════════════════════════════════════════════╝{RESET}
    """
    print(banner)

def get_execution_mode() -> str:
    """Inicia directamente la interfaz gráfica"""
    GREEN = '\033[32m'
    CYAN = '\033[36m'
    RESET = '\033[0m'
    
    print(f"\n{GREEN}🚀 INICIANDO INTERFAZ GRÁFICA:{RESET}")
    print(f"{CYAN}🖼️  Cargando Sistema de Matrículas - Modo Visual{RESET}")
    
    return '2'  # Siempre retorna GUI

def run_gui_with_auth():
    """Ejecuta la interfaz gráfica con autenticación"""
    try:
        GREEN = '\033[32m'
        CYAN = '\033[36m'
        RED = '\033[31m'
        RESET = '\033[0m'
        
        print(f"\n{CYAN}🖼️  Iniciando interfaz gráfica con autenticación...{RESET}")
        
        # Verificar que tkinter esté disponible
        import tkinter as tk
        
        # Verificar que la base de datos esté configurada
        from config.database import DatabaseConfig
        
        db_config = DatabaseConfig()
        if not db_config.create_database_and_tables():
            print(f"{RED}❌ Error configurando base de datos{RESET}")
            return
        
        # Crear tabla de usuarios
        try:
            connection = db_config.get_new_connection()
            if connection is None:
                print(f"{RED}❌ No se pudo establecer conexión con la base de datos{RESET}")
                return
                
            cursor = connection.cursor()
            
            create_users_table = '''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(64) NOT NULL,
                rol ENUM("ADMINISTRADOR", "ESTUDIANTE") NOT NULL,
                nombre VARCHAR(100),
                apellido VARCHAR(100),
                codigo_estudiante VARCHAR(10),
                activo BOOLEAN DEFAULT TRUE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
            
            cursor.execute(create_users_table)
            connection.commit()
            cursor.close()
            connection.close()
            
        except Exception as e:
            print(f"{RED}❌ Error creando tabla usuarios: {str(e)}{RESET}")
        
        from gui.main_window_with_auth import MainWindowWithAuth
        
        app = MainWindowWithAuth()
        app.run()
        
    except ImportError as e:
        print(f"{RED}❌ Error importando módulos GUI: {str(e)}{RESET}")
        print("Asegúrese de que tkinter esté instalado")
    except Exception as e:
        print(f"{RED}❌ Error ejecutando interfaz gráfica: {str(e)}{RESET}")

def main():
    """Función principal del programa"""
    try:
        # Configurar logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Iniciando Sistema de Matrículas Universitarias con Autenticación")
        
        # Mostrar banner de inicio
        show_startup_banner()
        
        # Verificar dependencias
        if not check_dependencies():
            YELLOW = '\033[33m'
            RED = '\033[31m'
            RESET = '\033[0m'
            
            print(f"\n{RED}❌ No se pueden ejecutar todas las funcionalidades sin las dependencias{RESET}")
            print(f"{YELLOW}¿Desea continuar de todos modos? (s/n): {RESET}", end="")
            
            if input().lower() not in ['s', 'si', 'y', 'yes']:
                print(f"{YELLOW}👋 Saliendo del programa...{RESET}")
                return
        
        # Seleccionar modo de ejecución (siempre GUI)
        mode = get_execution_mode()
        
        # Ejecutar interfaz gráfica
        run_gui_with_auth()
        
        GREEN = '\033[32m'
        RESET = '\033[0m'
        print(f"\n{GREEN}✅ Programa finalizado correctamente{RESET}")
        logger.info("Sistema de Matrículas finalizado correctamente")
        
    except KeyboardInterrupt:
        YELLOW = '\033[33m'
        RESET = '\033[0m'
        print(f"\n\n{YELLOW}⚠️  Programa interrumpido por el usuario{RESET}")
        logging.info("Programa interrumpido por el usuario")
    except Exception as e:
        RED = '\033[31m'
        RESET = '\033[0m'
        print(f"\n{RED}❌ Error crítico: {str(e)}{RESET}")
        logging.error(f"Error crítico: {str(e)}", exc_info=True)
    finally:
        CYAN = '\033[36m'
        YELLOW = '\033[33m'
        RESET = '\033[0m'
        print(f"\n{CYAN}👋 ¡Gracias por usar el Sistema de Matrículas Universitarias!{RESET}")
        print(f"{YELLOW}🎓 Universidad Tecnológica del Perú - UTP{RESET}")

if __name__ == "__main__":
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h', 'help']:
            print("Sistema de Matrículas Universitarias con Autenticación")
            print("Uso: python main_with_auth.py [opción]")
            print("Opciones:")
            print("  --gui, -g        Ejecutar en modo GUI (por defecto)")
            print("  --version, -v    Mostrar versión")
            print("  --help, -h       Mostrar esta ayuda")
        elif arg in ['--gui', '-g']:
            run_gui_with_auth()
        elif arg in ['--version', '-v']:
            print("Sistema de Matrículas Universitarias v2.0 - Interfaz Gráfica")
            print("Python", sys.version)
        else:
            RED = '\033[31m'
            RESET = '\033[0m'
            print(f"{RED}❌ Argumento desconocido: {arg}{RESET}")
            print("Use --help para ver opciones disponibles")
    else:
        # Ejecutar programa principal
        main()