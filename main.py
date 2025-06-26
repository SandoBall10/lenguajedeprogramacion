"""
Autor: Sistema de Matrículas Universitarias
Módulo: Punto de Entrada Principal
Descripción: Archivo principal para ejecutar la aplicación
Paradigma: Multiparadigma (POO, Funcional, Lógico)
"""

import sys
import os
import logging
from typing import Optional

def setup_logging():
    """
    Configura el sistema de logging para la aplicación
    Manejo de errores y registro de eventos
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('sistema_matriculas.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies() -> bool:
    """
    Verifica que todas las dependencias estén instaladas
    Validación de entrada y manejo de errores
    """
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
        print("✗ Faltan las siguientes dependencias:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\nInstale las dependencias con:")
        print("pip install mysql-connector-python pandas numpy matplotlib")
        print("tkinter viene incluido con Python")
        return False
    
    print("✓ Todas las dependencias están instaladas")
    return True

def show_startup_banner():
    """
    Muestra el banner de inicio de la aplicación
    Uso de cadenas de texto y formateo
    """
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SISTEMA DE MATRÍCULAS UNIVERSITARIAS                      ║
║                                                                              ║
║  🎓 Proyecto Académico - Teoría de los Lenguajes de Programación            ║
║                                                                              ║
║  📋 Características:                                                         ║
║     • Paradigmas: Orientado a Objetos, Funcional, Lógico                   ║
║     • Lenguaje: Python 3.x                                                  ║
║     • Base de Datos: MySQL (XAMPP)                                          ║
║     • Interfaz: Consola + GUI (tkinter)                                     ║
║     • Ciencia de Datos: pandas, numpy, matplotlib                           ║
║                                                                              ║
║  🔧 Funcionalidades:                                                         ║
║     • Gestión completa de estudiantes, cursos y matrículas                  ║
║     • Reportes y estadísticas avanzadas                                     ║
║     • Análisis de datos y visualizaciones                                   ║
║     • Exportación a CSV y Excel                                             ║
║     • Comparación de lenguajes de programación                              ║
║                                                                              ║
║  👨‍💻 Autor: Sistema de Matrículas Universitarias                             ║
║  📅 Año: 2024                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def get_execution_mode() -> str:
    """
    Permite al usuario seleccionar el modo de ejecución
    Uso de instrucciones condicionales y entrada de datos
    """
    print("\n🚀 MODOS DE EJECUCIÓN DISPONIBLES:")
    print("1. Aplicación de Consola (Interfaz de texto)")
    print("2. Interfaz Gráfica (GUI con tkinter)")
    print("3. Modo Mixto (Consola + opción de GUI)")
    
    while True:
        try:
            choice = input("\nSeleccione el modo de ejecución (1-3): ").strip()
            
            if choice in ['1', '2', '3']:
                return choice
            else:
                print("❌ Opción inválida. Seleccione 1, 2 o 3.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saliendo del programa...")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def run_console_mode():
    """
    Ejecuta la aplicación en modo consola
    Importación dinámica y manejo de módulos
    """
    try:
        print("\n🖥️  Iniciando aplicación de consola...")
        
        from console_app import ConsoleApp
        
        app = ConsoleApp()
        app.run()
        
    except ImportError as e:
        print(f"❌ Error importando módulo de consola: {str(e)}")
    except Exception as e:
        print(f"❌ Error ejecutando aplicación de consola: {str(e)}")

def run_gui_mode():
    """
    Ejecuta la aplicación en modo GUI
    Manejo de interfaz gráfica con tkinter
    """
    try:
        print("\n🖼️  Iniciando interfaz gráfica...")
        
        # Verificar que tkinter esté disponible
        import tkinter as tk
        
        # Verificar que la base de datos esté configurada
        from config.database import DatabaseConfig
        
        db_config = DatabaseConfig()
        if not db_config.create_database_and_tables():
            print("❌ Error configurando base de datos")
            return
        
        from gui.main_window import MainWindow
        
        app = MainWindow()
        app.run()
        
    except ImportError as e:
        print(f"❌ Error importando módulos GUI: {str(e)}")
        print("Asegúrese de que tkinter esté instalado")
    except Exception as e:
        print(f"❌ Error ejecutando interfaz gráfica: {str(e)}")

def run_mixed_mode():
    """
    Ejecuta la aplicación en modo mixto
    Combinación de consola y GUI según elección del usuario
    """
    try:
        print("\n🔄 Modo mixto seleccionado")
        print("Iniciando con aplicación de consola...")
        print("Desde la consola podrá acceder a la interfaz gráfica cuando lo desee")
        
        from console_app import ConsoleApp
        
        app = ConsoleApp()
        app.run()
        
    except Exception as e:
        print(f"❌ Error ejecutando modo mixto: {str(e)}")

def main():
    """
    Función principal del programa
    Punto de entrada y control de flujo principal
    """
    try:
        # Configurar logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Iniciando Sistema de Matrículas Universitarias")
        
        # Mostrar banner de inicio
        show_startup_banner()
        
        # Verificar dependencias
        if not check_dependencies():
            print("\n❌ No se pueden ejecutar todas las funcionalidades sin las dependencias")
            print("¿Desea continuar de todos modos? (s/n): ", end="")
            
            if input().lower() not in ['s', 'si', 'y', 'yes']:
                print("👋 Saliendo del programa...")
                return
        
        # Seleccionar modo de ejecución
        mode = get_execution_mode()
        
        # Ejecutar según el modo seleccionado
        mode_functions = {
            '1': run_console_mode,
            '2': run_gui_mode,
            '3': run_mixed_mode
        }
        
        # Programación funcional: usar diccionario como dispatcher
        mode_function = mode_functions.get(mode)
        if mode_function:
            mode_function()
        else:
            print("❌ Modo de ejecución inválido")
        
        print("\n✅ Programa finalizado correctamente")
        logger.info("Sistema de Matrículas finalizado correctamente")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
        logging.info("Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error crítico: {str(e)}")
        logging.error(f"Error crítico: {str(e)}", exc_info=True)
    finally:
        print("\n👋 ¡Gracias por usar el Sistema de Matrículas Universitarias!")

def show_help():
    """
    Muestra ayuda sobre el uso del programa
    Información para el usuario
    """
    help_text = """
📖 AYUDA - SISTEMA DE MATRÍCULAS UNIVERSITARIAS

🎯 PROPÓSITO:
   Sistema académico para gestionar estudiantes, cursos y matrículas universitarias.
   Desarrollado como proyecto para el curso de Teoría de los Lenguajes de Programación.

🔧 REQUISITOS TÉCNICOS:
   • Python 3.7 o superior
   • MySQL Server (XAMPP recomendado)
   • Librerías: mysql-connector-python, pandas, numpy, matplotlib

📋 FUNCIONALIDADES PRINCIPALES:
   • Registro y gestión de estudiantes
   • Administración de cursos académicos
   • Sistema de matrículas con validaciones
   • Reportes y estadísticas detalladas
   • Análisis de datos con pandas/numpy
   • Interfaz de consola y gráfica (tkinter)
   • Exportación a CSV y Excel

🎨 PARADIGMAS IMPLEMENTADOS:
   • Orientado a Objetos: Clases, herencia, encapsulación
   • Funcional: map(), filter(), lambda, funciones de orden superior
   • Lógico: Predicados, reglas de negocio, validaciones

🚀 MODOS DE EJECUCIÓN:
   1. Consola: Interfaz de texto completa
   2. GUI: Interfaz gráfica con tkinter
   3. Mixto: Consola con acceso a GUI

📞 SOPORTE:
   Para problemas técnicos, verifique:
   • Conexión a MySQL (XAMPP ejecutándose)
   • Instalación de dependencias Python
   • Permisos de base de datos

🎓 ASPECTOS ACADÉMICOS:
   • Demuestra aplicación de múltiples paradigmas
   • Implementa patrones de diseño (DAO, MVC)
   • Usa ciencia de datos para análisis
   • Incluye comparación de lenguajes de programación
    """
    print(help_text)

# Funciones auxiliares para el programa principal
def validate_python_version() -> bool:
    """
    Valida que la versión de Python sea compatible
    Verificación de requisitos del sistema
    """
    if sys.version_info < (3, 7):
        print(f"❌ Python 3.7+ requerido. Versión actual: {sys.version}")
        return False
    return True

def check_mysql_connection() -> bool:
    """
    Verifica la conexión a MySQL
    Predicado lógico para validación de base de datos
    """
    try:
        from config.database import DatabaseConfig
        
        db_config = DatabaseConfig()
        if db_config.connect():
            db_config.disconnect()
            return True
        return False
        
    except Exception:
        return False

# Decorador para manejo de errores (programación funcional)
def handle_errors(func):
    """
    Decorador para manejo centralizado de errores
    Programación funcional: decoradores como funciones de orden superior
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error en {func.__name__}: {str(e)}")
            print(f"❌ Error: {str(e)}")
            return None
    return wrapper

# Función lambda para validaciones rápidas
is_valid_mode = lambda mode: mode in ['1', '2', '3']
is_affirmative = lambda response: response.lower() in ['s', 'si', 'y', 'yes']

if __name__ == "__main__":
    # Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h', 'help']:
            show_help()
        elif arg in ['--console', '-c']:
            run_console_mode()
        elif arg in ['--gui', '-g']:
            run_gui_mode()
        elif arg in ['--version', '-v']:
            print("Sistema de Matrículas Universitarias v1.0")
            print("Python", sys.version)
        else:
            print(f"❌ Argumento desconocido: {arg}")
            print("Use --help para ver opciones disponibles")
    else:
        # Ejecutar programa principal
        main()