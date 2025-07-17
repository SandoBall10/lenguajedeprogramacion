"""
Autor: Sistema de Matrículas Universitarias
Módulo: Ventana Principal GUI
Descripción: Interfaz gráfica principal usando tkinter
Paradigma: POO con eventos
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, List
import logging

# Importar servicios y modelos
from services.matricula_service import MatriculaService
from dao.estudiante_dao import EstudianteDAO
from dao.curso_dao import CursoDAO
from dao.matricula_dao import MatriculaDAO
from models.estudiante import Estudiante
from models.curso import Curso
from config.database import DatabaseConfig

class MainWindow:
    """
    Ventana principal de la aplicación
    Implementa interfaz gráfica con tkinter
    """
    
    def __init__(self):
        """Constructor de la ventana principal"""
        self.root = tk.Tk()
        self.root.title("Sistema de Matrículas Universitarias")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Inicializar base de datos primero
        self.db_config = DatabaseConfig()
        if not self._initialize_database():
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        
        # Servicios y DAOs
        self.matricula_service = MatriculaService()
        self.estudiante_dao = EstudianteDAO()
        self.curso_dao = CursoDAO()
        self.matricula_dao = MatriculaDAO()
        
        # Logger
        self.logger = logging.getLogger(__name__)
        
        # Variables de control
        self.current_tab = tk.StringVar(value="estudiantes")
        
        # Configurar estilos
        self._configure_styles()
        
        # Crear interfaz
        self._create_widgets()
        
        # Cargar datos iniciales
        self._load_initial_data()
    
    def _initialize_database(self) -> bool:
        """Inicializa la base de datos y crea las tablas necesarias"""
        try:
            return self.db_config.create_database_and_tables()
        except Exception as e:
            print(f"Error inicializando base de datos: {e}")
            return False
    
    def _configure_styles(self):
        """Configura estilos personalizados para la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores y fuentes
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background='#f0f0f0')
        style.configure('Custom.TButton', font=('Arial', 10))
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def _create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Título principal
        title_label = ttk.Label(
            self.root, 
            text="Sistema de Matrículas Universitarias", 
            style='Title.TLabel'
        )
        title_label.pack(pady=10)
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Crear pestañas
        self._create_students_tab()
        self._create_courses_tab()
        self._create_enrollments_tab()
        self._create_reports_tab()
        
        # Barra de estado
        self.status_bar = ttk.Label(
            self.root, 
            text="Listo", 
            relief='sunken', 
            anchor='w'
        )
        self.status_bar.pack(side='bottom', fill='x')
    
    def _create_students_tab(self):
        """Crea la pestaña de gestión de estudiantes"""
        # Frame principal para estudiantes
        students_frame = ttk.Frame(self.notebook)
        self.notebook.add(students_frame, text="Estudiantes")
        
        # Frame superior para controles
        controls_frame = ttk.Frame(students_frame)
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        # Botones de acción
        ttk.Button(
            controls_frame, 
            text="Nuevo Estudiante", 
            command=self._new_student_dialog,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame, 
            text="Editar Estudiante", 
            command=self._edit_student_dialog,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame, 
            text="Eliminar Estudiante", 
            command=self._delete_student,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame, 
            text="Actualizar Lista", 
            command=self._refresh_students,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        # Frame para búsqueda
        search_frame = ttk.Frame(students_frame)
        search_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(search_frame, text="Buscar:").pack(side='left', padx=5)
        self.student_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.student_search_var)
        search_entry.pack(side='left', padx=5, fill='x', expand=True)
        search_entry.bind('<KeyRelease>', self._search_students)
        
        # Treeview para mostrar estudiantes
        columns = ('Código', 'Nombre', 'Apellido', 'Carrera', 'Email', 'Teléfono')
        self.students_tree = ttk.Treeview(students_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=150, anchor='center')
        
        # Scrollbars
        students_scrollbar_v = ttk.Scrollbar(students_frame, orient='vertical', command=self.students_tree.yview)
        students_scrollbar_h = ttk.Scrollbar(students_frame, orient='horizontal', command=self.students_tree.xview)
        self.students_tree.configure(yscrollcommand=students_scrollbar_v.set, xscrollcommand=students_scrollbar_h.set)
        
        # Empaquetar treeview y scrollbars
        self.students_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        students_scrollbar_v.pack(side='right', fill='y')
        students_scrollbar_h.pack(side='bottom', fill='x')
    
    def _create_courses_tab(self):
        """Crea la pestaña de gestión de cursos"""
        # Frame principal para cursos
        courses_frame = ttk.Frame(self.notebook)
        self.notebook.add(courses_frame, text="Cursos")
        
        # Frame superior para controles
        controls_frame = ttk.Frame(courses_frame)
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        # Botones de acción
        ttk.Button(
            controls_frame, 
            text="Nuevo Curso", 
            command=self._new_course_dialog,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame, 
            text="Editar Curso", 
            command=self._edit_course_dialog,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame, 
            text="Eliminar Curso", 
            command=self._delete_course,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame, 
            text="Actualizar Lista", 
            command=self._refresh_courses,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        # Treeview para mostrar cursos
        columns = ('Código', 'Nombre', 'Créditos', 'Profesor', 'Horario', 'Cupos Disp.', 'Matriculados')
        self.courses_tree = ttk.Treeview(courses_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        for col in columns:
            self.courses_tree.heading(col, text=col)
            self.courses_tree.column(col, width=120, anchor='center')
        
        # Scrollbars
        courses_scrollbar_v = ttk.Scrollbar(courses_frame, orient='vertical', command=self.courses_tree.yview)
        courses_scrollbar_h = ttk.Scrollbar(courses_frame, orient='horizontal', command=self.courses_tree.xview)
        self.courses_tree.configure(yscrollcommand=courses_scrollbar_v.set, xscrollcommand=courses_scrollbar_h.set)
        
        # Empaquetar treeview y scrollbars
        self.courses_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        courses_scrollbar_v.pack(side='right', fill='y')
        courses_scrollbar_h.pack(side='bottom', fill='x')
    
    def _create_enrollments_tab(self):
        """Crea la pestaña de gestión de matrículas"""
        # Frame principal para matrículas
        enrollments_frame = ttk.Frame(self.notebook)
        self.notebook.add(enrollments_frame, text="Matrículas")
        
        # Frame superior para controles
        controls_frame = ttk.Frame(enrollments_frame)
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        # Botones de acción
        ttk.Button(
            controls_frame, 
            text="Nueva Matrícula", 
            command=self._new_enrollment_dialog,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame, 
            text="Cancelar Matrícula", 
            command=self._cancel_enrollment,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame, 
            text="Actualizar Lista", 
            command=self._refresh_enrollments,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        # Frame para filtros
        filter_frame = ttk.Frame(enrollments_frame)
        filter_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Filtrar por:").pack(side='left', padx=5)
        
        self.enrollment_filter = ttk.Combobox(
            filter_frame, 
            values=['Todas', 'Activas', 'Canceladas', 'Completadas'],
            state='readonly'
        )
        self.enrollment_filter.set('Activas')
        self.enrollment_filter.pack(side='left', padx=5)
        self.enrollment_filter.bind('<<ComboboxSelected>>', self._filter_enrollments)
        
        # Treeview para mostrar matrículas
        columns = ('ID', 'Estudiante', 'Curso', 'Fecha Matrícula', 'Estado')
        self.enrollments_tree = ttk.Treeview(enrollments_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        column_widths = {'ID': 50, 'Estudiante': 200, 'Curso': 200, 'Fecha Matrícula': 150, 'Estado': 100}
        for col in columns:
            self.enrollments_tree.heading(col, text=col)
            self.enrollments_tree.column(col, width=column_widths.get(col, 150), anchor='center')
        
        # Scrollbars
        enrollments_scrollbar_v = ttk.Scrollbar(enrollments_frame, orient='vertical', command=self.enrollments_tree.yview)
        enrollments_scrollbar_h = ttk.Scrollbar(enrollments_frame, orient='horizontal', command=self.enrollments_tree.xview)
        self.enrollments_tree.configure(yscrollcommand=enrollments_scrollbar_v.set, xscrollcommand=enrollments_scrollbar_h.set)
        
        # Empaquetar treeview y scrollbars
        self.enrollments_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        enrollments_scrollbar_v.pack(side='right', fill='y')
        enrollments_scrollbar_h.pack(side='bottom', fill='x')
    
    def _create_reports_tab(self):
        """Crea la pestaña de reportes"""
        # Frame principal para reportes
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reportes")
        
        # Frame superior para controles
        controls_frame = ttk.Frame(reports_frame)
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        # Botones de reportes
        ttk.Button(
            controls_frame, 
            text="Reporte General", 
            command=self._generate_general_report,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame, 
            text="Exportar a CSV", 
            command=self._export_to_csv,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        ttk.Button(
            controls_frame, 
            text="Estadísticas", 
            command=self._show_statistics,
            style='Custom.TButton'
        ).pack(side='left', padx=5)
        
        # Text widget para mostrar reportes
        self.report_text = tk.Text(reports_frame, wrap='word', font=('Courier', 10))
        
        # Scrollbar para el texto
        report_scrollbar = ttk.Scrollbar(reports_frame, orient='vertical', command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=report_scrollbar.set)
        
        # Empaquetar widgets
        self.report_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        report_scrollbar.pack(side='right', fill='y')
    
    def _load_initial_data(self):
        """Carga datos iniciales en las pestañas"""
        try:
            self._refresh_students()
            self._refresh_courses()
            self._refresh_enrollments()
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando datos iniciales: {str(e)}")
    
    def _refresh_students(self):
        """Actualiza la lista de estudiantes"""
        try:
            # Limpiar treeview
            for item in self.students_tree.get_children():
                self.students_tree.delete(item)
            
            # Obtener estudiantes
            estudiantes = self.estudiante_dao.find_all()
            
            # Agregar estudiantes al treeview
            for estudiante in estudiantes:
                self.students_tree.insert('', 'end', values=(
                    estudiante.codigo,
                    estudiante.nombre,
                    estudiante.apellido,
                    estudiante.carrera,
                    estudiante.email,
                    estudiante.telefono
                ))
            
            self._update_status(f"Cargados {len(estudiantes)} estudiantes")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando estudiantes: {str(e)}")
            self.logger.error(f"Error cargando estudiantes: {e}")
    
    def _refresh_courses(self):
        """Actualiza la lista de cursos"""
        try:
            # Limpiar treeview
            for item in self.courses_tree.get_children():
                self.courses_tree.delete(item)
            
            # Obtener cursos
            cursos = self.curso_dao.find_all()
            
            # Agregar cursos al treeview
            for curso in cursos:
                self.courses_tree.insert('', 'end', values=(
                    curso.codigo,
                    curso.nombre,
                    curso.creditos,
                    curso.profesor,
                    curso.horario,
                    curso.cupos_disponibles,
                    curso.cupos_ocupados
                ))
            
            self._update_status(f"Cargados {len(cursos)} cursos")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando cursos: {str(e)}")
            self.logger.error(f"Error cargando cursos: {e}")
    
    def _refresh_enrollments(self):
        """Actualiza la lista de matrículas"""
        try:
            # Limpiar treeview
            for item in self.enrollments_tree.get_children():
                self.enrollments_tree.delete(item)
            
            # Obtener matrículas según filtro
            filter_value = self.enrollment_filter.get()
            
            if filter_value == 'Activas':
                matriculas = self.matricula_dao.find_active_matriculas()
            else:
                matriculas = self.matricula_dao.find_all()
                if filter_value != 'Todas':
                    # Filtrar por estado específico
                    from models.matricula import EstadoMatricula
                    estado_filtro = EstadoMatricula(filter_value.upper())
                    matriculas = [m for m in matriculas if m.estado == estado_filtro]
            
            # Agregar matrículas al treeview con información detallada
            for matricula in matriculas:
                # Obtener información del estudiante y curso
                estudiante = self.estudiante_dao.find_by_codigo(matricula.estudiante_codigo)
                curso = self.curso_dao.find_by_codigo(matricula.curso_codigo)
                
                estudiante_info = f"{estudiante.nombre} {estudiante.apellido} ({estudiante.codigo})" if estudiante else matricula.estudiante_codigo
                curso_info = f"{curso.nombre} ({curso.codigo})" if curso else matricula.curso_codigo
                
                self.enrollments_tree.insert('', 'end', values=(
                    matricula.id or '',
                    estudiante_info,
                    curso_info,
                    matricula.fecha_matricula.strftime('%Y-%m-%d %H:%M'),
                    matricula.estado.value
                ))
            
            self._update_status(f"Cargadas {len(matriculas)} matrículas")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando matrículas: {str(e)}")
            self.logger.error(f"Error cargando matrículas: {e}")
    
    def _update_status(self, message: str):
        """Actualiza la barra de estado"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()

    # Métodos de diálogo corregidos
    def _new_student_dialog(self):
        """Diálogo para crear nuevo estudiante"""
        try:
            dialog = StudentDialog(self.root, "Nuevo Estudiante")
            self.root.wait_window(dialog.dialog)  # Esperar a que se cierre el diálogo
            
            if dialog.result:
                # Verificar que el código no exista
                if self.estudiante_dao.exists_codigo(dialog.result['codigo']):
                    messagebox.showerror("Error", f"Ya existe un estudiante con código {dialog.result['codigo']}")
                    return
                
                estudiante = Estudiante(**dialog.result)
                estudiante_id = self.estudiante_dao.create(estudiante)
                
                if estudiante_id:
                    self._refresh_students()
                    messagebox.showinfo("Éxito", f"Estudiante creado exitosamente con ID: {estudiante_id}")
                else:
                    messagebox.showerror("Error", "No se pudo crear el estudiante")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error creando estudiante: {str(e)}")
            self.logger.error(f"Error creando estudiante: {e}")
    
    def _edit_student_dialog(self):
        """Diálogo para editar estudiante"""
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para editar")
            return
        
        try:
            # Obtener datos del estudiante seleccionado
            item = self.students_tree.item(selection[0])
            values = item['values']
            
            # Crear diálogo con datos existentes
            initial_data = {
                'codigo': values[0],
                'nombre': values[1],
                'apellido': values[2],
                'carrera': values[3],
                'email': values[4],
                'telefono': values[5]
            }
            
            dialog = StudentDialog(self.root, "Editar Estudiante", initial_data)
            self.root.wait_window(dialog.dialog)
            
            if dialog.result:
                estudiante = Estudiante(**dialog.result)
                if self.estudiante_dao.update(estudiante):
                    self._refresh_students()
                    messagebox.showinfo("Éxito", "Estudiante actualizado exitosamente")
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el estudiante")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error actualizando estudiante: {str(e)}")
            self.logger.error(f"Error actualizando estudiante: {e}")
    
    def _delete_student(self):
        """Elimina un estudiante"""
        selection = self.students_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un estudiante para eliminar")
            return
        
        try:
            item = self.students_tree.item(selection[0])
            codigo = item['values'][0]
            nombre = f"{item['values'][1]} {item['values'][2]}"
            
            if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al estudiante {nombre}?"):
                if self.estudiante_dao.delete_by_codigo(codigo):
                    self._refresh_students()
                    messagebox.showinfo("Éxito", "Estudiante eliminado exitosamente")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el estudiante")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error eliminando estudiante: {str(e)}")
            self.logger.error(f"Error eliminando estudiante: {e}")
    
    def _search_students(self, event=None):
        """Busca estudiantes por nombre"""
        search_term = self.student_search_var.get()
        if not search_term:
            self._refresh_students()
            return
        
        try:
            estudiantes = self.estudiante_dao.search_by_name(search_term)
            
            # Limpiar y actualizar treeview
            for item in self.students_tree.get_children():
                self.students_tree.delete(item)
            
            for estudiante in estudiantes:
                self.students_tree.insert('', 'end', values=(
                    estudiante.codigo,
                    estudiante.nombre,
                    estudiante.apellido,
                    estudiante.carrera,
                    estudiante.email,
                    estudiante.telefono
                ))
            
            self._update_status(f"Encontrados {len(estudiantes)} estudiantes")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda: {str(e)}")
            self.logger.error(f"Error en búsqueda: {e}")
    
    def _new_course_dialog(self):
        """Diálogo para crear nuevo curso"""
        try:
            dialog = CourseDialog(self.root, "Nuevo Curso")
            self.root.wait_window(dialog.dialog)
            
            if dialog.result:
                # Verificar que el código no exista
                if self.curso_dao.exists_codigo(dialog.result['codigo']):
                    messagebox.showerror("Error", f"Ya existe un curso con código {dialog.result['codigo']}")
                    return
                
                curso = Curso(**dialog.result)
                curso_id = self.curso_dao.create(curso)
                
                if curso_id:
                    self._refresh_courses()
                    messagebox.showinfo("Éxito", f"Curso creado exitosamente con ID: {curso_id}")
                else:
                    messagebox.showerror("Error", "No se pudo crear el curso")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error creando curso: {str(e)}")
            self.logger.error(f"Error creando curso: {e}")
    
    def _edit_course_dialog(self):
        """Diálogo para editar curso"""
        selection = self.courses_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un curso para editar")
            return
        
        try:
            item = self.courses_tree.item(selection[0])
            values = item['values']
            
            initial_data = {
                'codigo': values[0],
                'nombre': values[1],
                'creditos': int(values[2]),
                'profesor': values[3],
                'horario': values[4],
                'cupos_disponibles': int(values[5]) + int(values[6])  # Total de cupos
            }
            
            dialog = CourseDialog(self.root, "Editar Curso", initial_data)
            self.root.wait_window(dialog.dialog)
            
            if dialog.result:
                curso = Curso(**dialog.result)
                if self.curso_dao.update(curso):
                    self._refresh_courses()
                    messagebox.showinfo("Éxito", "Curso actualizado exitosamente")
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el curso")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error actualizando curso: {str(e)}")
            self.logger.error(f"Error actualizando curso: {e}")
    
    def _delete_course(self):
        """Elimina un curso"""
        selection = self.courses_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un curso para eliminar")
            return
        
        try:
            item = self.courses_tree.item(selection[0])
            codigo = item['values'][0]
            nombre = item['values'][1]
            
            if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el curso {nombre}?"):
                if self.curso_dao.delete_by_codigo(codigo):
                    self._refresh_courses()
                    messagebox.showinfo("Éxito", "Curso eliminado exitosamente")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el curso")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error eliminando curso: {str(e)}")
            self.logger.error(f"Error eliminando curso: {e}")
    
    def _new_enrollment_dialog(self):
        """Diálogo para crear nueva matrícula"""
        try:
            dialog = EnrollmentDialog(self.root, self.estudiante_dao, self.curso_dao)
            self.root.wait_window(dialog.dialog)
            
            if dialog.result:
                estudiante_codigo = dialog.result['estudiante_codigo']
                curso_codigo = dialog.result['curso_codigo']
                
                success, message = self.matricula_service.matricular_estudiante(estudiante_codigo, curso_codigo)
                
                if success:
                    self._refresh_enrollments()
                    self._refresh_courses()  # Actualizar cupos
                    messagebox.showinfo("Éxito", message)
                else:
                    messagebox.showerror("Error", message)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error en matrícula: {str(e)}")
            self.logger.error(f"Error en matrícula: {e}")
    
    def _cancel_enrollment(self):
        """Cancela una matrícula"""
        selection = self.enrollments_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una matrícula para cancelar")
            return
        
        try:
            item = self.enrollments_tree.item(selection[0])
            values = item['values']
            
            if values[4] != 'ACTIVA':
                messagebox.showwarning("Advertencia", "Solo se pueden cancelar matrículas activas")
                return
            
            # Extraer códigos de estudiante y curso
            estudiante_info = values[1]
            curso_info = values[2]
            
            # Obtener códigos (están entre paréntesis)
            estudiante_codigo = estudiante_info.split('(')[1].split(')')[0]
            curso_codigo = curso_info.split('(')[1].split(')')[0]
            
            if messagebox.askyesno("Confirmar", f"¿Está seguro de cancelar esta matrícula?"):
                success, message = self.matricula_service.cancelar_matricula(estudiante_codigo, curso_codigo)
                
                if success:
                    self._refresh_enrollments()
                    self._refresh_courses()
                    messagebox.showinfo("Éxito", message)
                else:
                    messagebox.showerror("Error", message)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error cancelando matrícula: {str(e)}")
            self.logger.error(f"Error cancelando matrícula: {e}")
    
    def _filter_enrollments(self, event=None):
        """Filtra matrículas según selección"""
        self._refresh_enrollments()
    
    def _generate_general_report(self):
        """Genera reporte general del sistema"""
        try:
            reporte = self.matricula_service.generar_reporte_matriculas()
            
            # Limpiar área de texto
            self.report_text.delete(1.0, tk.END)
            
            # Generar texto del reporte
            report_text = "=== REPORTE GENERAL DEL SISTEMA ===\n\n"
            
            # Resumen general
            if 'resumen' in reporte:
                resumen = reporte['resumen']
                report_text += "RESUMEN GENERAL:\n"
                report_text += f"- Total de matrículas: {resumen.get('total_matriculas', 0)}\n"
                report_text += f"- Matrículas activas: {resumen.get('matriculas_activas', 0)}\n"
                report_text += f"- Matrículas canceladas: {resumen.get('matriculas_canceladas', 0)}\n"
                report_text += f"- Matrículas completadas: {resumen.get('matriculas_completadas', 0)}\n"
                report_text += f"- Estudiantes con matrículas: {resumen.get('estudiantes_con_matriculas', 0)}\n\n"
            
            # Estadísticas por carrera
            if 'por_carrera' in reporte:
                report_text += "MATRÍCULAS POR CARRERA:\n"
                for carrera, cantidad in reporte['por_carrera'].items():
                    report_text += f"- {carrera}: {cantidad} matrículas\n"
                report_text += "\n"
            
            # Estadísticas por curso
            if 'por_curso' in reporte:
                report_text += "MATRÍCULAS POR CURSO:\n"
                for curso, cantidad in reporte['por_curso'].items():
                    report_text += f"- {curso}: {cantidad} estudiantes\n"
                report_text += "\n"
            
            # Porcentajes
            if 'porcentajes' in reporte:
                porcentajes = reporte['porcentajes']
                report_text += "DISTRIBUCIÓN PORCENTUAL:\n"
                report_text += f"- Activas: {porcentajes.get('activas', 0)}%\n"
                report_text += f"- Canceladas: {porcentajes.get('canceladas', 0)}%\n"
                report_text += f"- Completadas: {porcentajes.get('completadas', 0)}%\n"
            
            # Mostrar reporte
            self.report_text.insert(1.0, report_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generando reporte: {str(e)}")
            self.logger.error(f"Error generando reporte: {e}")
    
    def _export_to_csv(self):
        """Exporta datos a CSV"""
        try:
            from tkinter import filedialog
            import csv
            from datetime import datetime
            
            # Seleccionar archivo
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Guardar reporte como..."
            )
            
            if filename:
                # Obtener datos de matrículas
                reporte_data = self.matricula_dao.get_enrollment_report()
                
                # Escribir CSV
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = [
                        'estudiante_codigo', 'estudiante_nombre', 'carrera',
                        'curso_codigo', 'curso_nombre', 'creditos',
                        'fecha_matricula', 'estado'
                    ]
                    
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for row in reporte_data:
                        writer.writerow(row)
                
                messagebox.showinfo("Éxito", f"Reporte exportado a: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error exportando a CSV: {str(e)}")
            self.logger.error(f"Error exportando a CSV: {e}")
    
    def _show_statistics(self):
        """Muestra estadísticas detalladas"""
        try:
            stats = self.matricula_dao.get_statistics()
            
            # Crear ventana de estadísticas
            stats_window = tk.Toplevel(self.root)
            stats_window.title("Estadísticas del Sistema")
            stats_window.geometry("500x400")
            stats_window.configure(bg='#f0f0f0')
            
            # Crear texto con estadísticas
            stats_text = tk.Text(stats_window, wrap='word', font=('Courier', 10))
            stats_scrollbar = ttk.Scrollbar(stats_window, orient='vertical', command=stats_text.yview)
            stats_text.configure(yscrollcommand=stats_scrollbar.set)
            
            # Generar contenido
            content = "=== ESTADÍSTICAS DETALLADAS ===\n\n"
            content += f"Total de matrículas: {stats.get('total_matriculas', 0)}\n"
            content += f"Matrículas activas: {stats.get('matriculas_activas', 0)}\n"
            content += f"Matrículas canceladas: {stats.get('matriculas_canceladas', 0)}\n"
            content += f"Matrículas completadas: {stats.get('matriculas_completadas', 0)}\n\n"
            
            content += f"Estudiantes con matrículas activas: {stats.get('estudiantes_con_matriculas', 0)}\n"
            content += f"Cursos con matrículas activas: {stats.get('cursos_con_matriculas', 0)}\n\n"
            
            content += "DISTRIBUCIÓN PORCENTUAL:\n"
            content += f"- Activas: {stats.get('porcentaje_activas', 0)}%\n"
            content += f"- Canceladas: {stats.get('porcentaje_canceladas', 0)}%\n"
            content += f"- Completadas: {stats.get('porcentaje_completadas', 0)}%\n"
            
            stats_text.insert(1.0, content)
            stats_text.config(state='disabled')
            
            # Empaquetar widgets
            stats_text.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            stats_scrollbar.pack(side='right', fill='y', pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error mostrando estadísticas: {str(e)}")
            self.logger.error(f"Error mostrando estadísticas: {e}")

# Clases de diálogo corregidas
class StudentDialog:
    """Diálogo para crear/editar estudiantes"""
    
    def __init__(self, parent, title, initial_data=None):
        self.result = None
        
        # Crear ventana
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x350")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Variables
        self.codigo_var = tk.StringVar(value=initial_data.get('codigo', '') if initial_data else '')
        self.nombre_var = tk.StringVar(value=initial_data.get('nombre', '') if initial_data else '')
        self.apellido_var = tk.StringVar(value=initial_data.get('apellido', '') if initial_data else '')
        self.carrera_var = tk.StringVar(value=initial_data.get('carrera', '') if initial_data else '')
        self.email_var = tk.StringVar(value=initial_data.get('email', '') if initial_data else '')
        self.telefono_var = tk.StringVar(value=initial_data.get('telefono', '') if initial_data else '')
        
        self._create_widgets()
        
        # Centrar ventana
        self._center_window()
        
        # Enfocar primer campo
        self.codigo_entry.focus_set()
    
    def _center_window(self):
        """Centra la ventana en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Crea los widgets del diálogo"""
        # Frame principal
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Campos del formulario
        row = 0
        
        # Código
        ttk.Label(main_frame, text="Código:*").grid(row=row, column=0, sticky='w', pady=5)
        self.codigo_entry = ttk.Entry(main_frame, textvariable=self.codigo_var)
        self.codigo_entry.grid(row=row, column=1, sticky='ew', padx=(10, 0), pady=5)
        row += 1
        
        # Nombre
        ttk.Label(main_frame, text="Nombre:*").grid(row=row, column=0, sticky='w', pady=5)
        self.nombre_entry = ttk.Entry(main_frame, textvariable=self.nombre_var)
        self.nombre_entry.grid(row=row, column=1, sticky='ew', padx=(10, 0), pady=5)
        row += 1
        
        # Apellido
        ttk.Label(main_frame, text="Apellido:*").grid(row=row, column=0, sticky='w', pady=5)
        self.apellido_entry = ttk.Entry(main_frame, textvariable=self.apellido_var)
        self.apellido_entry.grid(row=row, column=1, sticky='ew', padx=(10, 0), pady=5)
        row += 1
        
        # Carrera
        ttk.Label(main_frame, text="Carrera:*").grid(row=row, column=0, sticky='w', pady=5)
        self.carrera_combo = ttk.Combobox(
            main_frame, 
            textvariable=self.carrera_var,
            values=[
                'INGENIERIA DE SISTEMAS', 'INGENIERIA INDUSTRIAL',
                'ADMINISTRACION', 'CONTADURIA', 'DERECHO',
                'MEDICINA', 'PSICOLOGIA', 'ARQUITECTURA'
            ],
            state='readonly'
        )
        self.carrera_combo.grid(row=row, column=1, sticky='ew', padx=(10, 0), pady=5)
        row += 1
        
        # Email
        ttk.Label(main_frame, text="Email:").grid(row=row, column=0, sticky='w', pady=5)
        self.email_entry = ttk.Entry(main_frame, textvariable=self.email_var)
        self.email_entry.grid(row=row, column=1, sticky='ew', padx=(10, 0), pady=5)
        row += 1
        
        # Teléfono
        ttk.Label(main_frame, text="Teléfono:").grid(row=row, column=0, sticky='w', pady=5)
        self.telefono_entry = ttk.Entry(main_frame, textvariable=self.telefono_var)
        self.telefono_entry.grid(row=row, column=1, sticky='ew', padx=(10, 0), pady=5)
        row += 1
        
        # Nota de campos obligatorios
        ttk.Label(main_frame, text="* Campos obligatorios", font=('Arial', 8)).grid(
            row=row, column=0, columnspan=2, pady=5
        )
        row += 1
        
        # Configurar columnas
        main_frame.columnconfigure(1, weight=1)
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Guardar", command=self._accept).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self._cancel).pack(side='left', padx=5)
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self._accept())
        self.dialog.bind('<Escape>', lambda e: self._cancel())
    
    def _accept(self):
        """Acepta el diálogo y valida datos"""
        try:
            # Validar campos requeridos
            codigo = self.codigo_var.get().strip()
            nombre = self.nombre_var.get().strip()
            apellido = self.apellido_var.get().strip()
            carrera = self.carrera_var.get().strip()
            
            if not all([codigo, nombre, apellido, carrera]):
                messagebox.showerror("Error", "Todos los campos marcados con * son obligatorios")
                return
            
            # Validar email si se proporciona
            email = self.email_var.get().strip()
            if email:
                import re
                patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(patron, email):
                    messagebox.showerror("Error", "Formato de email inválido")
                    return
            
            self.result = {
                'codigo': codigo.upper(),
                'nombre': nombre.title(),
                'apellido': apellido.title(),
                'carrera': carrera.upper(),
                'email': email.lower(),
                'telefono': self.telefono_var.get().strip()
            }
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error validando datos: {str(e)}")
    
    def _cancel(self):
        """Cancela el diálogo"""
        self.dialog.destroy()

class CourseDialog:
    """Diálogo para crear/editar cursos"""
    
    def __init__(self, parent, title, initial_data=None):
        self.result = None
        
        # Crear ventana
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x400")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Variables
        self.codigo_var = tk.StringVar(value=initial_data.get('codigo', '') if initial_data else '')
        self.nombre_var = tk.StringVar(value=initial_data.get('nombre', '') if initial_data else '')
        self.creditos_var = tk.IntVar(value=initial_data.get('creditos', 3) if initial_data else 3)
        self.profesor_var = tk.StringVar(value=initial_data.get('profesor', '') if initial_data else '')
        self.horario_var = tk.StringVar(value=initial_data.get('horario', '') if initial_data else '')
        self.cupos_var = tk.IntVar(value=initial_data.get('cupos_disponibles', 30) if initial_data else 30)
        
        self._create_widgets()
        self._center_window()
        
        # Enfocar primer campo
        self.codigo_entry.focus_set()
    
    def _center_window(self):
        """Centra la ventana en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Crea los widgets del diálogo"""
        # Frame principal
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        row = 0
        
        # Código
        ttk.Label(main_frame, text="Código:*").grid(row=row, column=0, sticky='w', pady=5)
        self.codigo_entry = ttk.Entry(main_frame, textvariable=self.codigo_var)
        self.codigo_entry.grid(row=row, column=1, sticky='ew', padx=(10, 0), pady=5)
        row += 1
        
        # Nombre
        ttk.Label(main_frame, text="Nombre:*").grid(row=row, column=0, sticky='w', pady=5)
        self.nombre_entry = ttk.Entry(main_frame, textvariable=self.nombre_var)
        self.nombre_entry.grid(row=row, column=1, sticky='ew', padx=(10, 0), pady=5)
        row += 1
        
        # Créditos
        ttk.Label(main_frame, text="Créditos:*").grid(row=row, column=0, sticky='w', pady=5)
        creditos_frame = ttk.Frame(main_frame)
        creditos_frame.grid(row=row, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.creditos_spin = ttk.Spinbox(
            creditos_frame, 
            from_=1, 
            to=6, 
            textvariable=self.creditos_var, 
            width=10,
            state='readonly'
        )
        self.creditos_spin.pack(side='left')
        ttk.Label(creditos_frame, text="(1-6 créditos)").pack(side='left', padx=(10, 0))
        row += 1
        
        # Profesor
        ttk.Label(main_frame, text="Profesor:").grid(row=row, column=0, sticky='w', pady=5)
        self.profesor_entry = ttk.Entry(main_frame, textvariable=self.profesor_var)
        self.profesor_entry.grid(row=row, column=1, sticky='ew', padx=(10, 0), pady=5)
        row += 1
        
        # Horario
        ttk.Label(main_frame, text="Horario:").grid(row=row, column=0, sticky='w', pady=5)
        self.horario_entry = ttk.Entry(main_frame, textvariable=self.horario_var)
        self.horario_entry.grid(row=row, column=1, sticky='ew', padx=(10, 0), pady=5)
        row += 1
        
        # Cupos
        ttk.Label(main_frame, text="Cupos:*").grid(row=row, column=0, sticky='w', pady=5)
        cupos_frame = ttk.Frame(main_frame)
        cupos_frame.grid(row=row, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.cupos_spin = ttk.Spinbox(
            cupos_frame, 
            from_=10, 
            to=100, 
            textvariable=self.cupos_var, 
            width=10,
            state='readonly'
        )
        self.cupos_spin.pack(side='left')
        ttk.Label(cupos_frame, text="(10-100 cupos)").pack(side='left', padx=(10, 0))
        row += 1
        
        # Nota de campos obligatorios
        ttk.Label(main_frame, text="* Campos obligatorios", font=('Arial', 8)).grid(
            row=row, column=0, columnspan=2, pady=5
        )
        row += 1
        
        # Configurar columnas
        main_frame.columnconfigure(1, weight=1)
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Guardar", command=self._accept).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self._cancel).pack(side='left', padx=5)
        
        # Bind keys
        self.dialog.bind('<Return>', lambda e: self._accept())
        self.dialog.bind('<Escape>', lambda e: self._cancel())
    
    def _accept(self):
        """Acepta el diálogo y valida datos"""
        try:
            # Validar campos requeridos
            codigo = self.codigo_var.get().strip()
            nombre = self.nombre_var.get().strip()
            
            if not all([codigo, nombre]):
                messagebox.showerror("Error", "Código y nombre son obligatorios")
                return
            
            # Validar valores numéricos
            creditos = self.creditos_var.get()
            cupos = self.cupos_var.get()
            
            if not (1 <= creditos <= 6):
                messagebox.showerror("Error", "Los créditos deben estar entre 1 y 6")
                return
            
            if not (10 <= cupos <= 100):
                messagebox.showerror("Error", "Los cupos deben estar entre 10 y 100")
                return
            
            self.result = {
                'codigo': codigo.upper(),
                'nombre': nombre.title(),
                'creditos': creditos,
                'profesor': self.profesor_var.get().strip(),
                'horario': self.horario_var.get().strip(),
                'cupos_disponibles': cupos
            }
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error validando datos: {str(e)}")
    
    def _cancel(self):
        """Cancela el diálogo"""
        self.dialog.destroy()

class EnrollmentDialog:
    """Diálogo para crear matrículas"""
    
    def __init__(self, parent, estudiante_dao, curso_dao):
        self.result = None
        self.estudiante_dao = estudiante_dao
        self.curso_dao = curso_dao
        
        # Crear ventana
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nueva Matrícula")
        self.dialog.geometry("600x400")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Variables
        self.estudiante_var = tk.StringVar()
        self.curso_var = tk.StringVar()
        
        self._create_widgets()
        self._load_data()
        self._center_window()
    
    def _center_window(self):
        """Centra la ventana en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _create_widgets(self):
        """Crea los widgets del diálogo"""
        # Frame principal
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Selección de estudiante
        ttk.Label(main_frame, text="Estudiante:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.estudiante_combo = ttk.Combobox(main_frame, textvariable=self.estudiante_var, width=60, state='readonly')
        self.estudiante_combo.grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)
        
        # Selección de curso
        ttk.Label(main_frame, text="Curso:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=(15, 5))
        self.curso_combo = ttk.Combobox(main_frame, textvariable=self.curso_var, width=60, state='readonly')
        self.curso_combo.grid(row=3, column=0, columnspan=2, sticky='ew', pady=5)
        
        # Información adicional
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding=10)
        info_frame.grid(row=4, column=0, columnspan=2, sticky='ew', pady=15)
        
        self.info_label = ttk.Label(
            info_frame, 
            text="Seleccione un estudiante y un curso para ver información adicional.",
            wraplength=500,
            justify='left'
        )
        self.info_label.pack(fill='both', expand=True)
        
        # Configurar columnas
        main_frame.columnconfigure(0, weight=1)
        
        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Matricular", command=self._accept).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self._cancel).pack(side='left', padx=5)
        
        # Bind eventos
        self.estudiante_combo.bind('<<ComboboxSelected>>', self._update_info)
        self.curso_combo.bind('<<ComboboxSelected>>', self._update_info)
        
        # Bind keys
        self.dialog.bind('<Return>', lambda e: self._accept())
        self.dialog.bind('<Escape>', lambda e: self._cancel())
    
    def _load_data(self):
        """Carga datos de estudiantes y cursos"""
        try:
            # Cargar estudiantes
            estudiantes = self.estudiante_dao.find_all()
            estudiante_values = [f"{e.codigo} - {e.nombre} {e.apellido} ({e.carrera})" for e in estudiantes]
            self.estudiante_combo['values'] = estudiante_values
            
            # Cargar cursos con cupos disponibles
            cursos = self.curso_dao.find_with_available_spots()
            curso_values = [f"{c.codigo} - {c.nombre} (Créditos: {c.creditos}, Cupos: {c.cupos_disponibles})" for c in cursos]
            self.curso_combo['values'] = curso_values
            
            if not estudiante_values:
                messagebox.showwarning("Advertencia", "No hay estudiantes registrados")
            
            if not curso_values:
                messagebox.showwarning("Advertencia", "No hay cursos con cupos disponibles")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando datos: {str(e)}")
    
    def _update_info(self, event=None):
        """Actualiza información adicional"""
        try:
            estudiante_sel = self.estudiante_var.get()
            curso_sel = self.curso_var.get()
            
            info_text = ""
            
            if estudiante_sel:
                codigo_estudiante = estudiante_sel.split(' - ')[0]
                estudiante = self.estudiante_dao.find_by_codigo(codigo_estudiante)
                if estudiante:
                    info_text += f"ESTUDIANTE:\n"
                    info_text += f"• Nombre: {estudiante.nombre} {estudiante.apellido}\n"
                    info_text += f"• Código: {estudiante.codigo}\n"
                    info_text += f"• Carrera: {estudiante.carrera}\n"
                    info_text += f"• Email: {estudiante.email}\n\n"
            
            if curso_sel:
                codigo_curso = curso_sel.split(' - ')[0]
                curso = self.curso_dao.find_by_codigo(codigo_curso)
                if curso:
                    info_text += f"CURSO:\n"
                    info_text += f"• Nombre: {curso.nombre}\n"
                    info_text += f"• Código: {curso.codigo}\n"
                    info_text += f"• Créditos: {curso.creditos}\n"
                    info_text += f"• Profesor: {curso.profesor or 'No asignado'}\n"
                    info_text += f"• Horario: {curso.horario or 'No definido'}\n"
                    info_text += f"• Cupos disponibles: {curso.cupos_disponibles}\n"
            
            if not info_text:
                info_text = "Seleccione un estudiante y un curso para ver información adicional."
            
            self.info_label.config(text=info_text)
            
        except Exception as e:
            self.info_label.config(text=f"Error: {str(e)}")
    
    def _accept(self):
        """Acepta el diálogo y valida datos"""
        try:
            if not self.estudiante_var.get() or not self.curso_var.get():
                messagebox.showerror("Error", "Debe seleccionar un estudiante y un curso")
                return
            
            # Extraer códigos
            estudiante_codigo = self.estudiante_var.get().split(' - ')[0]
            curso_codigo = self.curso_var.get().split(' - ')[0]
            
            # Confirmar matrícula
            estudiante = self.estudiante_dao.find_by_codigo(estudiante_codigo)
            curso = self.curso_dao.find_by_codigo(curso_codigo)
            
            if not estudiante or not curso:
                messagebox.showerror("Error", "Error obteniendo datos del estudiante o curso")
                return
            
            confirm_msg = f"¿Confirmar matrícula?\n\n"
            confirm_msg += f"Estudiante: {estudiante.nombre} {estudiante.apellido}\n"
            confirm_msg += f"Curso: {curso.nombre}\n"
            confirm_msg += f"Créditos: {curso.creditos}"
            
            if messagebox.askyesno("Confirmar Matrícula", confirm_msg):
                self.result = {
                    'estudiante_codigo': estudiante_codigo,
                    'curso_codigo': curso_codigo
                }
                
                self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error procesando datos: {str(e)}")
    
    def _cancel(self):
        """Cancela el diálogo"""
        self.dialog.destroy()