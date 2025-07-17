# Sistema de Matrículas Universitarias

**Autor:** Sistema de Matrículas Universitarias  
**Curso:** Teoría de los Lenguajes de Programación  
**Lenguaje:** Python 3.x  
**Año:** 2024

## 📋 Descripción del Proyecto

Sistema académico completo para la gestión de matrículas universitarias, desarrollado como proyecto para el curso de Teoría de los Lenguajes de Programación. Implementa múltiples paradigmas de programación y demuestra el uso avanzado de Python con integración de base de datos MySQL.

## 🎯 Objetivos Académicos

- **Aplicación de Paradigmas Múltiples:** Orientado a Objetos, Funcional y Lógico
- **Fundamentos de Lenguajes:** Léxico, semántica y características de Python
- **Ciencia de Datos:** Uso de pandas, numpy y matplotlib
- **Interfaz Gráfica:** Implementación con tkinter
- **Base de Datos:** Integración con MySQL usando XAMPP

## 🏗️ Arquitectura del Sistema

### Paradigmas Implementados

#### 1. Programación Orientada a Objetos
- **Clases principales:** `Estudiante`, `Curso`, `Matricula`
- **Herencia:** `Estudiante` hereda de `Persona`, DAOs heredan de `BaseDAO`
- **Encapsulación:** Propiedades privadas con getters/setters
- **Polimorfismo:** Métodos sobrescritos en clases derivadas

#### 2. Programación Funcional
- **Funciones de orden superior:** `map()`, `filter()`, `reduce()`
- **Funciones lambda:** Para filtrado y transformación de datos
- **Inmutabilidad:** Uso de copias para evitar efectos secundarios
- **Composición de funciones:** Pipeline de transformaciones de datos

#### 3. Programación Lógica
- **Predicados:** Funciones booleanas para validación
- **Reglas de negocio:** Sistema de reglas para matrículas
- **Unificación:** Verificación de prerrequisitos y restricciones

## 🛠️ Tecnologías Utilizadas

### Lenguaje Principal
- **Python 3.7+** - Lenguaje multiparadigma principal

### Base de Datos
- **MySQL** - Sistema de gestión de base de datos
- **XAMPP** - Entorno de desarrollo local
- **mysql-connector-python** - Conector Python-MySQL

### Ciencia de Datos
- **pandas** - Manipulación y análisis de datos
- **numpy** - Computación numérica
- **matplotlib** - Visualización de datos

### Interfaz de Usuario
- **tkinter** - Interfaz gráfica nativa de Python
- **Consola** - Interfaz de línea de comandos

## 📁 Estructura del Proyecto

```
sistema-matriculas/
├── config/
│   └── database.py          # Configuración de base de datos
├── models/
│   ├── estudiante.py        # Modelo de estudiante
│   ├── curso.py             # Modelo de curso
│   └── matricula.py         # Modelo de matrícula
├── dao/
│   ├── base_dao.py          # DAO base abstracto
│   ├── estudiante_dao.py    # DAO de estudiantes
│   ├── curso_dao.py         # DAO de cursos
│   └── matricula_dao.py     # DAO de matrículas
├── services/
│   └── matricula_service.py # Lógica de negocio
├── gui/
│   └── main_window.py       # Interfaz gráfica principal
├── utils/
│   ├── data_analysis.py     # Análisis de datos
│   └── language_comparison.py # Comparación de lenguajes
├── console_app.py           # Aplicación de consola
├── main.py                  # Punto de entrada principal
├── requirements.txt         # Dependencias
└── README.md               # Documentación
```

## 🚀 Instalación y Configuración

### Prerrequisitos
1. **Python 3.7 o superior**
2. **XAMPP** con MySQL activado
3. **Git** (opcional, para clonar el repositorio)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd sistema-matriculas
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar XAMPP**
   - Iniciar Apache y MySQL en XAMPP
   - Verificar que MySQL esté ejecutándose en puerto 3306

4. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

## 💻 Modos de Ejecución

### 1. Aplicación de Consola
```bash
python main.py --console
```
- Interfaz de texto completa
- Menús interactivos
- Todas las funcionalidades disponibles

### 2. Interfaz Gráfica
```bash
python main.py --gui
```
- Interfaz gráfica con tkinter
- Ventanas y formularios intuitivos
- Gestión visual de datos

### 3. Modo Mixto (Recomendado)
```bash
python main.py
```
- Inicia con consola
- Opción de abrir GUI desde menú
- Máxima flexibilidad

## 🎓 Funcionalidades Académicas

### Gestión de Estudiantes
- Registro con validación de datos
- Búsqueda por nombre/código
- Actualización de información
- Estadísticas por carrera

### Gestión de Cursos
- Creación de cursos con créditos
- Control de cupos disponibles
- Asignación de profesores y horarios
- Reportes de ocupación

### Sistema de Matrículas
- Validación de prerrequisitos
- Control de límites por estudiante
- Estados de matrícula (Activa, Cancelada, Completada)
- Reglas de negocio automatizadas

### Reportes y Análisis
- Estadísticas generales del sistema
- Análisis de datos con pandas
- Visualizaciones con matplotlib
- Exportación a CSV y Excel

### Comparación de Lenguajes
- Cuadro comparativo de lenguajes populares
- Análisis de paradigmas
- Justificación de elección de Python

## 🔧 Características Técnicas

### Paradigma Orientado a Objetos
```python
class Estudiante(Persona):
    def __init__(self, codigo, nombre, apellido, carrera):
        super().__init__(nombre, apellido)
        self._codigo = self._validar_codigo(codigo)
        self._carrera = carrera
    
    @property
    def codigo(self):
        return self._codigo
```

### Paradigma Funcional
```python
# Filtrado funcional
estudiantes_activos = list(filter(
    lambda est: est.tiene_matriculas_activas(), 
    estudiantes
))

# Transformación con map
nombres = list(map(
    lambda est: f"{est.nombre} {est.apellido}", 
    estudiantes
))
```

### Paradigma Lógico
```python
def puede_matricularse(self, estudiante, curso):
    # Regla 1: Debe haber cupos
    if not curso.tiene_cupos_disponibles():
        return False
    
    # Regla 2: No debe estar matriculado
    if self.ya_matriculado(estudiante, curso):
        return False
    
    # Regla 3: Cumplir prerrequisitos
    return self.cumple_prerrequisitos(estudiante, curso)
```

## 📊 Ciencia de Datos

### Análisis con Pandas
```python
# Crear DataFrame
df_estudiantes = pd.DataFrame(estudiantes_data)

# Análisis estadístico
stats = df_estudiantes.groupby('carrera').size()

# Filtrado avanzado
ing_sistemas = df_estudiantes[
    df_estudiantes['carrera'] == 'INGENIERIA DE SISTEMAS'
]
```

### Visualizaciones
- Gráficos de barras para distribución por carrera
- Gráficos de pastel para estados de matrícula
- Líneas de tendencia temporal

## 🗄️ Base de Datos

### Esquema de Tablas

#### Estudiantes
```sql
CREATE TABLE estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    carrera VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(15),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Cursos
```sql
CREATE TABLE cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    creditos INT NOT NULL,
    profesor VARCHAR(100),
    horario VARCHAR(50),
    cupos_disponibles INT DEFAULT 30
);
```

#### Matrículas
```sql
CREATE TABLE matriculas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT,
    curso_id INT,
    fecha_matricula TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('ACTIVA', 'CANCELADA', 'COMPLETADA') DEFAULT 'ACTIVA',
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
    FOREIGN KEY (curso_id) REFERENCES cursos(id)
);
```

## 🧪 Datos de Prueba

El sistema incluye funcionalidad para cargar datos de prueba:
- 5 estudiantes de diferentes carreras
- 5 cursos con diferentes créditos
- Matrículas de ejemplo
- Datos para testing de funcionalidades

## 📈 Reportes Disponibles

1. **Reporte General**
   - Resumen ejecutivo del sistema
   - Estadísticas por carrera y curso
   - Distribución porcentual

2. **Análisis de Datos**
   - Tendencias de matrícula
   - Estadísticas descriptivas
   - Correlaciones y patrones

3. **Exportaciones**
   - CSV para análisis externo
   - Excel con múltiples hojas
   - Reportes formateados

## 🔍 Validaciones y Reglas de Negocio

### Estudiantes
- Código único obligatorio
- Nombre y apellido requeridos
- Carrera de lista predefinida
- Email con formato válido

### Cursos
- Código único obligatorio
- Créditos entre 1 y 6
- Cupos entre 10 y 100
- Información de profesor opcional

### Matrículas
- Máximo 6 materias por estudiante
- Verificación de cupos disponibles
- Control de prerrequisitos
- Estados de transición válidos

## 🎨 Interfaz de Usuario

### Consola
- Menús jerárquicos intuitivos
- Validación de entrada en tiempo real
- Mensajes de error descriptivos
- Formateo de tablas y reportes

### GUI (tkinter)
- Ventanas con pestañas organizadas
- Formularios de entrada validados
- Tablas con ordenamiento y filtrado
- Diálogos de confirmación

## 🔧 Mantenimiento y Extensibilidad

### Patrones de Diseño
- **DAO (Data Access Object):** Separación de lógica de datos
- **MVC (Model-View-Controller):** Arquitectura organizada
- **Factory:** Creación de objetos estandarizada

### Logging y Debugging
- Sistema de logs configurado
- Manejo centralizado de errores
- Información de debugging disponible

## 📚 Aspectos Educativos

### Teoría de Lenguajes Aplicada
1. **Léxico:** Uso correcto de identificadores, palabras clave
2. **Sintaxis:** Estructura correcta de código Python
3. **Semántica:** Significado y comportamiento del código
4. **Pragmática:** Uso efectivo del lenguaje para resolver problemas

### Paradigmas Demostrados
- **Imperativo:** Control de flujo con bucles y condicionales
- **Declarativo:** Consultas SQL y expresiones funcionales
- **Orientado a Objetos:** Modelado del dominio del problema
- **Funcional:** Transformaciones de datos sin efectos secundarios

## 🚀 Posibles Extensiones

1. **Autenticación y Autorización**
   - Sistema de usuarios y roles
   - Permisos granulares

2. **Notificaciones**
   - Emails automáticos
   - Recordatorios de fechas importantes

3. **Reportes Avanzados**
   - Dashboard interactivo
   - Métricas en tiempo real

4. **API REST**
   - Servicios web para integración
   - Aplicación móvil

## 📞 Soporte y Troubleshooting

### Problemas Comunes

1. **Error de conexión a MySQL**
   - Verificar que XAMPP esté ejecutándose
   - Comprobar puerto 3306 disponible
   - Revisar credenciales de conexión

2. **Dependencias faltantes**
   - Ejecutar `pip install -r requirements.txt`
   - Verificar versión de Python

3. **Error en interfaz gráfica**
   - Verificar instalación de tkinter
   - Comprobar sistema de ventanas disponible

### Logs del Sistema
Los logs se guardan en `sistema_matriculas.log` con información detallada de:
- Operaciones de base de datos
- Errores y excepciones
- Flujo de ejecución del programa

## 🎓 Conclusiones Académicas

Este proyecto demuestra:

1. **Dominio de Python:** Uso avanzado del lenguaje y sus características
2. **Aplicación de Paradigmas:** Implementación práctica de POO, Funcional y Lógico
3. **Integración de Tecnologías:** Base de datos, GUI, ciencia de datos
4. **Buenas Prácticas:** Código limpio, documentado y mantenible
5. **Resolución de Problemas:** Análisis y diseño de sistema completo

El sistema representa una aplicación real y funcional que podría utilizarse en un entorno universitario, demostrando la aplicación práctica de los conceptos teóricos del curso.

---

**Desarrollado con ❤️ para el curso de Teoría de los Lenguajes de Programación**