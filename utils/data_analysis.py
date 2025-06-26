"""
Autor: Sistema de Matrículas Universitarias
Módulo: Análisis de Datos
Descripción: Funciones para análisis de datos usando pandas y numpy
Paradigma: Funcional con ciencia de datos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any
import logging
from datetime import datetime, timedelta

class DataAnalyzer:
    """
    Clase para análisis de datos del sistema de matrículas
    Uso de pandas y numpy para ciencia de datos básica
    """
    
    def __init__(self):
        """Constructor del analizador de datos"""
        self.logger = logging.getLogger(__name__)
        
        # Configurar matplotlib para español
        plt.rcParams['font.size'] = 10
        plt.rcParams['figure.figsize'] = (10, 6)
    
    def create_students_dataframe(self, estudiantes_data: List[Dict]) -> pd.DataFrame:
        """
        Crea un DataFrame de pandas con datos de estudiantes
        Aplicación de ciencia de datos con pandas
        """
        try:
            if not estudiantes_data:
                return pd.DataFrame()
            
            df = pd.DataFrame(estudiantes_data)
            
            # Limpiar y procesar datos
            if 'fecha_registro' in df.columns:
                df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])
            
            # Agregar columnas calculadas
            if 'nombre' in df.columns and 'apellido' in df.columns:
                df['nombre_completo'] = df['nombre'] + ' ' + df['apellido']
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error creando DataFrame de estudiantes: {e}")
            return pd.DataFrame()
    
    def create_courses_dataframe(self, cursos_data: List[Dict]) -> pd.DataFrame:
        """Crea un DataFrame de pandas con datos de cursos"""
        try:
            if not cursos_data:
                return pd.DataFrame()
            
            df = pd.DataFrame(cursos_data)
            
            # Calcular métricas adicionales
            if 'cupos_disponibles' in df.columns and 'cupos_ocupados' in df.columns:
                df['porcentaje_ocupacion'] = (df['cupos_ocupados'] / 
                                             (df['cupos_disponibles'] + df['cupos_ocupados']) * 100).round(2)
                df['cupos_libres'] = df['cupos_disponibles']
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error creando DataFrame de cursos: {e}")
            return pd.DataFrame()
    
    def create_enrollments_dataframe(self, matriculas_data: List[Dict]) -> pd.DataFrame:
        """Crea un DataFrame de pandas con datos de matrículas"""
        try:
            if not matriculas_data:
                return pd.DataFrame()
            
            df = pd.DataFrame(matriculas_data)
            
            # Procesar fechas
            if 'fecha_matricula' in df.columns:
                df['fecha_matricula'] = pd.to_datetime(df['fecha_matricula'])
                df['mes_matricula'] = df['fecha_matricula'].dt.month
                df['año_matricula'] = df['fecha_matricula'].dt.year
                df['dia_semana'] = df['fecha_matricula'].dt.day_name()
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error creando DataFrame de matrículas: {e}")
            return pd.DataFrame()
    
    def analyze_enrollment_trends(self, df_matriculas: pd.DataFrame) -> Dict[str, Any]:
        """
        Analiza tendencias de matrícula usando pandas
        Programación funcional con operaciones de agregación
        """
        try:
            if df_matriculas.empty:
                return {}
            
            analysis = {}
            
            # Análisis temporal
            if 'fecha_matricula' in df_matriculas.columns:
                # Matrículas por mes
                monthly_enrollments = df_matriculas.groupby('mes_matricula').size()
                analysis['matriculas_por_mes'] = monthly_enrollments.to_dict()
                
                # Matrículas por día de la semana
                weekly_enrollments = df_matriculas.groupby('dia_semana').size()
                analysis['matriculas_por_dia'] = weekly_enrollments.to_dict()
            
            # Análisis por estado
            if 'estado' in df_matriculas.columns:
                status_distribution = df_matriculas['estado'].value_counts()
                analysis['distribucion_estados'] = status_distribution.to_dict()
            
            # Análisis por carrera (si está disponible)
            if 'carrera' in df_matriculas.columns:
                career_enrollments = df_matriculas['carrera'].value_counts()
                analysis['matriculas_por_carrera'] = career_enrollments.to_dict()
            
            # Estadísticas descriptivas
            analysis['total_matriculas'] = len(df_matriculas)
            analysis['fecha_primera_matricula'] = df_matriculas['fecha_matricula'].min() if 'fecha_matricula' in df_matriculas.columns else None
            analysis['fecha_ultima_matricula'] = df_matriculas['fecha_matricula'].max() if 'fecha_matricula' in df_matriculas.columns else None
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analizando tendencias: {e}")
            return {}
    
    def calculate_course_statistics(self, df_cursos: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcula estadísticas de cursos usando numpy
        Aplicación de funciones matemáticas y estadísticas
        """
        try:
            if df_cursos.empty:
                return {}
            
            stats = {}
            
            # Estadísticas de créditos
            if 'creditos' in df_cursos.columns:
                creditos = df_cursos['creditos'].values
                stats['creditos'] = {
                    'promedio': np.mean(creditos).round(2),
                    'mediana': np.median(creditos),
                    'moda': float(np.bincount(creditos).argmax()),
                    'desviacion_estandar': np.std(creditos).round(2),
                    'minimo': np.min(creditos),
                    'maximo': np.max(creditos)
                }
            
            # Estadísticas de ocupación
            if 'porcentaje_ocupacion' in df_cursos.columns:
                ocupacion = df_cursos['porcentaje_ocupacion'].values
                ocupacion = ocupacion[~np.isnan(ocupacion)]  # Remover NaN
                
                if len(ocupacion) > 0:
                    stats['ocupacion'] = {
                        'promedio': np.mean(ocupacion).round(2),
                        'mediana': np.median(ocupacion).round(2),
                        'desviacion_estandar': np.std(ocupacion).round(2),
                        'minimo': np.min(ocupacion).round(2),
                        'maximo': np.max(ocupacion).round(2)
                    }
            
            # Distribución por créditos
            if 'creditos' in df_cursos.columns:
                credit_distribution = df_cursos['creditos'].value_counts().sort_index()
                stats['distribucion_creditos'] = credit_distribution.to_dict()
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error calculando estadísticas de cursos: {e}")
            return {}
    
    def generate_enrollment_report(self, df_matriculas: pd.DataFrame, 
                                 df_estudiantes: pd.DataFrame, 
                                 df_cursos: pd.DataFrame) -> str:
        """
        Genera un reporte completo usando pandas
        Combinación de DataFrames con merge y análisis
        """
        try:
            report = "=== REPORTE DE ANÁLISIS DE DATOS ===\n\n"
            
            # Información general
            report += f"Total de estudiantes: {len(df_estudiantes)}\n"
            report += f"Total de cursos: {len(df_cursos)}\n"
            report += f"Total de matrículas: {len(df_matriculas)}\n\n"
            
            # Análisis de estudiantes por carrera
            if not df_estudiantes.empty and 'carrera' in df_estudiantes.columns:
                career_counts = df_estudiantes['carrera'].value_counts()
                report += "ESTUDIANTES POR CARRERA:\n"
                for carrera, count in career_counts.items():
                    percentage = (count / len(df_estudiantes) * 100).round(1)
                    report += f"- {carrera}: {count} ({percentage}%)\n"
                report += "\n"
            
            # Análisis de cursos por créditos
            if not df_cursos.empty and 'creditos' in df_cursos.columns:
                credit_stats = self.calculate_course_statistics(df_cursos)
                if 'creditos' in credit_stats:
                    report += "ESTADÍSTICAS DE CRÉDITOS:\n"
                    cred_stats = credit_stats['creditos']
                    report += f"- Promedio: {cred_stats['promedio']} créditos\n"
                    report += f"- Mediana: {cred_stats['mediana']} créditos\n"
                    report += f"- Rango: {cred_stats['minimo']} - {cred_stats['maximo']} créditos\n\n"
            
            # Análisis de tendencias de matrícula
            if not df_matriculas.empty:
                trends = self.analyze_enrollment_trends(df_matriculas)
                
                if 'distribucion_estados' in trends:
                    report += "DISTRIBUCIÓN POR ESTADO DE MATRÍCULA:\n"
                    for estado, count in trends['distribucion_estados'].items():
                        percentage = (count / trends['total_matriculas'] * 100).round(1)
                        report += f"- {estado}: {count} ({percentage}%)\n"
                    report += "\n"
                
                if 'matriculas_por_mes' in trends:
                    report += "MATRÍCULAS POR MES:\n"
                    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
                    for mes_num, count in trends['matriculas_por_mes'].items():
                        mes_nombre = meses[mes_num - 1]
                        report += f"- {mes_nombre}: {count} matrículas\n"
                    report += "\n"
            
            # Recomendaciones basadas en datos
            report += "RECOMENDACIONES BASADAS EN ANÁLISIS:\n"
            
            # Análisis de ocupación de cursos
            if not df_cursos.empty and 'porcentaje_ocupacion' in df_cursos.columns:
                high_demand = df_cursos[df_cursos['porcentaje_ocupacion'] > 80]
                low_demand = df_cursos[df_cursos['porcentaje_ocupacion'] < 30]
                
                if not high_demand.empty:
                    report += f"- {len(high_demand)} cursos tienen alta demanda (>80% ocupación)\n"
                    report += "  Considerar aumentar cupos o abrir nuevas secciones\n"
                
                if not low_demand.empty:
                    report += f"- {len(low_demand)} cursos tienen baja demanda (<30% ocupación)\n"
                    report += "  Revisar contenido, horarios o estrategias de promoción\n"
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generando reporte: {e}")
            return f"Error generando reporte: {str(e)}"
    
    def create_visualization(self, df_data: pd.DataFrame, chart_type: str, 
                           title: str, filename: str = None) -> bool:
        """
        Crea visualizaciones usando matplotlib
        Aplicación de ciencia de datos para visualización
        """
        try:
            plt.figure(figsize=(10, 6))
            
            if chart_type == 'bar' and not df_data.empty:
                # Gráfico de barras
                if len(df_data.columns) >= 2:
                    plt.bar(df_data.iloc[:, 0], df_data.iloc[:, 1])
                    plt.xlabel(df_data.columns[0])
                    plt.ylabel(df_data.columns[1])
            
            elif chart_type == 'pie' and not df_data.empty:
                # Gráfico de pastel
                if len(df_data.columns) >= 2:
                    plt.pie(df_data.iloc[:, 1], labels=df_data.iloc[:, 0], autopct='%1.1f%%')
            
            elif chart_type == 'line' and not df_data.empty:
                # Gráfico de líneas
                if len(df_data.columns) >= 2:
                    plt.plot(df_data.iloc[:, 0], df_data.iloc[:, 1], marker='o')
                    plt.xlabel(df_data.columns[0])
                    plt.ylabel(df_data.columns[1])
            
            plt.title(title)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            if filename:
                plt.savefig(filename, dpi=300, bbox_inches='tight')
            
            plt.show()
            return True
            
        except Exception as e:
            self.logger.error(f"Error creando visualización: {e}")
            return False
    
    def export_analysis_to_excel(self, data_dict: Dict[str, pd.DataFrame], 
                                filename: str) -> bool:
        """
        Exporta análisis a Excel con múltiples hojas
        Uso avanzado de pandas para exportación
        """
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                for sheet_name, df in data_dict.items():
                    if not df.empty:
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            self.logger.info(f"Análisis exportado a: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exportando a Excel: {e}")
            return False

# Funciones de orden superior para análisis funcional
def apply_analysis_pipeline(data: List[Dict], 
                          transformations: List[callable]) -> Any:
    """
    Aplica una serie de transformaciones a los datos
    Programación funcional: pipeline de transformaciones
    """
    result = data
    for transform in transformations:
        result = transform(result)
    return result

def filter_data_by_criteria(data: List[Dict], 
                          criteria: Dict[str, Any]) -> List[Dict]:
    """
    Filtra datos según criterios específicos
    Programación funcional: filtrado avanzado
    """
    def matches_criteria(item: Dict) -> bool:
        return all(
            item.get(key) == value 
            for key, value in criteria.items()
        )
    
    return list(filter(matches_criteria, data))

def aggregate_data_by_field(data: List[Dict], 
                          group_field: str, 
                          agg_field: str, 
                          agg_func: callable = sum) -> Dict[str, Any]:
    """
    Agrupa y agrega datos por campo específico
    Programación funcional: agregación personalizada
    """
    from collections import defaultdict
    
    groups = defaultdict(list)
    
    # Agrupar datos
    for item in data:
        key = item.get(group_field)
        value = item.get(agg_field)
        if key is not None and value is not None:
            groups[key].append(value)
    
    # Aplicar función de agregación
    return {key: agg_func(values) for key, values in groups.items()}

# Funciones lambda para análisis rápido
calculate_percentage = lambda part, total: (part / total * 100) if total > 0 else 0
format_percentage = lambda value: f"{value:.1f}%"
safe_divide = lambda a, b: a / b if b != 0 else 0

# Predicados para análisis lógico
is_high_enrollment = lambda course: course.get('porcentaje_ocupacion', 0) > 80
is_low_enrollment = lambda course: course.get('porcentaje_ocupacion', 0) < 30
is_active_enrollment = lambda enrollment: enrollment.get('estado') == 'ACTIVA'
is_recent_enrollment = lambda enrollment: (
    datetime.now() - enrollment.get('fecha_matricula', datetime.min)
).days <= 30 if enrollment.get('fecha_matricula') else False