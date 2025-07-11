"""
Módulo: Aplicación de Consola
Descripción: Interfaz de consola para el sistema
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
from services.matricula_service import MatriculaService
from models.estudiante import Estudiante
from models.curso import Curso
from models.matricula import EstadoMatricula
from utils.data_analysis import DataAnalyzer
from utils.language_comparison import print_languages_comparison

class ConsoleApp:
    """
    Aplicación de consola para el sistema de matrículas
    Implementa interfaz de usuario por consola con menús interactivos
    """
    
    def __init__(self):
        """Constructor de la aplicación de consola"""
        self.db_config = DatabaseConfig()
        self.estudiante_dao = EstudianteDAO()
        self.curso_dao = CursoDAO()
        self.matricula_dao = MatriculaDAO()
        self.matricula_service = MatriculaService()
        self.data_analyzer = DataAnalyzer()
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Estado de la aplicación
        self.running = True
    
    def initialize_database(self) -> bool:
        """
        Inicializa la base de datos y crea las tablas necesarias
        Manejo de errores y validaciones de entrada
        """
        try:
            print("Inicializando base de datos...")
            
            if self.db_config.create_database_and_tables():
                print("✓ Base de datos inicializada correctamente")
                return True
            else:
                print("✗ Error inicializando base de datos")
                return False
                
        except Exception as e:
            print(f"✗ Error crítico: {str(e)}")
            return False
    
    def show_welcome_message(self):
        """
        Muestra mensaje de bienvenida con información del sistema
        Uso de cadenas de texto y formateo
        """
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar pantalla
        
        welcome_text = """
╔══════════════════════════════════════════════════════════════╗
║              SISTEMA DE MATRÍCULAS UNIVERSITARIAS            ║
║                                                              ║
║  Autor: Sistema de Matrículas Universitarias                 ║
║  Lenguaje: Python 3.x                                        ║
║  Paradigmas: POO, Funcional, Lógico                          ║
║  Base de Datos: MySQL (XAMPP)                                ║
║  Interfaz: Consola + GUI (tkinter)                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        
        print(welcome_text)
        print("\nPresione Enter para continuar...")
        input()
    
    def show_main_menu(self):
        """
        Muestra el menú principal del sistema
        Uso de instrucciones condicionales y bucles
        """
        menu_options = {
            '1': 'Gestión de Estudiantes',
            '2': 'Gestión de Cursos', 
            '3': 'Gestión de Matrículas',
            '4': 'Reportes y Estadísticas',
            '7': 'Interfaz Gráfica',
            '0': 'Salir'
        }
        
        while self.running:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("╔" + "═" * 50 + "╗")
            print("║" + " MENÚ PRINCIPAL".center(50) + "║")
            print("╠" + "═" * 50 + "╣")
            
            for key, value in menu_options.items():
                print(f"║ {key}. {value:<45} ║")
            
            print("╚" + "═" * 50 + "╝")
            
            choice = input("\nSeleccione una opción: ").strip()
            
            # Usar diccionario como estructura de control (programación funcional)
            menu_actions = {
                '1': self.student_management_menu,
                '2': self.course_management_menu,
                '3': self.enrollment_management_menu,
                '4': self.reports_menu,
                '5': self.data_analysis_menu,
                '6': self.language_comparison_menu,
                '7': self.launch_gui,
                '8': self.configuration_menu,
                '0': self.exit_application
            }
            
            action = menu_actions.get(choice)
            if action:
                action()
            else:
                print("Opción inválida. Presione Enter para continuar...")
                input()
    
    def student_management_menu(self):
        """
        Menú de gestión de estudiantes
        Aplicación de bucles y manejo de entrada de datos
        """
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("╔" + "═" * 40 + "╗")
            print("║" + " GESTIÓN DE ESTUDIANTES".center(40) + "║")
            print("╠" + "═" * 40 + "╣")
            print("║ 1. Registrar Estudiante" + " " * 15 + "║")
            print("║ 2. Listar Estudiantes" + " " * 17 + "║")
            print("║ 3. Buscar Estudiante" + " " * 18 + "║")
            print("║ 4. Actualizar Estudiante" + " " * 14 + "║")
            print("║ 5. Eliminar Estudiante" + " " * 16 + "║")
            print("║ 6. Estadísticas por Carrera" + " " * 10 + "║")
            print("║ 0. Volver al Menú Principal" + " " * 9 + "║")
            print("╚" + "═" * 40 + "╝")
            
            choice = input("\nSeleccione una opción: ").strip()
            
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
                print("Opción inválida. Presione Enter para continuar...")
                input()
    
    def register_student(self):
        """
        Registra un nuevo estudiante
        Validación de entrada y manejo de errores
        """
        print("\n" + "═" * 50)
        print("REGISTRO DE NUEVO ESTUDIANTE")
        print("═" * 50)
        
        try:
            # Entrada de datos con validación
            codigo = input("Código del estudiante: ").strip().upper()
            if not codigo:
                print("Error: El código no puede estar vacío")
                input("Presione Enter para continuar...")
                return
            
            # Verificar si el código ya existe
            if self.estudiante_dao.exists_codigo(codigo):
                print(f"Error: Ya existe un estudiante con código {codigo}")
                input("Presione Enter para continuar...")
                return
            
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            
            # Mostrar opciones de carrera
            carreras = [
                'INGENIERIA DE SISTEMAS', 'INGENIERIA INDUSTRIAL',
                'ADMINISTRACION', 'CONTADURIA', 'DERECHO',
                'MEDICINA', 'PSICOLOGIA', 'ARQUITECTURA'
            ]
            
            print("\nCarreras disponibles:")
            for i, carrera in enumerate(carreras, 1):
                print(f"{i}. {carrera}")
            
            while True:
                try:
                    carrera_idx = int(input("Seleccione carrera (número): ")) - 1
                    if 0 <= carrera_idx < len(carreras):
                        carrera = carreras[carrera_idx]
                        break
                    else:
                        print("Número inválido. Intente nuevamente.")
                except ValueError:
                    print("Ingrese un número válido.")
            
            email = input("Email (opcional): ").strip()
            telefono = input("Teléfono (opcional): ").strip()
            
            # Crear y guardar estudiante
            estudiante = Estudiante(codigo, nombre, apellido, carrera, email, telefono)
            estudiante_id = self.estudiante_dao.create(estudiante)
            
            print(f"\n✓ Estudiante registrado exitosamente con ID: {estudiante_id}")
            print(f"  Código: {estudiante.codigo}")
            print(f"  Nombre: {estudiante.nombre} {estudiante.apellido}")
            print(f"  Carrera: {estudiante.carrera}")
            
        except Exception as e:
            print(f"✗ Error registrando estudiante: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def list_students(self):
        """
        Lista todos los estudiantes
        Uso de bucles for y formateo de salida
        """
        print("\n" + "═" * 80)
        print("LISTA DE ESTUDIANTES REGISTRADOS")
        print("═" * 80)
        
        try:
            estudiantes = self.estudiante_dao.find_all()
            
            if not estudiantes:
                print("No hay estudiantes registrados.")
            else:
                # Encabezados de tabla
                print(f"{'Código':<10} {'Nombre':<20} {'Apellido':<20} {'Carrera':<25} {'Email':<25}")
                print("-" * 100)
                
                # Programación funcional: usar map para formatear
                def format_student(est):
                    return f"{est.codigo:<10} {est.nombre:<20} {est.apellido:<20} {est.carrera:<25} {est.email:<25}"
                
                formatted_students = list(map(format_student, estudiantes))
                
                for formatted_student in formatted_students:
                    print(formatted_student)
                
                print(f"\nTotal de estudiantes: {len(estudiantes)}")
                
        except Exception as e:
            print(f"✗ Error listando estudiantes: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def search_student(self):
        """
        Busca estudiantes por nombre
        Uso de funciones de búsqueda y filtrado
        """
        print("\n" + "═" * 50)
        print("BÚSQUEDA DE ESTUDIANTES")
        print("═" * 50)
        
        try:
            search_term = input("Ingrese nombre o apellido a buscar: ").strip()
            
            if not search_term:
                print("Término de búsqueda vacío.")
                input("Presione Enter para continuar...")
                return
            
            estudiantes = self.estudiante_dao.search_by_name(search_term)
            
            if not estudiantes:
                print(f"No se encontraron estudiantes con '{search_term}'")
            else:
                print(f"\nResultados para '{search_term}':")
                print("-" * 80)
                
                for est in estudiantes:
                    print(f"Código: {est.codigo}")
                    print(f"Nombre: {est.nombre} {est.apellido}")
                    print(f"Carrera: {est.carrera}")
                    print(f"Email: {est.email}")
                    print(f"Teléfono: {est.telefono}")
                    print("-" * 40)
                
                print(f"Total encontrados: {len(estudiantes)}")
                
        except Exception as e:
            print(f"✗ Error en búsqueda: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def course_management_menu(self):
        """Menú de gestión de cursos"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("╔" + "═" * 40 + "╗")
            print("║" + " GESTIÓN DE CURSOS".center(40) + "║")
            print("╠" + "═" * 40 + "╣")
            print("║ 1. Registrar Curso" + " " * 21 + "║")
            print("║ 2. Listar Cursos" + " " * 23 + "║")
            print("║ 3. Buscar Curso" + " " * 24 + "║")
            print("║ 4. Actualizar Curso" + " " * 20 + "║")
            print("║ 5. Eliminar Curso" + " " * 22 + "║")
            print("║ 6. Cursos con Cupos" + " " * 19 + "║")
            print("║ 0. Volver al Menú Principal" + " " * 9 + "║")
            print("╚" + "═" * 40 + "╝")
            
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == '1':
                self.register_course()
            elif choice == '2':
                self.list_courses()
            elif choice == '3':
                self.search_course()
            elif choice == '4':
                self.update_course()
            elif choice == '5':
                self.delete_course()
            elif choice == '6':
                self.courses_with_spots()
            elif choice == '0':
                break
            else:
                print("Opción inválida. Presione Enter para continuar...")
                input()
    
    def register_course(self):
        """Registra un nuevo curso"""
        print("\n" + "═" * 50)
        print("REGISTRO DE NUEVO CURSO")
        print("═" * 50)
        
        try:
            codigo = input("Código del curso: ").strip().upper()
            if not codigo:
                print("Error: El código no puede estar vacío")
                input("Presione Enter para continuar...")
                return
            
            if self.curso_dao.exists_codigo(codigo):
                print(f"Error: Ya existe un curso con código {codigo}")
                input("Presione Enter para continuar...")
                return
            
            nombre = input("Nombre del curso: ").strip()
            
            # Validar créditos
            while True:
                try:
                    creditos = int(input("Número de créditos (1-6): "))
                    if 1 <= creditos <= 6:
                        break
                    else:
                        print("Los créditos deben estar entre 1 y 6")
                except ValueError:
                    print("Ingrese un número válido")
            
            profesor = input("Profesor (opcional): ").strip()
            horario = input("Horario (opcional): ").strip()
            
            # Validar cupos
            while True:
                try:
                    cupos = int(input("Cupos disponibles (10-100): "))
                    if 10 <= cupos <= 100:
                        break
                    else:
                        print("Los cupos deben estar entre 10 y 100")
                except ValueError:
                    print("Ingrese un número válido")
            
            # Crear y guardar curso
            curso = Curso(codigo, nombre, creditos, profesor, horario, cupos)
            curso_id = self.curso_dao.create(curso)
            
            print(f"\n✓ Curso registrado exitosamente con ID: {curso_id}")
            print(f"  Código: {curso.codigo}")
            print(f"  Nombre: {curso.nombre}")
            print(f"  Créditos: {curso.creditos}")
            print(f"  Cupos: {curso._cupos_disponibles}")
            
        except Exception as e:
            print(f"✗ Error registrando curso: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def list_courses(self):
        """Lista todos los cursos"""
        print("\n" + "═" * 100)
        print("LISTA DE CURSOS REGISTRADOS")
        print("═" * 100)
        
        try:
            cursos = self.curso_dao.find_all()
            
            if not cursos:
                print("No hay cursos registrados.")
            else:
                # Encabezados
                print(f"{'Código':<8} {'Nombre':<30} {'Créd.':<5} {'Profesor':<20} {'Cupos Disp.':<12} {'Ocupados':<8}")
                print("-" * 100)
                
                for curso in cursos:
                    print(f"{curso.codigo:<8} {curso.nombre:<30} {curso.creditos:<5} "
                          f"{curso.profesor:<20} {curso.cupos_disponibles:<12} {curso.cupos_ocupados:<8}")
                
                print(f"\nTotal de cursos: {len(cursos)}")
                
        except Exception as e:
            print(f"✗ Error listando cursos: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def enrollment_management_menu(self):
        """Menú de gestión de matrículas"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("╔" + "═" * 40 + "╗")
            print("║" + " GESTIÓN DE MATRÍCULAS".center(40) + "║")
            print("╠" + "═" * 40 + "╣")
            print("║ 1. Nueva Matrícula" + " " * 20 + "║")
            print("║ 2. Listar Matrículas" + " " * 18 + "║")
            print("║ 3. Cancelar Matrícula" + " " * 17 + "║")
            print("║ 4. Matrículas por Estudiante" + " " * 8 + "║")
            print("║ 5. Estudiantes por Curso" + " " * 14 + "║")
            print("║ 6. Matrículas Activas" + " " * 16 + "║")
            print("║ 0. Volver al Menú Principal" + " " * 9 + "║")
            print("╚" + "═" * 40 + "╝")
            
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == '1':
                self.new_enrollment()
            elif choice == '2':
                self.list_enrollments()
            elif choice == '3':
                self.cancel_enrollment()
            elif choice == '4':
                self.enrollments_by_student()
            elif choice == '5':
                self.students_by_course()
            elif choice == '6':
                self.active_enrollments()
            elif choice == '0':
                break
            else:
                print("Opción inválida. Presione Enter para continuar...")
                input()
    
    def new_enrollment(self):
        """
        Crea una nueva matrícula
        Aplicación de reglas de negocio y validaciones
        """
        print("\n" + "═" * 50)
        print("NUEVA MATRÍCULA")
        print("═" * 50)
        
        try:
            # Solicitar código de estudiante
            estudiante_codigo = input("Código del estudiante: ").strip().upper()
            if not estudiante_codigo:
                print("Error: Código de estudiante requerido")
                input("Presione Enter para continuar...")
                return
            
            # Verificar que existe el estudiante
            estudiante = self.estudiante_dao.find_by_codigo(estudiante_codigo)
            if not estudiante:
                print(f"Error: No existe estudiante con código {estudiante_codigo}")
                input("Presione Enter para continuar...")
                return
            
            print(f"Estudiante: {estudiante.nombre} {estudiante.apellido} ({estudiante.carrera})")
            
            # Mostrar cursos disponibles para el estudiante
            cursos_disponibles = self.matricula_service.obtener_cursos_disponibles_para_estudiante(estudiante_codigo)
            
            if not cursos_disponibles:
                print("No hay cursos disponibles para este estudiante.")
                input("Presione Enter para continuar...")
                return
            
            print("\nCursos disponibles:")
            print("-" * 80)
            for i, curso in enumerate(cursos_disponibles, 1):
                print(f"{i}. {curso['codigo']} - {curso['nombre']} "
                      f"({curso['creditos']} créditos, {curso['cupos_disponibles']} cupos)")
            
            # Seleccionar curso
            while True:
                try:
                    curso_idx = int(input("\nSeleccione curso (número): ")) - 1
                    if 0 <= curso_idx < len(cursos_disponibles):
                        curso_seleccionado = cursos_disponibles[curso_idx]
                        break
                    else:
                        print("Número inválido. Intente nuevamente.")
                except ValueError:
                    print("Ingrese un número válido.")
            
            # Confirmar matrícula
            print(f"\nConfirmar matrícula:")
            print(f"Estudiante: {estudiante.nombre} {estudiante.apellido}")
            print(f"Curso: {curso_seleccionado['nombre']}")
            print(f"Créditos: {curso_seleccionado['creditos']}")
            
            confirmar = input("\n¿Confirmar matrícula? (s/n): ").strip().lower()
            
            if confirmar == 's':
                # Procesar matrícula
                success, message = self.matricula_service.matricular_estudiante(
                    estudiante_codigo, 
                    curso_seleccionado['codigo']
                )
                
                if success:
                    print(f"\n✓ {message}")
                else:
                    print(f"\n✗ {message}")
            else:
                print("Matrícula cancelada.")
                
        except Exception as e:
            print(f"✗ Error en matrícula: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def list_enrollments(self):
        """Lista todas las matrículas"""
        print("\n" + "═" * 100)
        print("LISTA DE MATRÍCULAS")
        print("═" * 100)
        
        try:
            matriculas = self.matricula_dao.find_all()
            
            if not matriculas:
                print("No hay matrículas registradas.")
            else:
                print(f"{'ID':<5} {'Estudiante':<15} {'Curso':<15} {'Fecha':<20} {'Estado':<12}")
                print("-" * 100)
                
                for matricula in matriculas:
                    # Obtener información adicional
                    estudiante = self.estudiante_dao.find_by_codigo(matricula.estudiante_codigo)
                    curso = self.curso_dao.find_by_codigo(matricula.curso_codigo)
                    
                    estudiante_info = f"{estudiante.apellido}" if estudiante else matricula.estudiante_codigo
                    curso_info = curso.codigo if curso else matricula.curso_codigo
                    fecha_str = matricula.fecha_matricula.strftime('%Y-%m-%d %H:%M')
                    
                    print(f"{matricula.id or 'N/A':<5} {estudiante_info:<15} {curso_info:<15} "
                          f"{fecha_str:<20} {matricula.estado.value:<12}")
                
                print(f"\nTotal de matrículas: {len(matriculas)}")
                
        except Exception as e:
            print(f"✗ Error listando matrículas: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def reports_menu(self):
        """Menú de reportes y estadísticas"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("╔" + "═" * 40 + "╗")
            print("║" + " REPORTES Y ESTADÍSTICAS".center(40) + "║")
            print("╠" + "═" * 40 + "╣")
            print("║ 1. Reporte General" + " " * 20 + "║")
            print("║ 2. Estadísticas de Matrícula" + " " * 10 + "║")
            print("║ 3. Reporte por Carrera" + " " * 16 + "║")
            print("║ 4. Ocupación de Cursos" + " " * 16 + "║")
            print("║ 5. Exportar a CSV" + " " * 20 + "║")
            print("║ 0. Volver al Menú Principal" + " " * 9 + "║")
            print("╚" + "═" * 40 + "╝")
            
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == '1':
                self.general_report()
            elif choice == '2':
                self.enrollment_statistics()
            elif choice == '3':
                self.career_report()
            elif choice == '4':
                self.course_occupation_report()
            elif choice == '5':
                self.export_csv()
            elif choice == '0':
                break
            else:
                print("Opción inválida. Presione Enter para continuar...")
                input()
    
    def general_report(self):
        """Genera reporte general del sistema"""
        print("\n" + "═" * 60)
        print("REPORTE GENERAL DEL SISTEMA")
        print("═" * 60)
        
        try:
            # Obtener estadísticas básicas
            total_estudiantes = len(self.estudiante_dao.find_all())
            total_cursos = len(self.curso_dao.find_all())
            total_matriculas = len(self.matricula_dao.find_all())
            matriculas_activas = len(self.matricula_dao.find_active_matriculas())
            
            # Generar reporte usando el servicio
            reporte = self.matricula_service.generar_reporte_matriculas()
            
            print(f"Fecha del reporte: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"\nRESUMEN EJECUTIVO:")
            print(f"- Total de estudiantes registrados: {total_estudiantes}")
            print(f"- Total de cursos disponibles: {total_cursos}")
            print(f"- Total de matrículas realizadas: {total_matriculas}")
            print(f"- Matrículas activas: {matriculas_activas}")
            
            if reporte and 'resumen' in reporte:
                resumen = reporte['resumen']
                print(f"- Estudiantes con matrículas activas: {resumen.get('estudiantes_con_matriculas', 0)}")
            
            # Estadísticas por carrera
            if reporte and 'por_carrera' in reporte:
                print(f"\nMATRÍCULAS POR CARRERA:")
                for carrera, cantidad in reporte['por_carrera'].items():
                    print(f"- {carrera}: {cantidad} matrículas")
            
            # Top cursos más demandados
            if reporte and 'por_curso' in reporte:
                print(f"\nTOP 5 CURSOS MÁS DEMANDADOS:")
                cursos_ordenados = sorted(reporte['por_curso'].items(), key=lambda x: x[1], reverse=True)
                for i, (curso, cantidad) in enumerate(cursos_ordenados[:5], 1):
                    print(f"{i}. {curso}: {cantidad} estudiantes")
            
            # Porcentajes
            if reporte and 'porcentajes' in reporte:
                porcentajes = reporte['porcentajes']
                print(f"\nDISTRIBUCIÓN DE MATRÍCULAS:")
                print(f"- Activas: {porcentajes.get('activas', 0):.1f}%")
                print(f"- Canceladas: {porcentajes.get('canceladas', 0):.1f}%")
                print(f"- Completadas: {porcentajes.get('completadas', 0):.1f}%")
            
        except Exception as e:
            print(f"✗ Error generando reporte: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def data_analysis_menu(self):
        """Menú de análisis de datos"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("╔" + "═" * 40 + "╗")
            print("║" + " ANÁLISIS DE DATOS".center(40) + "║")
            print("╠" + "═" * 40 + "╣")
            print("║ 1. Análisis con Pandas" + " " * 16 + "║")
            print("║ 2. Estadísticas con NumPy" + " " * 12 + "║")
            print("║ 3. Tendencias de Matrícula" + " " * 12 + "║")
            print("║ 4. Análisis por Carrera" + " " * 15 + "║")
            print("║ 5. Exportar a Excel" + " " * 19 + "║")
            print("║ 0. Volver al Menú Principal" + " " * 9 + "║")
            print("╚" + "═" * 40 + "╝")
            
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == '1':
                self.pandas_analysis()
            elif choice == '2':
                self.numpy_statistics()
            elif choice == '3':
                self.enrollment_trends()
            elif choice == '4':
                self.career_analysis()
            elif choice == '5':
                self.export_excel()
            elif choice == '0':
                break
            else:
                print("Opción inválida. Presione Enter para continuar...")
                input()
    
    def pandas_analysis(self):
        """Análisis de datos usando pandas"""
        print("\n" + "═" * 60)
        print("ANÁLISIS DE DATOS CON PANDAS")
        print("═" * 60)
        
        try:
            # Obtener datos
            estudiantes_data = [est.to_dict() for est in self.estudiante_dao.find_all()]
            cursos_data = [curso.to_dict() for curso in self.curso_dao.find_all()]
            matriculas_data = self.matricula_dao.get_enrollment_report()
            
            # Crear DataFrames
            df_estudiantes = self.data_analyzer.create_students_dataframe(estudiantes_data)
            df_cursos = self.data_analyzer.create_courses_dataframe(cursos_data)
            df_matriculas = self.data_analyzer.create_enrollments_dataframe(matriculas_data)
            
            print(f"DataFrames creados:")
            print(f"- Estudiantes: {len(df_estudiantes)} registros")
            print(f"- Cursos: {len(df_cursos)} registros")
            print(f"- Matrículas: {len(df_matriculas)} registros")
            
            # Análisis básico con pandas
            if not df_estudiantes.empty:
                print(f"\nANÁLISIS DE ESTUDIANTES:")
                if 'carrera' in df_estudiantes.columns:
                    carrera_counts = df_estudiantes['carrera'].value_counts()
                    print("Distribución por carrera:")
                    for carrera, count in carrera_counts.items():
                        percentage = (count / len(df_estudiantes) * 100)
                        print(f"  - {carrera}: {count} ({percentage:.1f}%)")
            
            if not df_cursos.empty:
                print(f"\nANÁLISIS DE CURSOS:")
                if 'creditos' in df_cursos.columns:
                    creditos_stats = df_cursos['creditos'].describe()
                    print("Estadísticas de créditos:")
                    print(f"  - Promedio: {creditos_stats['mean']:.2f}")
                    print(f"  - Mediana: {creditos_stats['50%']:.2f}")
                    print(f"  - Mínimo: {creditos_stats['min']}")
                    print(f"  - Máximo: {creditos_stats['max']}")
            
            if not df_matriculas.empty:
                print(f"\nANÁLISIS DE MATRÍCULAS:")
                if 'estado' in df_matriculas.columns:
                    estado_counts = df_matriculas['estado'].value_counts()
                    print("Distribución por estado:")
                    for estado, count in estado_counts.items():
                        percentage = (count / len(df_matriculas) * 100)
                        print(f"  - {estado}: {count} ({percentage:.1f}%)")
            
        except Exception as e:
            print(f"✗ Error en análisis con pandas: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def language_comparison_menu(self):
        """Menú de comparación de lenguajes"""
        print("\n" + "═" * 60)
        print("COMPARACIÓN DE LENGUAJES DE PROGRAMACIÓN")
        print("═" * 60)
        
        try:
            print_languages_comparison()
            
        except Exception as e:
            print(f"✗ Error mostrando comparación: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def launch_gui(self):
        """Lanza la interfaz gráfica"""
        print("\n" + "═" * 50)
        print("LANZANDO INTERFAZ GRÁFICA")
        print("═" * 50)
        
        try:
            print("Iniciando interfaz gráfica con tkinter...")
            print("Nota: La ventana GUI se abrirá en una nueva ventana.")
            print("Cierre la ventana GUI para volver a la consola.")
            
            from gui.main_window import MainWindow
            
            # Crear y ejecutar ventana principal
            app = MainWindow()
            app.run()
            
            print("Interfaz gráfica cerrada.")
            
        except Exception as e:
            print(f"✗ Error lanzando GUI: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def configuration_menu(self):
        """Menú de configuración"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("╔" + "═" * 40 + "╗")
            print("║" + " CONFIGURACIÓN".center(40) + "║")
            print("╠" + "═" * 40 + "╣")
            print("║ 1. Verificar Base de Datos" + " " * 13 + "║")
            print("║ 2. Reinicializar BD" + " " * 19 + "║")
            print("║ 3. Cargar Datos de Prueba" + " " * 13 + "║")
            print("║ 4. Información del Sistema" + " " * 11 + "║")
            print("║ 0. Volver al Menú Principal" + " " * 9 + "║")
            print("╚" + "═" * 40 + "╝")
            
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == '1':
                self.verify_database()
            elif choice == '2':
                self.reinitialize_database()
            elif choice == '3':
                self.load_test_data()
            elif choice == '4':
                self.system_information()
            elif choice == '0':
                break
            else:
                print("Opción inválida. Presione Enter para continuar...")
                input()
    
    def verify_database(self):
        """Verifica el estado de la base de datos"""
        print("\n" + "═" * 50)
        print("VERIFICACIÓN DE BASE DE DATOS")
        print("═" * 50)
        
        try:
            if self.db_config.connect():
                print("✓ Conexión a MySQL exitosa")
                
                # Verificar tablas
                connection = self.db_config.get_connection()
                cursor = connection.cursor()
                
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                expected_tables = ['estudiantes', 'cursos', 'matriculas']
                existing_tables = [table[0] for table in tables]
                
                print(f"✓ Base de datos: {self.db_config.database}")
                print(f"✓ Tablas encontradas: {len(existing_tables)}")
                
                for table in expected_tables:
                    if table in existing_tables:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        print(f"  - {table}: {count} registros")
                    else:
                        print(f"  - {table}: ✗ NO EXISTE")
                
                cursor.close()
                connection.close()
                
            else:
                print("✗ Error conectando a la base de datos")
                
        except Exception as e:
            print(f"✗ Error verificando base de datos: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def load_test_data(self):
        """Carga datos de prueba en el sistema"""
        print("\n" + "═" * 50)
        print("CARGA DE DATOS DE PRUEBA")
        print("═" * 50)
        
        try:
            print("Cargando datos de prueba...")
            
            # Datos de estudiantes de prueba
            estudiantes_prueba = [
                ("EST001", "Juan", "Pérez", "INGENIERIA DE SISTEMAS", "juan.perez@email.com", "123456789"),
                ("EST002", "María", "González", "ADMINISTRACION", "maria.gonzalez@email.com", "987654321"),
                ("EST003", "Carlos", "Rodríguez", "INGENIERIA INDUSTRIAL", "carlos.rodriguez@email.com", "456789123"),
                ("EST004", "Ana", "López", "MEDICINA", "ana.lopez@email.com", "789123456"),
                ("EST005", "Luis", "Martínez", "DERECHO", "luis.martinez@email.com", "321654987")
            ]
            
            # Datos de cursos de prueba
            cursos_prueba = [
                ("MAT101", "Matemáticas I", 4, "Dr. García", "Lun-Mie-Vie 8:00-10:00", 30),
                ("FIS101", "Física I", 4, "Dra. Herrera", "Mar-Jue 10:00-12:00", 25),
                ("QUI101", "Química General", 3, "Dr. Morales", "Lun-Mie 14:00-16:00", 20),
                ("ING101", "Introducción a la Ingeniería", 2, "Ing. Vargas", "Vie 16:00-18:00", 35),
                ("ADM101", "Fundamentos de Administración", 3, "Lic. Ruiz", "Mar-Jue 8:00-10:00", 40)
            ]
            
            # Insertar estudiantes
            estudiantes_insertados = 0
            for codigo, nombre, apellido, carrera, email, telefono in estudiantes_prueba:
                try:
                    if not self.estudiante_dao.exists_codigo(codigo):
                        estudiante = Estudiante(codigo, nombre, apellido, carrera, email, telefono)
                        self.estudiante_dao.create(estudiante)
                        estudiantes_insertados += 1
                except Exception as e:
                    print(f"Error insertando estudiante {codigo}: {str(e)}")
            
            # Insertar cursos
            cursos_insertados = 0
            for codigo, nombre, creditos, profesor, horario, cupos in cursos_prueba:
                try:
                    if not self.curso_dao.exists_codigo(codigo):
                        curso = Curso(codigo, nombre, creditos, profesor, horario, cupos)
                        self.curso_dao.create(curso)
                        cursos_insertados += 1
                except Exception as e:
                    print(f"Error insertando curso {codigo}: {str(e)}")
            
            print(f"✓ Datos de prueba cargados:")
            print(f"  - Estudiantes insertados: {estudiantes_insertados}")
            print(f"  - Cursos insertados: {cursos_insertados}")
            
            # Crear algunas matrículas de prueba
            matriculas_prueba = [
                ("EST001", "MAT101"),
                ("EST001", "FIS101"),
                ("EST002", "ADM101"),
                ("EST003", "ING101"),
                ("EST004", "QUI101")
            ]
            
            matriculas_insertadas = 0
            for est_codigo, curso_codigo in matriculas_prueba:
                try:
                    success, message = self.matricula_service.matricular_estudiante(est_codigo, curso_codigo)
                    if success:
                        matriculas_insertadas += 1
                except Exception as e:
                    print(f"Error creando matrícula {est_codigo}-{curso_codigo}: {str(e)}")
            
            print(f"  - Matrículas creadas: {matriculas_insertadas}")
            
        except Exception as e:
            print(f"✗ Error cargando datos de prueba: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def system_information(self):
        """Muestra información del sistema"""
        print("\n" + "═" * 60)
        print("INFORMACIÓN DEL SISTEMA")
        print("═" * 60)
        
        try:
            import sys
            import platform
            
            print(f"INFORMACIÓN TÉCNICA:")
            print(f"- Lenguaje: Python {sys.version}")
            print(f"- Plataforma: {platform.system()} {platform.release()}")
            print(f"- Arquitectura: {platform.machine()}")
            
            print(f"\nCARACTERÍSTICAS DEL PROYECTO:")
            print(f"- Paradigmas implementados: POO, Funcional, Lógico")
            print(f"- Base de datos: MySQL (XAMPP)")
            print(f"- Interfaz: Consola + GUI (tkinter)")
            print(f"- Librerías: pandas, numpy, matplotlib, mysql-connector")
            
            print(f"\nPARADIGMAS APLICADOS:")
            print(f"- POO: Clases, herencia, encapsulación, polimorfismo")
            print(f"- Funcional: map(), filter(), lambda, funciones de orden superior")
            print(f"- Lógico: Predicados, reglas de negocio, validaciones")
            
            print(f"\nFUNCIONALIDADES:")
            print(f"- Gestión completa de estudiantes, cursos y matrículas")
            print(f"- Reportes y estadísticas avanzadas")
            print(f"- Análisis de datos con pandas y numpy")
            print(f"- Interfaz gráfica con tkinter")
            print(f"- Exportación a CSV y Excel")
            print(f"- Comparación de lenguajes de programación")
            
        except Exception as e:
            print(f"✗ Error obteniendo información: {str(e)}")
        
        input("\nPresione Enter para continuar...")
    
    def exit_application(self):
        """Sale de la aplicación"""
        print("\n" + "═" * 50)
        print("SALIENDO DEL SISTEMA")
        print("═" * 50)
        
        print("Gracias por usar el Sistema de Matrículas Universitarias")
        print("Desarrollado con Python - Paradigmas: POO, Funcional, Lógico")
        print("Autor: Sistema de Matrículas Universitarias")
        
        self.running = False
    
    def run(self):
        """
        Ejecuta la aplicación principal
        Punto de entrada del programa
        """
        try:
            # Mostrar mensaje de bienvenida
            self.show_welcome_message()
            
            # Inicializar base de datos
            if not self.initialize_database():
                print("No se pudo inicializar la base de datos. Saliendo...")
                return
            
            # Ejecutar menú principal
            self.show_main_menu()
            
        except KeyboardInterrupt:
            print("\n\nInterrupción por teclado. Saliendo...")
        except Exception as e:
            print(f"\nError crítico: {str(e)}")
        finally:
            # Limpiar recursos
            if hasattr(self, 'db_config'):
                self.db_config.disconnect()

# Funciones auxiliares para la aplicación de consola
def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_for_input(message: str = "Presione Enter para continuar..."):
    """Espera entrada del usuario"""
    input(message)

def format_table_row(values: List[str], widths: List[int]) -> str:
    """
    Formatea una fila de tabla con anchos específicos
    Programación funcional: uso de zip y map
    """
    formatted_values = [str(val)[:width].ljust(width) for val, width in zip(values, widths)]
    return " | ".join(formatted_values)

def validate_input(prompt: str, validator: callable, error_message: str = "Entrada inválida") -> Any:
    """
    Valida entrada del usuario usando un predicado
    Programación funcional: función de orden superior
    """
    while True:
        try:
            value = input(prompt).strip()
            if validator(value):
                return value
            else:
                print(error_message)
        except KeyboardInterrupt:
            raise
        except Exception:
            print(error_message)

# Predicados para validación
is_not_empty = lambda x: bool(x.strip())
is_numeric = lambda x: x.isdigit()
is_valid_email = lambda x: '@' in x and '.' in x
is_yes_no = lambda x: x.lower() in ['s', 'n', 'si', 'no', 'y', 'yes']

if __name__ == "__main__":
    # Punto de entrada de la aplicación
    app = ConsoleApp()
    app.run()