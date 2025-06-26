"""
Autor: Sistema de Matrículas Universitarias
Módulo: Comparación de Lenguajes de Programación
Descripción: Cuadro comparativo de lenguajes más usados
Paradigma: Funcional con análisis de datos
"""

import pandas as pd
from typing import Dict, List, Any

def get_programming_languages_comparison() -> pd.DataFrame:
    """
    Retorna un DataFrame con comparación de lenguajes de programación
    Aplicación de ciencia de datos para mostrar información educativa
    """
    
    # Datos de lenguajes de programación más populares (2024)
    languages_data = [
        {
            'Lenguaje': 'Python',
            'Paradigma': 'Multiparadigma',
            'Tipado': 'Dinámico',
            'Año_Creacion': 1991,
            'Popularidad_2024': 29.9,
            'Uso_Principal': 'IA, Data Science, Web',
            'Facilidad_Aprendizaje': 'Alta',
            'Performance': 'Media',
            'Comunidad': 'Muy Grande'
        },
        {
            'Lenguaje': 'JavaScript',
            'Paradigma': 'Multiparadigma',
            'Tipado': 'Dinámico',
            'Año_Creacion': 1995,
            'Popularidad_2024': 26.8,
            'Uso_Principal': 'Web Frontend/Backend',
            'Facilidad_Aprendizaje': 'Media',
            'Performance': 'Media',
            'Comunidad': 'Muy Grande'
        },
        {
            'Lenguaje': 'Java',
            'Paradigma': 'Orientado a Objetos',
            'Tipado': 'Estático',
            'Año_Creacion': 1995,
            'Popularidad_2024': 20.6,
            'Uso_Principal': 'Empresarial, Android',
            'Facilidad_Aprendizaje': 'Media',
            'Performance': 'Alta',
            'Comunidad': 'Muy Grande'
        },
        {
            'Lenguaje': 'C#',
            'Paradigma': 'Multiparadigma',
            'Tipado': 'Estático',
            'Año_Creacion': 2000,
            'Popularidad_2024': 17.3,
            'Uso_Principal': 'Windows, Web, Games',
            'Facilidad_Aprendizaje': 'Media',
            'Performance': 'Alta',
            'Comunidad': 'Grande'
        },
        {
            'Lenguaje': 'C++',
            'Paradigma': 'Multiparadigma',
            'Tipado': 'Estático',
            'Año_Creacion': 1985,
            'Popularidad_2024': 14.5,
            'Uso_Principal': 'Sistemas, Games, HPC',
            'Facilidad_Aprendizaje': 'Baja',
            'Performance': 'Muy Alta',
            'Comunidad': 'Grande'
        },
        {
            'Lenguaje': 'TypeScript',
            'Paradigma': 'Multiparadigma',
            'Tipado': 'Estático',
            'Año_Creacion': 2012,
            'Popularidad_2024': 12.7,
            'Uso_Principal': 'Web Frontend',
            'Facilidad_Aprendizaje': 'Media',
            'Performance': 'Media',
            'Comunidad': 'Grande'
        },
        {
            'Lenguaje': 'Go',
            'Paradigma': 'Imperativo',
            'Tipado': 'Estático',
            'Año_Creacion': 2009,
            'Popularidad_2024': 8.9,
            'Uso_Principal': 'Backend, Cloud',
            'Facilidad_Aprendizaje': 'Media',
            'Performance': 'Alta',
            'Comunidad': 'Media'
        },
        {
            'Lenguaje': 'Rust',
            'Paradigma': 'Multiparadigma',
            'Tipado': 'Estático',
            'Año_Creacion': 2010,
            'Popularidad_2024': 7.8,
            'Uso_Principal': 'Sistemas, Seguridad',
            'Facilidad_Aprendizaje': 'Baja',
            'Performance': 'Muy Alta',
            'Comunidad': 'Media'
        },
        {
            'Lenguaje': 'PHP',
            'Paradigma': 'Multiparadigma',
            'Tipado': 'Dinámico',
            'Año_Creacion': 1995,
            'Popularidad_2024': 7.2,
            'Uso_Principal': 'Web Backend',
            'Facilidad_Aprendizaje': 'Alta',
            'Performance': 'Media',
            'Comunidad': 'Grande'
        },
        {
            'Lenguaje': 'Swift',
            'Paradigma': 'Multiparadigma',
            'Tipado': 'Estático',
            'Año_Creacion': 2014,
            'Popularidad_2024': 6.1,
            'Uso_Principal': 'iOS, macOS',
            'Facilidad_Aprendizaje': 'Media',
            'Performance': 'Alta',
            'Comunidad': 'Media'
        }
    ]
    
    return pd.DataFrame(languages_data)

def generate_languages_report() -> str:
    """
    Genera un reporte textual de comparación de lenguajes
    Uso de programación funcional para análisis
    """
    df = get_programming_languages_comparison()
    
    report = "=== COMPARACIÓN DE LENGUAJES DE PROGRAMACIÓN 2024 ===\n\n"
    
    # Top 5 más populares
    top_5 = df.nlargest(5, 'Popularidad_2024')
    report += "TOP 5 LENGUAJES MÁS POPULARES:\n"
    for idx, row in top_5.iterrows():
        report += f"{idx+1}. {row['Lenguaje']} - {row['Popularidad_2024']}%\n"
    report += "\n"
    
    # Análisis por paradigma
    paradigm_counts = df['Paradigma'].value_counts()
    report += "DISTRIBUCIÓN POR PARADIGMA:\n"
    for paradigma, count in paradigm_counts.items():
        percentage = (count / len(df) * 100).round(1)
        report += f"- {paradigma}: {count} lenguajes ({percentage}%)\n"
    report += "\n"
    
    # Análisis por tipado
    typing_counts = df['Tipado'].value_counts()
    report += "DISTRIBUCIÓN POR TIPO DE TIPADO:\n"
    for tipado, count in typing_counts.items():
        percentage = (count / len(df) * 100).round(1)
        report += f"- {tipado}: {count} lenguajes ({percentage}%)\n"
    report += "\n"
    
    # Lenguajes por facilidad de aprendizaje
    learning_ease = df.groupby('Facilidad_Aprendizaje')['Lenguaje'].apply(list)
    report += "LENGUAJES POR FACILIDAD DE APRENDIZAJE:\n"
    for nivel, lenguajes in learning_ease.items():
        report += f"- {nivel}: {', '.join(lenguajes)}\n"
    report += "\n"
    
    # Análisis de performance
    performance_groups = df.groupby('Performance')['Lenguaje'].apply(list)
    report += "LENGUAJES POR PERFORMANCE:\n"
    for nivel, lenguajes in performance_groups.items():
        report += f"- {nivel}: {', '.join(lenguajes)}\n"
    report += "\n"
    
    # Recomendaciones por uso
    report += "RECOMENDACIONES POR ÁREA DE USO:\n"
    
    # Agrupar por uso principal usando programación funcional
    use_cases = {}
    for _, row in df.iterrows():
        uses = row['Uso_Principal'].split(', ')
        for use in uses:
            if use not in use_cases:
                use_cases[use] = []
            use_cases[use].append(row['Lenguaje'])
    
    for uso, lenguajes in use_cases.items():
        report += f"- {uso}: {', '.join(lenguajes)}\n"
    report += "\n"
    
    # Análisis temporal
    modern_languages = df[df['Año_Creacion'] >= 2000]
    classic_languages = df[df['Año_Creacion'] < 2000]
    
    report += "ANÁLISIS TEMPORAL:\n"
    report += f"- Lenguajes modernos (2000+): {len(modern_languages)} ({len(modern_languages)/len(df)*100:.1f}%)\n"
    report += f"- Lenguajes clásicos (<2000): {len(classic_languages)} ({len(classic_languages)/len(df)*100:.1f}%)\n"
    report += "\n"
    
    # Tendencias y conclusiones
    report += "TENDENCIAS Y CONCLUSIONES:\n"
    report += "1. Python mantiene su liderazgo gracias a IA y Data Science\n"
    report += "2. JavaScript sigue siendo esencial para desarrollo web\n"
    report += "3. Los lenguajes multiparadigma dominan el mercado\n"
    report += "4. Hay equilibrio entre tipado estático y dinámico\n"
    report += "5. Los lenguajes modernos se enfocan en seguridad y performance\n"
    
    return report

def get_python_advantages() -> List[str]:
    """
    Retorna las ventajas de Python como lenguaje
    Justificación de la elección para este proyecto
    """
    return [
        "Sintaxis clara y legible (Zen of Python)",
        "Multiparadigma: soporta POO, funcional, imperativo",
        "Gran ecosistema de librerías (pandas, numpy, tkinter)",
        "Excelente para prototipado rápido",
        "Comunidad muy activa y documentación extensa",
        "Ideal para ciencia de datos y análisis",
        "Fácil integración con bases de datos",
        "Interpretado: desarrollo ágil sin compilación",
        "Multiplataforma: funciona en Windows, Linux, macOS",
        "Usado en industria: Google, Netflix, Instagram, etc."
    ]

def compare_paradigms() -> Dict[str, Dict[str, Any]]:
    """
    Compara los paradigmas de programación implementados en el proyecto
    Análisis teórico de los paradigmas aplicados
    """
    return {
        'Orientado_a_Objetos': {
            'descripcion': 'Organiza código en clases y objetos con encapsulación, herencia y polimorfismo',
            'ventajas': [
                'Reutilización de código',
                'Mantenibilidad',
                'Modelado natural del mundo real',
                'Encapsulación de datos'
            ],
            'aplicacion_proyecto': [
                'Clases Estudiante, Curso, Matricula',
                'Herencia en BaseDAO',
                'Encapsulación con propiedades',
                'Polimorfismo en métodos DAO'
            ],
            'ejemplos_codigo': [
                'class Estudiante(Persona)',
                'def __init__(self, ...)',
                '@property',
                'super().__init__(...)'
            ]
        },
        'Funcional': {
            'descripcion': 'Trata las funciones como ciudadanos de primera clase, evita efectos secundarios',
            'ventajas': [
                'Código más predecible',
                'Fácil testing',
                'Paralelización natural',
                'Inmutabilidad'
            ],
            'aplicacion_proyecto': [
                'Funciones map(), filter(), reduce()',
                'Funciones lambda',
                'Funciones de orden superior',
                'Inmutabilidad en listas'
            ],
            'ejemplos_codigo': [
                'list(filter(lambda m: m.esta_activa(), matriculas))',
                'list(map(self._row_to_estudiante, results))',
                'funciones como parámetros',
                'return lista.copy()'
            ]
        },
        'Logico': {
            'descripcion': 'Basado en reglas y predicados lógicos para tomar decisiones',
            'ventajas': [
                'Expresión natural de reglas de negocio',
                'Fácil validación',
                'Código autodocumentado',
                'Mantenimiento simplificado'
            ],
            'aplicacion_proyecto': [
                'Predicados de validación',
                'Reglas de matrícula',
                'Verificación de prerrequisitos',
                'Estados de transición'
            ],
            'ejemplos_codigo': [
                'def puede_matricularse(self) -> bool',
                'def esta_activa(self) -> bool',
                'if not self.tiene_cupos_disponibles()',
                'reglas de transición de estados'
            ]
        }
    }

def print_languages_comparison():
    """
    Imprime la comparación de lenguajes en consola
    Función para mostrar información educativa
    """
    print(generate_languages_report())
    
    print("\n" + "="*60)
    print("VENTAJAS DE PYTHON PARA ESTE PROYECTO:")
    print("="*60)
    
    advantages = get_python_advantages()
    for i, advantage in enumerate(advantages, 1):
        print(f"{i:2d}. {advantage}")
    
    print("\n" + "="*60)
    print("PARADIGMAS IMPLEMENTADOS EN EL PROYECTO:")
    print("="*60)
    
    paradigms = compare_paradigms()
    for paradigm_name, paradigm_info in paradigms.items():
        print(f"\n{paradigm_name.replace('_', ' ').upper()}:")
        print(f"Descripción: {paradigm_info['descripcion']}")
        print("Aplicación en el proyecto:")
        for app in paradigm_info['aplicacion_proyecto']:
            print(f"  - {app}")

# Funciones lambda para análisis de lenguajes
is_modern_language = lambda year: year >= 2000
is_high_performance = lambda perf: perf in ['Alta', 'Muy Alta']
is_easy_to_learn = lambda ease: ease == 'Alta'
is_multiparadigm = lambda paradigm: paradigm == 'Multiparadigma'

# Función de orden superior para filtrar lenguajes
def filter_languages_by_criteria(df: pd.DataFrame, *criteria_functions) -> pd.DataFrame:
    """
    Filtra lenguajes aplicando múltiples criterios
    Programación funcional: composición de predicados
    """
    result = df.copy()
    
    for criterion in criteria_functions:
        if criterion.__name__ == 'is_modern_language':
            result = result[result['Año_Creacion'].apply(criterion)]
        elif criterion.__name__ == 'is_high_performance':
            result = result[result['Performance'].apply(criterion)]
        elif criterion.__name__ == 'is_easy_to_learn':
            result = result[result['Facilidad_Aprendizaje'].apply(criterion)]
        elif criterion.__name__ == 'is_multiparadigm':
            result = result[result['Paradigma'].apply(criterion)]
    
    return result