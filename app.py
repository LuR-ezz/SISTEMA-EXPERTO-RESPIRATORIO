"""
Sistema Experto para Orientación Preliminar de Enfermedades Respiratorias
Interfaz de Usuario desarrollada en Streamlit.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from knowledge_base import CONDITIONS, VARIABLES
from inference_engine import evaluate_patient

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA STREAMLIT
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sistema Experto Respiratorio",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .card-alarm {
        background-color: #FEF2F2;
        border-left: 6px solid #DC2626;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .card-result {
        background-color: #F0FDF4;
        border-left: 6px solid #16A34A;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .rule-box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        padding: 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
        white-space: pre-wrap;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# ENCABEZADO Y TÍTULO
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">🫁 Sistema Experto de Orientación Respiratoria</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Especialidad: Medicina Respiratoria | Diagnóstico Rápido mediante Motor de Inferencia de Reglas (CDC)</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# BARRA LATERAL: DATOS DEL PACIENTE Y PRESETS DE PRUEBA
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/387/387561.png", width=70)
    st.header("📋 Datos del Paciente")
    
    patient_id = st.text_input("Nombre o Código del Paciente", value="Paciente-001")
    age = st.number_input("Edad (años)", min_value=1, max_value=120, value=30)
    gender = st.selectbox("Género", ["Femenino", "Masculino", "Otro"])
    
    st.divider()
    st.header("🚀 Casos Clínicos Predefinidos")
    st.caption("Cargar rápidamente combinaciones típicas de síntomas:")
    
    preset = st.radio(
        "Seleccionar Preset:",
        ["Personalizado", "Caso 1: Resfriado Común", "Caso 2: Influenza Aguda", "Caso 3: Faringitis Estreptocócica", "Caso 4: Signo de Alarma (Disnea)"],
        index=0
    )
    
    st.divider()
    st.info("ℹ️ **Sistema Experto Basado en Reglas**: Este sistema aplica inferencia hacia adelante (Forward Chaining) evaluando síntomas clínicos de entrada según guías epidemiológicas del CDC.")

# Inicializar o actualizar estado de variables según Preset elegido
def get_preset_values(preset_name):
    defaults = {f"S{i:02d}": False for i in range(1, 19)}
    defaults["S19"] = "≤ 7 días"
    
    if preset_name == "Caso 1: Resfriado Común":
        defaults["S04"] = True # Rinorrea
        defaults["S05"] = True # Congestión
        defaults["S06"] = True # Estornudos
        defaults["S07"] = True # Dolor garganta
        defaults["S03"] = True # Tos
        defaults["S19"] = "≤ 7 días"
    elif preset_name == "Caso 2: Influenza Aguda":
        defaults["S01"] = True # Fiebre
        defaults["S02"] = True # Inicio súbito
        defaults["S03"] = True # Tos
        defaults["S09"] = True # Mialgias
        defaults["S10"] = True # Fatiga
        defaults["S19"] = "≤ 7 días"
    elif preset_name == "Caso 3: Faringitis Estreptocócica":
        defaults["S01"] = True # Fiebre
        defaults["S02"] = True # Inicio súbito
        defaults["S07"] = True # Dolor garganta
        defaults["S08"] = True # Odinofagia
        defaults["S12"] = True # Exudado amigdalino
        defaults["S13"] = True # Ganglios
        defaults["S03"] = False # Sin tos
        defaults["S04"] = False # Sin rinorrea
        defaults["S19"] = "≤ 7 días"
    elif preset_name == "Caso 4: Signo de Alarma (Disnea)":
        defaults["S01"] = True
        defaults["S03"] = True
        defaults["S15"] = True # Dificultad para respirar!
        defaults["S16"] = True # Dolor pecho
        defaults["S19"] = "8 – 21 días"
        
    return defaults

preset_vals = get_preset_values(preset)

# -----------------------------------------------------------------------------
# FORMULARIO DE CAPTURA DE SÍNTOMAS (VARIABLES S01 - S19)
# -----------------------------------------------------------------------------
tab_eval, tab_rules, tab_doc = st.tabs(["📝 Evaluador de Síntomas", "🔍 Árbol de Reglas e Inferencia", "📚 Documentación de la Guía"])

with tab_eval:
    st.subheader("1. Ingrese los Síntomas Observados / Reportados")
    st.write("Seleccione los signos y síntomas presentes en la evaluación inicial:")
    
    col1, col2, col3 = st.columns(3)
    
    patient_inputs = {}
    
    with col1:
        st.markdown("##### 🤒 Síntomas Generales")
        patient_inputs["S01"] = st.checkbox(VARIABLES["S01"]["name"], value=preset_vals["S01"], help="Presencia de fiebre o sensación de alza térmica")
        patient_inputs["S02"] = st.checkbox(VARIABLES["S02"]["name"], value=preset_vals["S02"], help="Los síntomas aparecieron repentinamente en pocas horas")
        patient_inputs["S09"] = st.checkbox(VARIABLES["S09"]["name"], value=preset_vals["S09"], help="Dolor generalizado en músculos y cuerpo")
        patient_inputs["S10"] = st.checkbox(VARIABLES["S10"]["name"], value=preset_vals["S10"], help="Sensación marcada de cansancio y debilidad")

        st.markdown("##### ⏱️ Evolución Temporal (S19)")
        patient_inputs["S19"] = st.selectbox(
            VARIABLES["S19"]["name"],
            VARIABLES["S19"]["options"],
            index=VARIABLES["S19"]["options"].index(preset_vals["S19"])
        )

    with col2:
        st.markdown("##### 🗣️ Vías Respiratorias Altas y Faringe")
        patient_inputs["S04"] = st.checkbox(VARIABLES["S04"]["name"], value=preset_vals["S04"])
        patient_inputs["S05"] = st.checkbox(VARIABLES["S05"]["name"], value=preset_vals["S05"])
        patient_inputs["S06"] = st.checkbox(VARIABLES["S06"]["name"], value=preset_vals["S06"])
        patient_inputs["S07"] = st.checkbox(VARIABLES["S07"]["name"], value=preset_vals["S07"])
        patient_inputs["S08"] = st.checkbox(VARIABLES["S08"]["name"], value=preset_vals["S08"])

        st.markdown("##### 🔬 Examen Físico Faríngeo")
        patient_inputs["S11"] = st.checkbox(VARIABLES["S11"]["name"], value=preset_vals["S11"])
        patient_inputs["S12"] = st.checkbox(VARIABLES["S12"]["name"], value=preset_vals["S12"])
        patient_inputs["S13"] = st.checkbox(VARIABLES["S13"]["name"], value=preset_vals["S13"])

    with col3:
        st.markdown("##### 🫁 Vías Respiratorias Bajas")
        patient_inputs["S03"] = st.checkbox(VARIABLES["S03"]["name"], value=preset_vals["S03"])
        patient_inputs["S14"] = st.checkbox(VARIABLES["S14"]["name"], value=preset_vals["S14"])

        st.markdown("##### 🚨 Signos de Alarma (Nivel 1)")
        st.caption("Criterios de gravedad de prioridad absoluta:")
        patient_inputs["S15"] = st.checkbox(VARIABLES["S15"]["name"], value=preset_vals["S15"])
        patient_inputs["S16"] = st.checkbox(VARIABLES["S16"]["name"], value=preset_vals["S16"])
        patient_inputs["S17"] = st.checkbox(VARIABLES["S17"]["name"], value=preset_vals["S17"])
        patient_inputs["S18"] = st.checkbox(VARIABLES["S18"]["name"], value=preset_vals["S18"])

    st.divider()
    
    # -------------------------------------------------------------------------
    # EJECUCIÓN DEL MOTOR DE INFERENCIA
    # -------------------------------------------------------------------------
    btn_eval = st.button("🚀 Evaluar Diagnóstico con Sistema Experto", type="primary", use_container_width=True)

    results = evaluate_patient(patient_inputs)
    cond_info = results["condition_details"]
    
    st.subheader("2. Resultado del Diagnóstico Preliminar")
    
    # SI HAY SIGNOS DE ALARMA (D5)
    if results["has_alarms"]:
        st.error(f"### {cond_info['icon']} {cond_info['name']}")
        st.markdown(f"**Categoría:** {cond_info['category']}")
        st.markdown(f"**Descripción:** {cond_info['description']}")
        
        st.warning("**⚠️ SIGNOS DE ALARMA DETECTADOS EN EL PACIENTE:**")
        for trigger in results["alarm_triggers"]:
            st.write(f"- 🔴 **{trigger}**")
            
        st.error(f"**💡 Recomendación de Emergencia:** {cond_info['recommendation']}")
        
    else:
        # DIAGNÓSTICO ESTÁNDAR (D1, D2, D3, D4, D6)
        card_bg = cond_info["color"]
        st.markdown(f"""
            <div style="background-color: {card_bg}15; border-left: 6px solid {card_bg}; padding: 1.2rem; border-radius: 8px;">
                <h2 style="color: {card_bg}; margin-top:0;">{cond_info['icon']} {cond_info['name']}</h2>
                <p><b>Categoría Clínica:</b> {cond_info['category']}</p>
                <p>{cond_info['description']}</p>
                <hr>
                <p style="font-size: 1.05rem;"><b>💡 Recomendación Asistencial:</b> {cond_info['recommendation']}</p>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader("3. Análisis de Coincidencia de Patrones (%)")
    
    df_rank = pd.DataFrame(results["sorted_ranking"], columns=["Código", "Condición", "Coincidencia (%)"])
    
    col_chart, col_reasons = st.columns([1.2, 1])
    
    with col_chart:
        fig = px.bar(
            df_rank,
            x="Coincidencia (%)",
            y="Condición",
            orientation="h",
            color="Coincidencia (%)",
            color_continuous_scale="Blues",
            text="Coincidencia (%)",
            title="Porcentaje de Coincidencia por Patrón de Enfermedad"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"), height=320)
        st.plotly_chart(fig, use_container_width=True)

    with col_reasons:
        st.markdown("##### 📌 Justificación de Reglas por Condición")
        for code in ["D1", "D2", "D3", "D4"]:
            reasons = results["reasons"][code]
            with st.expander(f"{CONDITIONS[code]['icon']} {CONDITIONS[code]['name']} ({results['percentages'][code]}%)"):
                if reasons:
                    for r in reasons:
                        st.write(f"- {r}")
                else:
                    st.caption("No se activaron reglas específicas para esta condición.")

# -----------------------------------------------------------------------------
# TAB 2: ÁRBOLES DE REGLAS E INFERENCIA
# -----------------------------------------------------------------------------
with tab_rules:
    st.subheader("🔍 Traza de Ejecución del Motor de Inferencia (Forward Chaining)")
    st.write("Demostración paso a paso del proceso de inferencia y reglas activadas:")
    
    st.code(results["rule_trace"], language="markdown")

    st.divider()
    st.subheader("🌐 Diagrama de Dependencias del Sistema Experto")
    
    st.markdown("""
    ```mermaid
    graph TD
        A[Síntomas del Usuario S01-S19] --> B{¿Signo de Alarma S15-S18?}
        B -- SÍ --> C[🚨 D5: Signos de Alarma / Emergencia URGENTE]
        B -- NO --> D[Motor de Inferencia Nivel 2]
        
        D --> E[Evaluación Reglas D1 Resfriado Común]
        D --> F[Evaluación Reglas D2 Influenza Aguda]
        D --> G[Evaluación Reglas D3 Faringitis Estreptocócica]
        D --> H[Evaluación Reglas D4 Bronquitis Aguda]
        
        E --> I[Cálculo de Porcentajes de Coincidencia]
        F --> I
        G --> I
        H --> I
        
        I --> J{¿Mayor Coincidencia >= 40%?}
        J -- SÍ --> K[Diagnóstico Compatibilidad Mayor D1-D4]
        J -- NO --> L[❓ D6: Resultado No Concluyente]
    ```
    """)

# -----------------------------------------------------------------------------
# TAB 3: DOCUMENTACIÓN DE LA GUÍA DE METODOLOGÍA
# -----------------------------------------------------------------------------
with tab_doc:
    st.subheader("📚 Metodología de Construcción del Sistema Experto (Guía de 7 Pasos)")
    
    st.markdown("""
    Este Sistema Experto ha sido construido siguiendo rigurosamente los 7 pasos definidos en la guía metodológica de desarrollo de Sistemas Expertos:

    1. **Paso 1: Descripción del Dominio de Aplicación**: Orientación preliminar en el área de medicina respiratoria.
    2. **Paso 2: Aislar el Área de Desarrollo**: Delimitación a 4 enfermedades comunes (Resfriado Común, Influenza, Faringitis Estreptocócica, Bronquitis Aguda), 1 categoría de signos de alarma y 1 categoría de resultado indeterminado.
    3. **Paso 3: Decidir el Objetivo del Prototipo**: Proporcionar una herramienta rápida de triaje preliminar basada en conocimiento clínico del CDC.
    4. **Paso 4: Crear el Diagrama de Dependencias**: Inferencia estructurada en dos niveles (Nivel 1: Alarma de Urgencia; Nivel 2: Patrón respiratorio).
    5. **Paso 5: Crear las Tablas de Decisión**: Mapeo de combinaciones de variables S01 a S19 con las salidas esperadas D1 a D6.
    6. **Paso 6: Transformar a Reglas IF-THEN**: Representación formal del conocimiento clínico mediante reglas condicionales ponderadas.
    7. **Paso 7: Implementación del Motor de Inferencia e Interfaz**: Desarrollo del motor en Python puro y despliegue interactivo mediante **Streamlit**.
    """)

# Pie de página
st.divider()
st.caption("Desarrollado para la materia de SISTEMA EXPERTO | Implementación en Python & Streamlit | 2026")
