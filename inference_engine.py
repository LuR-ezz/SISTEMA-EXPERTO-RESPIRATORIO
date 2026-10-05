"""
Motor de Inferencia del Sistema Experto de Orientación Respiratoria.
Implementa inferencia encadenada hacia adelante (forward chaining) y coincidencia de patrones basada en reglas IF-THEN.
"""

from knowledge_base import CONDITIONS, VARIABLES

def evaluate_patient(patient_data):
    """
    Evalúa los síntomas del paciente utilizando dos niveles de inferencia:
    - Nivel 1: Evaluación de Signos de Alarma (Emergencia médica).
    - Nivel 2: Identificación del patrón respiratorio compatible (D1, D2, D3, D4).
    """
    rule_trace = []
    alarm_triggers = []
    
    # -------------------------------------------------------------------------
    # NIVEL 1: SIGNOS DE ALARMA (Máxima Prioridad)
    # -------------------------------------------------------------------------
    rule_trace.append("🔍 [EVALUACIÓN NIVEL 1] Verificando presencia de Signos de Alarma (Reglas de Emergencia CDC)...")
    
    if patient_data.get("S15", False):
        alarm_triggers.append("S15: Dificultad para respirar / falta de aire (Disnea)")
        rule_trace.append("  ⚠️ REGLA ALARMA-01 ACTIVADA: S15 = Sí -> Criterio de dificultad respiratoria presente.")
        
    if patient_data.get("S16", False):
        alarm_triggers.append("S16: Dolor o presión persistente en el pecho")
        rule_trace.append("  ⚠️ REGLA ALARMA-02 ACTIVADA: S16 = Sí -> Criterio de dolor/presión torácica constante.")
        
    if patient_data.get("S17", False):
        alarm_triggers.append("S17: Confusión o mareo persistente")
        rule_trace.append("  ⚠️ REGLA ALARMA-03 ACTIVADA: S17 = Sí -> Criterio de alteración del estado neurológico/mareo.")
        
    if patient_data.get("S18", False):
        alarm_triggers.append("S18: Síntomas mejoraron y luego empeoraron severamente")
        rule_trace.append("  ⚠️ REGLA ALARMA-04 ACTIVADA: S18 = Sí -> Criterio de recaída/empeoramiento secundario.")

    has_alarms = len(alarm_triggers) > 0

    # -------------------------------------------------------------------------
    # NIVEL 2: PATRÓN DE ENFERMEDAD RESPIRATORIA
    # -------------------------------------------------------------------------
    rule_trace.append("\n🔬 [EVALUACIÓN NIVEL 2] Analizando patrón clínico mediante Reglas de Inferencia IF-THEN...")
    
    scores = {
        "D1": 0.0, # Resfriado común
        "D2": 0.0, # Influenza
        "D3": 0.0, # Faringitis Estreptocócica
        "D4": 0.0  # Bronquitis Aguda
    }
    
    max_possible = {
        "D1": 10.0,
        "D2": 10.0,
        "D3": 10.0,
        "D4": 10.0
    }

    # REGLAS PARA RESFRIADO COMÚN (D1)
    d1_match_reasons = []
    if patient_data.get("S04", False) and patient_data.get("S05", False):
        scores["D1"] += 3.0
        d1_match_reasons.append("S04 (Rinorrea) y S05 (Congestión nasal) presentes (+3.0)")
        rule_trace.append("  ✔️ REGLA D1-01 ACTIVADA: IF S04=Sí Y S05=Sí THEN Patrón rinogéptico (+3.0 D1)")
        
    if patient_data.get("S06", False):
        scores["D1"] += 2.0
        d1_match_reasons.append("S06 (Estornudos frecuentes) presente (+2.0)")
        rule_trace.append("  ✔️ REGLA D1-02 ACTIVADA: IF S06=Sí THEN Reflejo estornudo (+2.0 D1)")
        
    if patient_data.get("S07", False):
        scores["D1"] += 2.0
        d1_match_reasons.append("S07 (Dolor de garganta) presente (+2.0)")
        rule_trace.append("  ✔️ REGLA D1-03 ACTIVADA: IF S07=Sí THEN Irritación faríngea (+2.0 D1)")
        
    if patient_data.get("S03", False):
        scores["D1"] += 1.5
        d1_match_reasons.append("S03 (Tos leve/moderada) presente (+1.5)")
        rule_trace.append("  ✔️ REGLA D1-04 ACTIVADA: IF S03=Sí THEN Componente tusígeno (+1.5 D1)")

    if not patient_data.get("S09", False):
        scores["D1"] += 1.5
        d1_match_reasons.append("S09 (Ausencia de dolores musculares severos) (+1.5)")
        rule_trace.append("  ✔️ REGLA D1-05 ACTIVADA: IF S09=No THEN Ausencia mialgia sistémica (+1.5 D1)")

    # REGLAS PARA INFLUENZA (D2)
    d2_match_reasons = []
    if patient_data.get("S02", False): # Inicio súbito
        scores["D2"] += 2.5
        d2_match_reasons.append("S02 (Inicio súbito/repentino) (+2.5)")
        rule_trace.append("  ⚡ REGLA D2-01 ACTIVADA: IF S02=Sí THEN Inicio súbito (+2.5 D2)")
        
    if patient_data.get("S09", False): # Mialgias
        scores["D2"] += 2.5
        d2_match_reasons.append("S09 (Dolor muscular / mialgias intensas) (+2.5)")
        rule_trace.append("  ⚡ REGLA D2-02 ACTIVADA: IF S09=Sí THEN Mialgia sistémica (+2.5 D2)")
        
    if patient_data.get("S10", False): # Fatiga
        scores["D2"] += 2.0
        d2_match_reasons.append("S10 (Fatiga / astenia intensa) (+2.0)")
        rule_trace.append("  ⚡ REGLA D2-03 ACTIVADA: IF S10=Sí THEN Cansancio marcado (+2.0 D2)")
        
    if patient_data.get("S03", False): # Tos
        scores["D2"] += 1.5
        d2_match_reasons.append("S03 (Tos) (+1.5)")
        rule_trace.append("  ⚡ REGLA D2-04 ACTIVADA: IF S03=Sí THEN Compromiso respiratorio (+1.5 D2)")
        
    if patient_data.get("S01", False): # Fiebre
        scores["D2"] += 1.5
        d2_match_reasons.append("S01 (Fiebre / sensación febril) (+1.5)")
        rule_trace.append("  ⚡ REGLA D2-05 ACTIVADA: IF S01=Sí THEN Reacción febril (+1.5 D2)")

    # REGLAS PARA FARINGITIS ESTREPTOCÓCICA (D3) (Basadas en criterios clínicos de Centor)
    d3_match_reasons = []
    if patient_data.get("S07", False) and patient_data.get("S08", False):
        scores["D3"] += 2.5
        d3_match_reasons.append("S07 (Dolor de garganta) y S08 (Odinofagia) presentes (+2.5)")
        rule_trace.append("  🔥 REGLA D3-01 ACTIVADA: IF S07=Sí Y S08=Sí THEN Odinofagia marcada (+2.5 D3)")
        
    if patient_data.get("S12", False): # Exudado
        scores["D3"] += 3.0
        d3_match_reasons.append("S12 (Placas blancas/exudado en amígdalas) (+3.0)")
        rule_trace.append("  🔥 REGLA D3-02 ACTIVADA: IF S12=Sí THEN Exudado pultáceo (+3.0 D3)")
        
    elif patient_data.get("S11", False): # Amígdalas inflamadas
        scores["D3"] += 1.5
        d3_match_reasons.append("S11 (Amígdalas inflamadas/eritematosas) (+1.5)")
        rule_trace.append("  🔥 REGLA D3-03 ACTIVADA: IF S11=Sí THEN Eritema amigdalino (+1.5 D3)")

    if patient_data.get("S13", False): # Ganglios cervicales
        scores["D3"] += 2.0
        d3_match_reasons.append("S13 (Adenopatía cervical anterior dolorosa) (+2.0)")
        rule_trace.append("  🔥 REGLA D3-04 ACTIVADA: IF S13=Sí THEN Adenopatía cervical (+2.0 D3)")

    if patient_data.get("S01", False): # Fiebre
        scores["D3"] += 1.5
        d3_match_reasons.append("S01 (Fiebre) (+1.5)")
        rule_trace.append("  🔥 REGLA D3-05 ACTIVADA: IF S01=Sí THEN Respuesta febril (+1.5 D3)")

    # REGLA EXCLUSIÓN VIRAL PARA ESTREPTOCOCO (Ausencia de tos y ausenica de rinorrea orientan a estreptococo)
    if not patient_data.get("S03", False) and not patient_data.get("S04", False):
        scores["D3"] += 1.0
        d3_match_reasons.append("Ausencia de tos y de rinorrea (Criterio negativo para virus, orienta a estreptococo) (+1.0)")
        rule_trace.append("  🔥 REGLA D3-06 ACTIVADA: IF S03=No Y S04=No THEN Ausencia cuadro viral clásico (+1.0 D3)")

    # REGLAS PARA BRONQUITIS AGUDA (D4)
    d4_match_reasons = []
    if patient_data.get("S03", False): # Tos síntoma principal
        scores["D4"] += 3.5
        d4_match_reasons.append("S03 (Tos como síntoma predominante) (+3.5)")
        rule_trace.append("  🌬️ REGLA D4-01 ACTIVADA: IF S03=Sí THEN Síntoma cardinal bronquial (+3.5 D4)")
        
        if patient_data.get("S14", False): # Mucosidad
            scores["D4"] += 2.5
            d4_match_reasons.append("S14 (Tos productiva con mucosidad/flema) (+2.5)")
            rule_trace.append("  🌬️ REGLA D4-02 ACTIVADA: IF S14=Sí THEN Tos expectorante (+2.5 D4)")
        else:
            scores["D4"] += 1.5
            d4_match_reasons.append("S03 (Tos seca no productiva) (+1.5)")
            rule_trace.append("  🌬️ REGLA D4-03 ACTIVADA: IF S14=No THEN Tos irritativa (+1.5 D4)")

    duracion = patient_data.get("S19", "≤ 7 días")
    if duracion in ["8 – 21 días", "> 21 días"] and patient_data.get("S03", False):
        scores["D4"] += 2.5
        d4_match_reasons.append(f"S19 (Duración prolongada de tos: {duracion}) (+2.5)")
        rule_trace.append(f"  🌬️ REGLA D4-04 ACTIVADA: IF S19={duracion} Y S03=Sí THEN Cuadro tusígeno subagudo (+2.5 D4)")
    elif duracion == "≤ 7 días" and patient_data.get("S03", False):
        scores["D4"] += 1.5
        rule_trace.append("  🌬️ REGLA D4-05 ACTIVADA: IF S19=≤ 7 días THEN Fase inicial bronquial (+1.5 D4)")

    if patient_data.get("S10", False):
        scores["D4"] += 1.5
        d4_match_reasons.append("S10 (Fatiga acompañante) (+1.5)")
        rule_trace.append("  🌬️ REGLA D4-06 ACTIVADA: IF S10=Sí THEN Astenia secundaria (+1.5 D4)")

    # -------------------------------------------------------------------------
    # CÁLCULO DE PORCENTAJES Y DIAGNÓSTICO FINAL
    # -------------------------------------------------------------------------
    percentages = {}
    for code, score in scores.items():
        pct = min(100.0, (score / max_possible[code]) * 100.0)
        percentages[code] = round(pct, 1)

    # Ordenar resultados por coincidencia
    sorted_conditions = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
    top_code, top_pct = sorted_conditions[0]

    # Determinar condición resultante
    if has_alarms:
        final_code = "D5" # Signos de alarma
    elif top_pct >= 40.0:
        final_code = top_code
    else:
        final_code = "D6" # Resultado no concluyente

    rule_trace.append(f"\n📊 [RESULTADO FINAL] Diagnóstico principal asignado: {CONDITIONS[final_code]['name']} ({top_pct}% coincidencia relativa)")

    return {
        "final_code": final_code,
        "condition_details": CONDITIONS[final_code],
        "has_alarms": has_alarms,
        "alarm_triggers": alarm_triggers,
        "percentages": percentages,
        "sorted_ranking": [(code, CONDITIONS[code]["name"], pct) for code, pct in sorted_conditions],
        "rule_trace": "\n".join(rule_trace),
        "reasons": {
            "D1": d1_match_reasons,
            "D2": d2_match_reasons,
            "D3": d3_match_reasons,
            "D4": d4_match_reasons
        }
    }
