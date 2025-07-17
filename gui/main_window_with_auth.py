"""
Autor: Sistema de Matrículas Universitarias
Módulo: Interfaz Gráfica Principal con Autenticación
Descripción: Ventana principal con sistema de login y roles
Paradigma: Orientado a Objetos con GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import hashlib
import logging
from typing import Optional, Tuple
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import DatabaseConfig

class LoginWindow:
    """Ventana de login para autenticación de usuarios"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title("Sistema de Matrículas - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Centrar ventana
        self.center_window()
        
        # Variables
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.usuario_logueado = None
        
        # Configurar interfaz
        self.setup_ui()
        
        # Configurar servicios
        self.setup_services()
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_services(self):
        """Configura los servicios necesarios"""
        try:
            self.db_config = DatabaseConfig()
            
            # Crear usuario administrador por defecto si no existe
            self.create_default_admin()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error configurando servicios: {str(e)}")
            
    def create_default_admin(self):
        """Crea un usuario administrador por defecto"""
        try:
            if not self.db_config.connect():
                return
                
            connection = self.db_config.get_new_connection()
            if connection is None:
                return
                
            cursor = connection.cursor()
            
            # Verificar si ya existe el admin
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", ("admin@sistema.com",))
            if cursor.fetchone():
                cursor.close()
                connection.close()
                return
            
            # Crear usuario admin
            password_hash = hashlib.sha256("admin123".encode()).hexdigest()
            
            insert_query = """
            INSERT INTO usuarios (email, password_hash, rol, nombre, apellido, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                "admin@sistema.com",
                password_hash,
                "ADMINISTRADOR",
                "Administrador",
                "Sistema",
                True
            ))
            
            connection.commit()
            cursor.close()
            connection.close()
            
        except Exception as e:
            logging.error(f"Error creando admin por defecto: {str(e)}")
            
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="🎓 Sistema de Matrículas", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Email
        ttk.Label(main_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        email_entry = ttk.Entry(main_frame, textvariable=self.email_var, width=30)
        email_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(main_frame, text="Contraseña:").grid(row=2, column=0, sticky=tk.W, pady=5)
        password_entry = ttk.Entry(main_frame, textvariable=self.password_var, 
                                  show="*", width=30)
        password_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        login_btn = ttk.Button(button_frame, text="Iniciar Sesión", 
                              command=self.login)
        login_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = ttk.Button(button_frame, text="Cancelar", 
                               command=self.root.destroy)
        cancel_btn.pack(side=tk.LEFT)
        
        # Info de credenciales
        info_label = ttk.Label(main_frame, 
                              text="Credenciales por defecto:\nAdmin: admin@sistema.com / admin123",
                              font=("Arial", 8), foreground="gray")
        info_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Configurar Enter para login
        self.root.bind('<Return>', lambda e: self.login())
        
        # Focus en email
        email_entry.focus()
        
    def login(self):
        """Procesa el login del usuario"""
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Ingrese email y contraseña")
            return
            
        try:
            # Verificar credenciales
            if not self.db_config.connect():
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
                
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo obtener conexión a la base de datos")
                return
                
            cursor = connection.cursor()
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            query = """
            SELECT id, email, rol, nombre, apellido, activo 
            FROM usuarios 
            WHERE email = %s AND password_hash = %s AND activo = TRUE
            """
            
            cursor.execute(query, (email, password_hash))
            result = cursor.fetchone()
            
            if result:
                self.usuario_logueado = {
                    'id': result[0],
                    'email': result[1],
                    'rol': result[2],
                    'nombre': result[3],
                    'apellido': result[4],
                    'activo': result[5]
                }
                
                messagebox.showinfo("Éxito", f"Bienvenido {result[3]} {result[4]}")
                self.root.destroy()
                
            else:
                messagebox.showerror("Error", "Credenciales inválidas")
                
            cursor.close()
            connection.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante login: {str(e)}")
            
    def get_usuario_logueado(self):
        """Retorna el usuario logueado"""
        return self.usuario_logueado


class MainWindowWithAuth:
    """Ventana principal del sistema con autenticación"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Matrículas Universitarias")
        self.root.geometry("800x600")
        
        # Usuario logueado
        self.usuario_logueado = None
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Configurar servicios
        self.setup_services()
        
    def setup_services(self):
        """Configura los servicios necesarios"""
        try:
            self.db_config = DatabaseConfig()
        except Exception as e:
            messagebox.showerror("Error", f"Error configurando servicios: {str(e)}")
            
    def authenticate(self) -> bool:
        """Muestra ventana de login y autentica usuario"""
        login_window = LoginWindow(self.root)
        self.root.wait_window(login_window.root)
        
        self.usuario_logueado = login_window.get_usuario_logueado()
        
        if self.usuario_logueado:
            self.setup_main_ui()
            return True
        else:
            return False
            
    def setup_main_ui(self):
        """Configura la interfaz principal después del login"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header con info del usuario
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        user_info = f"Usuario: {self.usuario_logueado['nombre']} {self.usuario_logueado['apellido']} ({self.usuario_logueado['rol']})"
        ttk.Label(header_frame, text=user_info, font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        
        logout_btn = ttk.Button(header_frame, text="Cerrar Sesión", command=self.logout)
        logout_btn.pack(side=tk.RIGHT)
        
        # Menú lateral
        menu_frame = ttk.LabelFrame(main_frame, text="Menú", padding="5")
        menu_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Contenido principal
        self.content_frame = ttk.LabelFrame(main_frame, text="Contenido", padding="10")
        self.content_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botones del menú según el rol
        if self.usuario_logueado['rol'] == 'ADMINISTRADOR':
            self.setup_admin_menu(menu_frame)
        else:
            self.setup_student_menu(menu_frame)
            
        # Contenido inicial
        welcome_label = ttk.Label(self.content_frame, 
                                 text=f"¡Bienvenido al Sistema de Matrículas!\n\nSeleccione una opción del menú lateral.",
                                 font=("Arial", 12))
        welcome_label.pack(expand=True)
        
    def setup_admin_menu(self, parent):
        """Configura el menú para administradores"""
        ttk.Button(parent, text="👥 Gestionar Estudiantes", 
                  command=self.show_students_management).pack(fill=tk.X, pady=2)
        ttk.Button(parent, text="📚 Gestionar Cursos", 
                  command=self.show_courses_management).pack(fill=tk.X, pady=2)
        ttk.Button(parent, text="📋 Ver Matrículas", 
                  command=self.show_enrollments).pack(fill=tk.X, pady=2)
        ttk.Button(parent, text="👤 Gestionar Usuarios", 
                  command=self.show_users_management).pack(fill=tk.X, pady=2)
        ttk.Button(parent, text="📊 Reportes", 
                  command=self.show_reports).pack(fill=tk.X, pady=2)
        
    def setup_student_menu(self, parent):
        """Configura el menú para estudiantes"""
        ttk.Button(parent, text="📚 Ver Cursos Disponibles", 
                  command=self.show_available_courses).pack(fill=tk.X, pady=2)
        ttk.Button(parent, text="📋 Mis Matrículas", 
                  command=self.show_my_enrollments).pack(fill=tk.X, pady=2)
        ttk.Button(parent, text="➕ Matricularme en Curso", 
                  command=self.self_enroll).pack(fill=tk.X, pady=2)
        ttk.Button(parent, text="👤 Mi Perfil", 
                  command=self.show_my_profile).pack(fill=tk.X, pady=2)
        
    def show_students_management(self):
        """Muestra la gestión de estudiantes"""
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
                    
        # Lista de estudiantes
        ttk.Label(self.content_frame, text="Gestión de Estudiantes", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame para botones
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Agregar Estudiante", 
                  command=self.add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Ver Estudiantes", 
                  command=self.list_students).pack(side=tk.LEFT, padx=5)
        
        # Área de contenido
        self.content_area = ttk.Frame(self.content_frame)
        self.content_area.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def show_courses_management(self):
        """Muestra la gestión de cursos"""
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
                    
        # Lista de cursos
        ttk.Label(self.content_frame, text="Gestión de Cursos", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame para botones
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Agregar Curso", 
                  command=self.add_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Ver Cursos", 
                  command=self.list_courses).pack(side=tk.LEFT, padx=5)
        
        # Área de contenido
        self.content_area = ttk.Frame(self.content_frame)
        self.content_area.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def show_enrollments(self):
        """Muestra las matrículas"""
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
                    
        ttk.Label(self.content_frame, text="Gestión de Matrículas", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame para botones
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Nueva Matrícula", 
                  command=self.new_enrollment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Ver Matrículas", 
                  command=self.list_enrollments).pack(side=tk.LEFT, padx=5)
        
        # Área de contenido
        self.content_area = ttk.Frame(self.content_frame)
        self.content_area.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def show_users_management(self):
        """Muestra la gestión de usuarios"""
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
                    
        ttk.Label(self.content_frame, text="Gestión de Usuarios", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame para botones
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Crear Usuario", 
                  command=self.create_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Ver Usuarios", 
                  command=self.list_users).pack(side=tk.LEFT, padx=5)
        
        # Área de contenido
        self.content_area = ttk.Frame(self.content_frame)
        self.content_area.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def show_reports(self):
        """Muestra los reportes"""
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
                    
        ttk.Label(self.content_frame, text="Reportes del Sistema", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Frame para botones
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Reporte de Estudiantes", 
                  command=self.student_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reporte de Cursos", 
                  command=self.course_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reporte de Matrículas", 
                  command=self.enrollment_report).pack(side=tk.LEFT, padx=5)
        
        # Área de contenido
        self.content_area = ttk.Frame(self.content_frame)
        self.content_area.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def show_available_courses(self):
        """Muestra cursos disponibles para estudiantes"""
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
                    
        ttk.Label(self.content_frame, text="Cursos Disponibles", font=("Arial", 14, "bold")).pack(pady=10)
        
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
                
            cursor = connection.cursor()
            cursor.execute("SELECT codigo, nombre, creditos, profesor, cupos_disponibles FROM cursos")
            courses = cursor.fetchall()
            
            # Crear tabla
            tree = ttk.Treeview(self.content_frame, columns=('Código', 'Nombre', 'Créditos', 'Profesor', 'Cupos'), show='headings')
            tree.heading('#1', text='Código')
            tree.heading('#2', text='Nombre')
            tree.heading('#3', text='Créditos')
            tree.heading('#4', text='Profesor')
            tree.heading('#5', text='Cupos')
            
            for course in courses:
                tree.insert('', 'end', values=course)
            
            tree.pack(fill=tk.BOTH, expand=True, pady=10)
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar cursos: {str(e)}")
        
    def show_my_enrollments(self):
        """Muestra las matrículas del estudiante"""
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
                    
        ttk.Label(self.content_frame, text="Mis Matrículas", font=("Arial", 14, "bold")).pack(pady=10)
        
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
            
            cursor = connection.cursor()
            
            # Obtener matrículas del estudiante logueado
            query = """SELECT m.id, c.codigo, c.nombre, c.creditos, m.fecha_matricula, m.estado 
                      FROM matriculas m 
                      JOIN cursos c ON m.curso_id = c.id 
                      JOIN estudiantes e ON m.estudiante_id = e.id 
                      JOIN usuarios u ON e.email = u.email 
                      WHERE u.id = %s"""
            
            cursor.execute(query, (self.usuario_logueado['id'],))
            enrollments = cursor.fetchall()
            
            if not enrollments:
                ttk.Label(self.content_frame, text="No tienes matrículas registradas", 
                         font=("Arial", 12)).pack(pady=20)
            else:
                # Frame para botones
                btn_frame = ttk.Frame(self.content_frame)
                btn_frame.pack(pady=10)
                
                # Crear tabla
                tree = ttk.Treeview(self.content_frame, columns=('ID', 'Código', 'Curso', 'Créditos', 'Fecha', 'Estado'), show='headings')
                tree.heading('#1', text='ID')
                tree.heading('#2', text='Código')
                tree.heading('#3', text='Curso')
                tree.heading('#4', text='Créditos')
                tree.heading('#5', text='Fecha')
                tree.heading('#6', text='Estado')
                
                tree.column('#1', width=50)
                tree.column('#2', width=80)
                tree.column('#3', width=200)
                tree.column('#4', width=80)
                tree.column('#5', width=120)
                tree.column('#6', width=100)
                
                for enrollment in enrollments:
                    tree.insert('', 'end', values=enrollment)
                
                tree.pack(fill=tk.BOTH, expand=True, pady=10)
                
                def cancel_enrollment():
                    try:
                        selected = tree.selection()
                        if not selected:
                            messagebox.showwarning("Advertencia", "Seleccione una matrícula para cancelar")
                            return
                        
                        item = tree.item(selected[0])
                        matricula_id = item['values'][0]
                        curso_nombre = item['values'][2]
                        
                        if messagebox.askyesno("Confirmar", f"¿Está seguro que desea cancelar la matrícula en {curso_nombre}?"):
                            cursor = connection.cursor()
                            cursor.execute("UPDATE matriculas SET estado = 'CANCELADA' WHERE id = %s", (matricula_id,))
                            connection.commit()
                            cursor.close()
                            
                            messagebox.showinfo("Éxito", "Matrícula cancelada correctamente")
                            self.show_my_enrollments()  # Refrescar
                    
                    except Exception as e:
                        messagebox.showerror("Error", f"Error al cancelar matrícula: {str(e)}")
                
                ttk.Button(btn_frame, text="Cancelar Matrícula Seleccionada", 
                          command=cancel_enrollment).pack(side=tk.LEFT, padx=5)
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar matrículas: {str(e)}")
        
    def show_my_profile(self):
        """Muestra el perfil del estudiante"""
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
                    
        ttk.Label(self.content_frame, text="Mi Perfil", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Mostrar información del usuario
        info_frame = ttk.LabelFrame(self.content_frame, text="Información Personal", padding="10")
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(info_frame, text=f"Nombre: {self.usuario_logueado['nombre']} {self.usuario_logueado['apellido']}", 
                 font=("Arial", 11)).pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Email: {self.usuario_logueado['email']}", 
                 font=("Arial", 11)).pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"Rol: {self.usuario_logueado['rol']}", 
                 font=("Arial", 11)).pack(anchor=tk.W, pady=2)
        
        # Si es estudiante, mostrar código
        if self.usuario_logueado['rol'] == 'ESTUDIANTE':
            try:
                connection = self.db_config.get_new_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT codigo_estudiante FROM usuarios WHERE id = %s", (self.usuario_logueado['id'],))
                result = cursor.fetchone()
                if result and result[0]:
                    ttk.Label(info_frame, text=f"Código de Estudiante: {result[0]}", 
                             font=("Arial", 11)).pack(anchor=tk.W, pady=2)
                cursor.close()
                connection.close()
            except Exception as e:
                pass
    
    def self_enroll(self):
        """Permite al estudiante matricularse en un curso"""
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
            
            cursor = connection.cursor()
            
            # Obtener cursos disponibles (no matriculados por este estudiante)
            query = """SELECT c.id, c.codigo, c.nombre, c.creditos, c.profesor 
                      FROM cursos c 
                      WHERE c.id NOT IN (
                          SELECT m.curso_id 
                          FROM matriculas m 
                          JOIN estudiantes e ON m.estudiante_id = e.id 
                          JOIN usuarios u ON e.email = u.email 
                          WHERE u.id = %s AND m.estado = 'ACTIVA'
                      )"""
            
            cursor.execute(query, (self.usuario_logueado['id'],))
            cursos_disponibles = cursor.fetchall()
            
            if not cursos_disponibles:
                messagebox.showinfo("Información", "No hay cursos disponibles para matrícula")
                cursor.close()
                connection.close()
                return
            
            # Ventana para auto-matrícula
            enroll_window = tk.Toplevel(self.root)
            enroll_window.title("Matricularme en Curso")
            enroll_window.geometry("600x400")
            
            ttk.Label(enroll_window, text="Seleccione un curso para matricularse:", 
                     font=("Arial", 12, "bold")).pack(pady=10)
            
            # Lista de cursos disponibles
            curso_frame = ttk.Frame(enroll_window)
            curso_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            tree = ttk.Treeview(curso_frame, columns=('Código', 'Nombre', 'Créditos', 'Profesor'), show='headings')
            tree.heading('#1', text='Código')
            tree.heading('#2', text='Nombre')
            tree.heading('#3', text='Créditos')
            tree.heading('#4', text='Profesor')
            
            tree.column('#1', width=100)
            tree.column('#2', width=250)
            tree.column('#3', width=80)
            tree.column('#4', width=150)
            
            for curso in cursos_disponibles:
                tree.insert('', 'end', values=curso[1:])  # Omitir el ID
            
            tree.pack(fill=tk.BOTH, expand=True)
            
            def matricular():
                try:
                    selected = tree.selection()
                    if not selected:
                        messagebox.showwarning("Advertencia", "Seleccione un curso")
                        return
                    
                    # Obtener el curso seleccionado
                    item_index = tree.index(selected[0])
                    curso_seleccionado = cursos_disponibles[item_index]
                    curso_id = curso_seleccionado[0]
                    curso_nombre = curso_seleccionado[2]
                    
                    if messagebox.askyesno("Confirmar", f"¿Desea matricularse en {curso_nombre}?"):
                        # Obtener el estudiante_id
                        cursor.execute("""SELECT e.id FROM estudiantes e 
                                         JOIN usuarios u ON e.email = u.email 
                                         WHERE u.id = %s""", (self.usuario_logueado['id'],))
                        estudiante_result = cursor.fetchone()
                        
                        if not estudiante_result:
                            messagebox.showerror("Error", "No se encontró el registro de estudiante")
                            return
                        
                        estudiante_id = estudiante_result[0]
                        
                        # Insertar matrícula
                        cursor.execute("INSERT INTO matriculas (estudiante_id, curso_id, estado) VALUES (%s, %s, 'ACTIVA')", 
                                     (estudiante_id, curso_id))
                        connection.commit()
                        
                        messagebox.showinfo("Éxito", f"¡Te has matriculado exitosamente en {curso_nombre}!")
                        enroll_window.destroy()
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Error al matricularse: {str(e)}")
            
            ttk.Button(enroll_window, text="Matricularme", command=matricular).pack(pady=20)
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def logout(self):
        """Cierra sesión del usuario"""
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea cerrar sesión?"):
            self.usuario_logueado = None
            self.root.destroy()
    
    # Funciones de gestión de estudiantes
    def add_student(self):
        """Agregar nuevo estudiante"""
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
                
            # Ventana para agregar estudiante
            add_window = tk.Toplevel(self.root)
            add_window.title("Agregar Estudiante")
            add_window.geometry("400x300")
            
            # Campos
            ttk.Label(add_window, text="Código:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
            codigo_var = tk.StringVar()
            ttk.Entry(add_window, textvariable=codigo_var).grid(row=0, column=1, padx=10, pady=5)
            
            ttk.Label(add_window, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
            nombre_var = tk.StringVar()
            ttk.Entry(add_window, textvariable=nombre_var).grid(row=1, column=1, padx=10, pady=5)
            
            ttk.Label(add_window, text="Apellido:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
            apellido_var = tk.StringVar()
            ttk.Entry(add_window, textvariable=apellido_var).grid(row=2, column=1, padx=10, pady=5)
            
            ttk.Label(add_window, text="Carrera:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
            carrera_var = tk.StringVar()
            ttk.Entry(add_window, textvariable=carrera_var).grid(row=3, column=1, padx=10, pady=5)
            
            ttk.Label(add_window, text="Email:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
            email_var = tk.StringVar()
            ttk.Entry(add_window, textvariable=email_var).grid(row=4, column=1, padx=10, pady=5)
            
            def save_student():
                try:
                    cursor = connection.cursor()
                    query = """INSERT INTO estudiantes (codigo, nombre, apellido, carrera, email) 
                              VALUES (%s, %s, %s, %s, %s)"""
                    cursor.execute(query, (codigo_var.get(), nombre_var.get(), apellido_var.get(), 
                                         carrera_var.get(), email_var.get()))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    messagebox.showinfo("Éxito", "Estudiante agregado correctamente")
                    add_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al agregar estudiante: {str(e)}")
            
            ttk.Button(add_window, text="Guardar", command=save_student).grid(row=5, column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def list_students(self):
        """Listar estudiantes"""
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
                
            cursor = connection.cursor()
            cursor.execute("SELECT codigo, nombre, apellido, carrera, email FROM estudiantes")
            students = cursor.fetchall()
            
            # Limpiar área de contenido
            for widget in self.content_area.winfo_children():
                widget.destroy()
            
            # Crear tabla
            tree = ttk.Treeview(self.content_area, columns=('Código', 'Nombre', 'Apellido', 'Carrera', 'Email'), show='headings')
            tree.heading('#1', text='Código')
            tree.heading('#2', text='Nombre')
            tree.heading('#3', text='Apellido')
            tree.heading('#4', text='Carrera')
            tree.heading('#5', text='Email')
            
            for student in students:
                tree.insert('', 'end', values=student)
            
            tree.pack(fill=tk.BOTH, expand=True)
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al listar estudiantes: {str(e)}")
    
    # Funciones de gestión de cursos
    def add_course(self):
        """Agregar nuevo curso"""
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
                
            # Ventana para agregar curso
            add_window = tk.Toplevel(self.root)
            add_window.title("Agregar Curso")
            add_window.geometry("400x250")
            
            # Campos
            ttk.Label(add_window, text="Código:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
            codigo_var = tk.StringVar()
            ttk.Entry(add_window, textvariable=codigo_var).grid(row=0, column=1, padx=10, pady=5)
            
            ttk.Label(add_window, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
            nombre_var = tk.StringVar()
            ttk.Entry(add_window, textvariable=nombre_var).grid(row=1, column=1, padx=10, pady=5)
            
            ttk.Label(add_window, text="Créditos:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
            creditos_var = tk.StringVar()
            ttk.Entry(add_window, textvariable=creditos_var).grid(row=2, column=1, padx=10, pady=5)
            
            ttk.Label(add_window, text="Profesor:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
            profesor_var = tk.StringVar()
            ttk.Entry(add_window, textvariable=profesor_var).grid(row=3, column=1, padx=10, pady=5)
            
            def save_course():
                try:
                    cursor = connection.cursor()
                    query = """INSERT INTO cursos (codigo, nombre, creditos, profesor) 
                              VALUES (%s, %s, %s, %s)"""
                    cursor.execute(query, (codigo_var.get(), nombre_var.get(), 
                                         int(creditos_var.get()), profesor_var.get()))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    messagebox.showinfo("Éxito", "Curso agregado correctamente")
                    add_window.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al agregar curso: {str(e)}")
            
            ttk.Button(add_window, text="Guardar", command=save_course).grid(row=4, column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def list_courses(self):
        """Listar cursos"""
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
                
            cursor = connection.cursor()
            cursor.execute("SELECT codigo, nombre, creditos, profesor FROM cursos")
            courses = cursor.fetchall()
            
            # Limpiar área de contenido
            for widget in self.content_area.winfo_children():
                widget.destroy()
            
            # Crear tabla
            tree = ttk.Treeview(self.content_area, columns=('Código', 'Nombre', 'Créditos', 'Profesor'), show='headings')
            tree.heading('#1', text='Código')
            tree.heading('#2', text='Nombre')
            tree.heading('#3', text='Créditos')
            tree.heading('#4', text='Profesor')
            
            for course in courses:
                tree.insert('', 'end', values=course)
            
            tree.pack(fill=tk.BOTH, expand=True)
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al listar cursos: {str(e)}")
    
    # Funciones de matrículas
    def new_enrollment(self):
        """Nueva matrícula"""
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
            
            cursor = connection.cursor()
            
            # Obtener estudiantes
            cursor.execute("SELECT id, codigo, nombre, apellido FROM estudiantes")
            estudiantes = cursor.fetchall()
            
            # Obtener cursos
            cursor.execute("SELECT id, codigo, nombre FROM cursos")
            cursos = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            if not estudiantes:
                messagebox.showwarning("Advertencia", "No hay estudiantes registrados")
                return
            
            if not cursos:
                messagebox.showwarning("Advertencia", "No hay cursos registrados")
                return
            
            # Ventana para nueva matrícula
            enroll_window = tk.Toplevel(self.root)
            enroll_window.title("Nueva Matrícula")
            enroll_window.geometry("500x300")
            
            # Variables
            estudiante_var = tk.StringVar()
            curso_var = tk.StringVar()
            
            # Campos
            ttk.Label(enroll_window, text="Estudiante:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
            
            # Lista de estudiantes
            estudiante_frame = ttk.Frame(enroll_window)
            estudiante_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=(tk.W, tk.E))
            
            estudiante_list = tk.Listbox(estudiante_frame, height=5)
            estudiante_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar1 = ttk.Scrollbar(estudiante_frame, orient=tk.VERTICAL, command=estudiante_list.yview)
            scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
            estudiante_list.config(yscrollcommand=scrollbar1.set)
            
            for est in estudiantes:
                estudiante_list.insert(tk.END, f"{est[1]} - {est[2]} {est[3]}")
            
            ttk.Label(enroll_window, text="Curso:", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
            
            # Lista de cursos
            curso_frame = ttk.Frame(enroll_window)
            curso_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=(tk.W, tk.E))
            
            curso_list = tk.Listbox(curso_frame, height=5)
            curso_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar2 = ttk.Scrollbar(curso_frame, orient=tk.VERTICAL, command=curso_list.yview)
            scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
            curso_list.config(yscrollcommand=scrollbar2.set)
            
            for curso in cursos:
                curso_list.insert(tk.END, f"{curso[1]} - {curso[2]}")
            
            def matricular():
                try:
                    est_sel = estudiante_list.curselection()
                    curso_sel = curso_list.curselection()
                    
                    if not est_sel:
                        messagebox.showerror("Error", "Seleccione un estudiante")
                        return
                    
                    if not curso_sel:
                        messagebox.showerror("Error", "Seleccione un curso")
                        return
                    
                    estudiante_id = estudiantes[est_sel[0]][0]
                    curso_id = cursos[curso_sel[0]][0]
                    
                    connection = self.db_config.get_new_connection()
                    cursor = connection.cursor()
                    
                    # Verificar si ya está matriculado
                    cursor.execute("SELECT id FROM matriculas WHERE estudiante_id = %s AND curso_id = %s", 
                                 (estudiante_id, curso_id))
                    if cursor.fetchone():
                        messagebox.showwarning("Advertencia", "El estudiante ya está matriculado en este curso")
                        cursor.close()
                        connection.close()
                        return
                    
                    # Insertar matrícula
                    query = "INSERT INTO matriculas (estudiante_id, curso_id, estado) VALUES (%s, %s, 'ACTIVA')"
                    cursor.execute(query, (estudiante_id, curso_id))
                    
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Éxito", "Matrícula realizada correctamente")
                    enroll_window.destroy()
                    self.list_enrollments()  # Refrescar lista
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error al matricular: {str(e)}")
            
            ttk.Button(enroll_window, text="Matricular", command=matricular).grid(row=4, column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def list_enrollments(self):
        """Listar matrículas"""
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
                
            cursor = connection.cursor()
            query = """SELECT e.codigo, e.nombre, c.codigo, c.nombre, m.fecha_matricula, m.estado 
                      FROM matriculas m 
                      JOIN estudiantes e ON m.estudiante_id = e.id 
                      JOIN cursos c ON m.curso_id = c.id"""
            cursor.execute(query)
            enrollments = cursor.fetchall()
            
            # Limpiar área de contenido
            for widget in self.content_area.winfo_children():
                widget.destroy()
            
            # Crear tabla
            tree = ttk.Treeview(self.content_area, columns=('Cód. Est.', 'Estudiante', 'Cód. Curso', 'Curso', 'Fecha', 'Estado'), show='headings')
            tree.heading('#1', text='Cód. Est.')
            tree.heading('#2', text='Estudiante')
            tree.heading('#3', text='Cód. Curso')
            tree.heading('#4', text='Curso')
            tree.heading('#5', text='Fecha')
            tree.heading('#6', text='Estado')
            
            for enrollment in enrollments:
                tree.insert('', 'end', values=enrollment)
            
            tree.pack(fill=tk.BOTH, expand=True)
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al listar matrículas: {str(e)}")
    
    # Funciones de usuarios
    def create_user(self):
        """Crear nuevo usuario"""
        try:
            # Ventana para crear usuario
            create_window = tk.Toplevel(self.root)
            create_window.title("Crear Usuario")
            create_window.geometry("500x400")
            
            # Variables
            email_var = tk.StringVar()
            password_var = tk.StringVar()
            nombre_var = tk.StringVar()
            apellido_var = tk.StringVar()
            rol_var = tk.StringVar(value="ESTUDIANTE")
            codigo_var = tk.StringVar()
            
            # Campos
            row = 0
            ttk.Label(create_window, text="Email:").grid(row=row, column=0, padx=10, pady=5, sticky=tk.W)
            ttk.Entry(create_window, textvariable=email_var, width=30).grid(row=row, column=1, padx=10, pady=5)
            
            row += 1
            ttk.Label(create_window, text="Contraseña:").grid(row=row, column=0, padx=10, pady=5, sticky=tk.W)
            ttk.Entry(create_window, textvariable=password_var, show="*", width=30).grid(row=row, column=1, padx=10, pady=5)
            
            row += 1
            ttk.Label(create_window, text="Nombre:").grid(row=row, column=0, padx=10, pady=5, sticky=tk.W)
            ttk.Entry(create_window, textvariable=nombre_var, width=30).grid(row=row, column=1, padx=10, pady=5)
            
            row += 1
            ttk.Label(create_window, text="Apellido:").grid(row=row, column=0, padx=10, pady=5, sticky=tk.W)
            ttk.Entry(create_window, textvariable=apellido_var, width=30).grid(row=row, column=1, padx=10, pady=5)
            
            row += 1
            ttk.Label(create_window, text="Rol:").grid(row=row, column=0, padx=10, pady=5, sticky=tk.W)
            rol_combo = ttk.Combobox(create_window, textvariable=rol_var, values=["ADMINISTRADOR", "ESTUDIANTE"], 
                                   state="readonly", width=27)
            rol_combo.grid(row=row, column=1, padx=10, pady=5)
            
            row += 1
            ttk.Label(create_window, text="Código Estudiante:").grid(row=row, column=0, padx=10, pady=5, sticky=tk.W)
            codigo_entry = ttk.Entry(create_window, textvariable=codigo_var, width=30)
            codigo_entry.grid(row=row, column=1, padx=10, pady=5)
            
            # Función para habilitar/deshabilitar código según rol
            def on_rol_change(*args):
                if rol_var.get() == "ESTUDIANTE":
                    codigo_entry.config(state="normal")
                else:
                    codigo_entry.config(state="disabled")
                    codigo_var.set("")
            
            rol_var.trace('w', on_rol_change)
            
            def save_user():
                try:
                    if not all([email_var.get(), password_var.get(), nombre_var.get(), apellido_var.get()]):
                        messagebox.showerror("Error", "Todos los campos son obligatorios")
                        return
                    
                    if rol_var.get() == "ESTUDIANTE" and not codigo_var.get():
                        messagebox.showerror("Error", "El código de estudiante es obligatorio")
                        return
                    
                    connection = self.db_config.get_new_connection()
                    if connection is None:
                        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                        return
                    
                    cursor = connection.cursor()
                    
                    # Hash de la contraseña
                    password_hash = hashlib.sha256(password_var.get().encode()).hexdigest()
                    
                    # Insertar usuario
                    query = """INSERT INTO usuarios (email, password_hash, rol, nombre, apellido, codigo_estudiante, activo) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    
                    cursor.execute(query, (
                        email_var.get(),
                        password_hash,
                        rol_var.get(),
                        nombre_var.get(),
                        apellido_var.get(),
                        codigo_var.get() if rol_var.get() == "ESTUDIANTE" else None,
                        True
                    ))
                    
                    # Si es estudiante, también agregarlo a la tabla estudiantes
                    if rol_var.get() == "ESTUDIANTE":
                        query_est = """INSERT INTO estudiantes (codigo, nombre, apellido, email) 
                                      VALUES (%s, %s, %s, %s)"""
                        cursor.execute(query_est, (
                            codigo_var.get(),
                            nombre_var.get(),
                            apellido_var.get(),
                            email_var.get()
                        ))
                    
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Éxito", "Usuario creado correctamente")
                    create_window.destroy()
                    self.list_users()  # Refrescar lista
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error al crear usuario: {str(e)}")
            
            row += 2
            ttk.Button(create_window, text="Guardar", command=save_user).grid(row=row, column=0, columnspan=2, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def list_users(self):
        """Listar usuarios"""
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
                
            cursor = connection.cursor()
            cursor.execute("SELECT email, rol, nombre, apellido, activo FROM usuarios")
            users = cursor.fetchall()
            
            # Limpiar área de contenido
            for widget in self.content_area.winfo_children():
                widget.destroy()
            
            # Crear tabla
            tree = ttk.Treeview(self.content_area, columns=('Email', 'Rol', 'Nombre', 'Apellido', 'Activo'), show='headings')
            tree.heading('#1', text='Email')
            tree.heading('#2', text='Rol')
            tree.heading('#3', text='Nombre')
            tree.heading('#4', text='Apellido')
            tree.heading('#5', text='Activo')
            
            for user in users:
                tree.insert('', 'end', values=user)
            
            tree.pack(fill=tk.BOTH, expand=True)
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al listar usuarios: {str(e)}")
    
    # Funciones de reportes
    def student_report(self):
        """Reporte de estudiantes"""
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
                
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM estudiantes")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT carrera, COUNT(*) FROM estudiantes GROUP BY carrera")
            by_career = cursor.fetchall()
            
            # Limpiar área de contenido
            for widget in self.content_area.winfo_children():
                widget.destroy()
            
            ttk.Label(self.content_area, text=f"Total de estudiantes: {total}", font=("Arial", 12, "bold")).pack(pady=10)
            
            ttk.Label(self.content_area, text="Estudiantes por carrera:", font=("Arial", 10, "bold")).pack(pady=5)
            for career, count in by_career:
                ttk.Label(self.content_area, text=f"• {career}: {count}").pack()
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def course_report(self):
        """Reporte de cursos"""
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
                
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM cursos")
            total = cursor.fetchone()[0]
            
            # Limpiar área de contenido
            for widget in self.content_area.winfo_children():
                widget.destroy()
            
            ttk.Label(self.content_area, text=f"Total de cursos: {total}", font=("Arial", 12, "bold")).pack(pady=10)
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def enrollment_report(self):
        """Reporte de matrículas"""
        try:
            connection = self.db_config.get_new_connection()
            if connection is None:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                return
                
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM matriculas")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT estado, COUNT(*) FROM matriculas GROUP BY estado")
            by_status = cursor.fetchall()
            
            # Limpiar área de contenido
            for widget in self.content_area.winfo_children():
                widget.destroy()
            
            ttk.Label(self.content_area, text=f"Total de matrículas: {total}", font=("Arial", 12, "bold")).pack(pady=10)
            
            ttk.Label(self.content_area, text="Matrículas por estado:", font=("Arial", 10, "bold")).pack(pady=5)
            for status, count in by_status:
                ttk.Label(self.content_area, text=f"• {status}: {count}").pack()
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def run(self):
        """Ejecuta la aplicación"""
        try:
            # Primero autenticar
            if self.authenticate():
                # Si la autenticación fue exitosa, ejecutar interfaz principal
                self.root.mainloop()
            else:
                # Si no se autenticó, cerrar aplicación
                self.root.destroy()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error ejecutando aplicación: {str(e)}")
            self.logger.error(f"Error ejecutando aplicación: {str(e)}")


if __name__ == "__main__":
    app = MainWindowWithAuth()
    app.run()
