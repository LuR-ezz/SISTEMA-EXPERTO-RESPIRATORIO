"""
Base de Conocimiento para el Sistema Experto de Orientación Respiratoria.
Basado en los lineamientos de la Guía de Sistemas Expertos y el documento de Orientación Preliminar.
"""

CONDITIONS = {
    "D1": {
        "name": "Resfriado común",
        "category": "Infección viral de vías respiratorias superiores",
        "description": "Enfermedad viral leve caracterizada por congestión nasal, secreción nasal, estornudos, tos y molestia leve en la garganta.",
        "icon": "🤧",
        "color": "#2563EB",
        "recommendation": "Reposo, hidratación abundante y manejo sintomático. Si los síntomas persisten más de 10 días o empeoran, consulte a un profesional médico."
    },
    "D2": {
        "name": "Influenza (Gripe)",
        "category": "Infección viral respiratoria aguda",
        "description": "Enfermedad viral de inicio repentino caracterizada por fiebre, tos seca o productiva, dolores musculares intensos (mialgias), dolor de cabeza y fatiga marcada.",
        "icon": "🤒",
        "color": "#DC2626",
        "recommendation": "Aislamiento preventivo, reposo estricto, hidratación constante y monitoreo de la temperatura. Consulte a un médico para evaluar tratamiento antiviral si está en las primeras 48 horas."
    },
    "D3": {
        "name": "Sospecha de Faringitis Estreptocócica",
        "category": "Infección bacteriana faríngea",
        "description": "Infección bacteriana faríngea caracterizada por dolor de garganta intenso de inicio súbito, odinofagia, fiebre y exudado amigdalino, típicamente sin tos ni rinorrea.",
        "icon": "🗣️",
        "color": "#D97706",
        "recommendation": "Requiere evaluación médica profesional para confirmación mediante prueba rápida de estreptococo o cultivo faríngeo y prescripción adecuada de antibióticos."
    },
    "D4": {
        "name": "Bronquitis Aguda",
        "category": "Inflamación de vías respiratorias inferiores",
        "description": "Inflamación de la mucosa bronquial caracterizada principalmente por tos molesta (con o sin expectoración de mucosidad) que puede prolongarse de 1 a 3 semanas.",
        "icon": "🫁",
        "color": "#7C3AED",
        "recommendation": "Hidratación, uso de humidificadores y evitar irritantes bronquiales (como humo de tabaco). Consulte al médico si presenta sibilancias o dificultad al respirar."
    },
    "D5": {
        "name": "SIGNOS DE ALARMA - ATENCIÓN MÉDICA URGENTE",
        "category": "Criterio de Gravedad / Emergencia Médica",
        "description": "Se detectaron signos de alarma clínicos (dificultad respiratoria, dolor en el pecho, confusión o empeoramiento tras mejoría).",
        "icon": "🚨",
        "color": "#B91C1C",
        "recommendation": "¡ATENCIÓN URGENTE! Acuda de inmediato a un centro de urgencias o solicite asistencia médica de emergencia. No automedicarse."
    },
    "D6": {
        "name": "Resultado No Concluyente",
        "category": "Patrón Indeterminado",
        "description": "El patrón de síntomas ingresado no coincide con suficiente especificidad con las reglas de las condiciones evaluadas.",
        "icon": "❓",
        "color": "#4B5563",
        "recommendation": "Monitoree la evolución de sus síntomas. Si estos aumentan de intensidad o aparecen nuevos signos, consulte a un profesional de la salud."
    }
}

VARIABLES = {
    "S01": {"code": "S01", "name": "Fiebre o sensación febril", "type": "bool", "category": "Síntomas Generales"},
    "S02": {"code": "S02", "name": "Inicio repentino / súbito de los síntomas", "type": "bool", "category": "Síntomas Generales"},
    "S03": {"code": "S03", "name": "Tos", "type": "bool", "category": "Vías Respiratorias Bajas"},
    "S04": {"code": "S04", "name": "Secreción nasal (Rinorrea)", "type": "bool", "category": "Vías Respiratorias Altas"},
    "S05": {"code": "S05", "name": "Congestión nasal", "type": "bool", "category": "Vías Respiratorias Altas"},
    "S06": {"code": "S06", "name": "Estornudos frecuentes", "type": "bool", "category": "Vías Respiratorias Altas"},
    "S07": {"code": "S07", "name": "Dolor de garganta", "type": "bool", "category": "Vías Respiratorias Altas"},
    "S08": {"code": "S08", "name": "Dolor al tragar (Odinofagia)", "type": "bool", "category": "Vías Respiratorias Altas"},
    "S09": {"code": "S09", "name": "Dolor muscular / corporal (Mialgias)", "type": "bool", "category": "Síntomas Generales"},
    "S10": {"code": "S10", "name": "Fatiga o cansancio intenso", "type": "bool", "category": "Síntomas Generales"},
    "S11": {"code": "S11", "name": "Amígdalas inflamadas o enrojecidas", "type": "bool", "category": "Examen Faríngeo"},
    "S12": {"code": "S12", "name": "Placas blancas / exudado en amígdalas", "type": "bool", "category": "Examen Faríngeo"},
    "S13": {"code": "S13", "name": "Ganglios cervicales inflamados / dolorosos", "type": "bool", "category": "Examen Faríngeo"},
    "S14": {"code": "S14", "name": "Mucosidad o flema con la tos", "type": "bool", "category": "Vías Respiratorias Bajas"},
    "S15": {"code": "S15", "name": "Dificultad para respirar (Falta de aire)", "type": "bool", "category": "Signos de Alarma"},
    "S16": {"code": "S16", "name": "Dolor o presión persistente en el pecho", "type": "bool", "category": "Signos de Alarma"},
    "S17": {"code": "S17", "name": "Confusión o mareo persistente", "type": "bool", "category": "Signos de Alarma"},
    "S18": {"code": "S18", "name": "Síntomas mejoraron y luego empeoraron severamente", "type": "bool", "category": "Signos de Alarma"},
    "S19": {"code": "S19", "name": "Duración de los síntomas", "type": "choice", "options": ["≤ 7 días", "8 – 21 días", "> 21 días"], "category": "Evolución Temporal"}
}
