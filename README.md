# 🫁 Sistema Experto de Orientación Preliminar de Enfermedades Respiratorias

Este proyecto implementa un **Sistema Experto (SE)** basado en conocimiento y reglas de inferencia clínica para el diagnóstico y triaje rápido de enfermedades respiratorias comunes. Desarrollado en **Python** e implementado con una interfaz interactiva en **Streamlit**.

---

## 📌 1. Delimitación del Sistema Experto

- **Especialidad de la Salud**: Medicina Respiratoria / Neumología Básica.
- **Enfermedades Evaluadas**:
  - `D1`: Resfriado común (Infección viral alta).
  - `D2`: Influenza (Gripe aguda).
  - `D3`: Sospecha de Faringitis Estreptocócica (Infección bacteriana).
  - `D4`: Bronquitis Aguda (Inflamación traqueobronquial).
  - `D5`: **Signos de Alarma (Atención Médica Urgente)**.
  - `D6`: Resultado No Concluyente / Atípico.

---

## 🛠️ 2. Metodología de Desarrollo (Guía de 7 Pasos)

El desarrollo sigue rigurosamente la metodología de construcción de sistemas expertos:

1. **Paso 1: Descripción del Dominio**: Identificación del problema de traslape sintomático (tos, fiebre, congestión, odinofagia) y establecimiento de bases de conocimiento clínico (CDC).
2. **Paso 2: Aislar el Área de Desarrollo**: Delimitación de 19 variables de entrada (`S01` a `S19`) mapeadas a 6 resultados posibles.
3. **Paso 3: Objetivo del Prototipo**: Brindar orientación asistencial preliminar con reglas *IF-THEN* y detección temprana de alertas de emergencia.
4. **Paso 4: Diagrama de Dependencias**: Jerarquización de dos niveles:
   - **Nivel 1 (Prioritario)**: Signos de alarma (dificultad respiratoria, dolor torácico, confusión, empeoramiento).
   - **Nivel 2**: Patrón respiratorio por coincidencia sintomática.
5. **Paso 5: Tablas de Decisión**: Mapeo de combinaciones lógicas de condiciones y acciones.
6. **Paso 6: Transformación a Reglas IF-THEN**: Representación del conocimiento mediante motor de inferencia encadenada hacia adelante (*Forward Chaining*).
7. **Paso 7: Implementación en Python & Streamlit**: Motor modular en `inference_engine.py` e interfaz en `app.py`.

---

## 🚀 3. Instrucciones de Ejecución Local

### Prerrequisitos
Tener instalado Python 3.10 o superior.

### Pasos
1. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecutar la aplicación en Streamlit:
   ```bash
   streamlit run app.py
   ```
3. Abrir el navegador en `http://localhost:8501`.

---

## 🌐 4. Despliegue en Streamlit Community Cloud & GitHub

Para compartir el sistema online en Streamlit Cloud:

1. **Crear repositorio en GitHub**:
   - Subir los archivos `app.py`, `inference_engine.py`, `knowledge_base.py`, `requirements.txt` y `README.md` a su cuenta de GitHub (ejemplo: `https://github.com/tu-usuario/sistema-experto-respiratorio`).

2. **Desplegar en Streamlit Cloud**:
   - Ingrese a [Streamlit Community Cloud](https://share.streamlit.io/).
   - Haga clic en **"New app"**.
   - Seleccione el repositorio de GitHub, la rama `main` (o `master`) y el archivo principal `app.py`.
   - Haga clic en **"Deploy!"**.

3. **Enlace Directo**:
   - La aplicación estará disponible en una URL del tipo:
     `https://<tu-usuario>-sistema-experto-respiratorio.streamlit.app`

---

### 👨‍⚕️ Nota Médica
*Este sistema es un prototipo con fines educativos de la materia Sistemas Expertos y no reemplaza el juicio clínico de un médico especialista.*
