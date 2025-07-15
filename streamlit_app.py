import streamlit as st
import math

# --- Source Definitions ---
FUENTE_ENDESA_NRZ103_PG69_CONTRATACION = "Endesa Guía NRZ103, Pág. 69, 'POTENCIAS A CONTRATAR'"
FUENTE_ENDESA_NRZ103_PG54_IGM_REGLA = "Endesa Guía NRZ103, Pág. 54, 'Unidad IGM'"
FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS = "Endesa Guía NRZ103, Pág. 21, 'Tipos CGP'"
FUENTE_UF_TABLA = "Tabla Unión Fenosa (Proporcionada por Usuario)"
FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2 = "Unión Fenosa ES.0100.ES.RE.EIC, Pág. 14, 'Tabla 2 CGP'"
FUENTE_IBERDROLA_MT_PG17_TABLA1 = "Iberdrola MT 2.80.12, Pág. 17, 'Tabla 1'"
FUENTE_IBERDROLA_NI_PG5_TABLA1 = "Iberdrola NI 76.50.01, Pág. 5, 'Tabla 1'"
FUENTE_IBERDROLA_MT_PG19_IGM_REGLA = "Iberdrola MT 2.80.12, Pág. 19, 'Unidad IGM'"
FUENTE_GUIA_BT_14_PG9_TABLA1 = "GUÍA - BT-14, Pág. 9, 'Tabla 1'"
FUENTE_GUIA_BT_15_PG56_TABLA14 = "GUÍA - BT-15, Pág. 56, 'Tabla 14 PE'"
FUENTE_GENERICO_CABLE = "Tabla General de Calibres de Cable"

# Import data from your separate files
from endesa_data import endesa_contracted_power_data, get_endesa_igm_capacity, get_endesa_cgp_type
from iberdrola_data import iberdrola_ide_table, get_iberdrola_cgp_type
from union_fenosa_data import ufd_table, get_uf_cgp_type_and_fuse
from shared_data import guia_bt_14_table_1, generic_cable_diameter_data

# --- Helper Functions ---
def find_data(lookup_value, data_table, lookup_key='power_kw'):
    """
    Finds the appropriate row in a data table based on a lookup value.
    Can search by power ('power_kw') or by current ('conductor_amp_rating').
    """
    for row in data_table:
        if lookup_key in row and row[lookup_key]["valor"] >= lookup_value:
            return row
            
    return None
    
def get_iberdrola_igm_capacity(power_kw):
    """
    Determines the IGM capacity for Iberdrola and cites the correct source.
    """    
    fuente_iberdrola = "Iberdrola MT 2.80.12, Pág. 19, 'Unidad IGM'"
    if power_kw <= 90:
        return {"valor": "160 A", "fuente": fuente_iberdrola}
    elif power_kw <= 150:
        return {"valor": "250 A", "fuente": fuente_iberdrola}
    else:
        return {"valor": "Consultar i-DE (>250A)", "fuente": fuente_iberdrola}

def find_guia_bt_14_tube_diameter_by_sections(phase_mm2):
    """
    Finds the tube diameter from GUIA-BT-14 based on ONLY the phase conductor section.
    This is now more flexible and will work for Endesa's unique neutral wire rule.
    """
    if not isinstance(phase_mm2, (int, float)):
        return "N/A", "Sección de fase no válida"

    for row in guia_bt_14_table_1:
        if row.get("phase_mm2_cu") and row["phase_mm2_cu"]["valor"] >= phase_mm2:
            return row["tube_dia_mm"]["valor"], row["tube_dia_mm"]["fuente"]
        if row.get("phase_mm2_al") and row["phase_mm2_al"]["valor"] >= phase_mm2:
            return row["tube_dia_mm"]["valor"], row["tube_dia_mm"]["fuente"]
    
    if guia_bt_14_table_1:
        return guia_bt_14_table_1[-1]["tube_dia_mm"]["valor"], "Sección excede la tabla; usando el valor más grande."
    return "N/A", "No se encontraron datos aplicables."

def get_guia_bt_15_ground_size_by_phase(phase_mm2_ref):
    if not isinstance(phase_mm2_ref, (int, float)): return "N/A"
    if phase_mm2_ref <= 16: return phase_mm2_ref
    elif phase_mm2_ref <= 35: return 16
    else: return max(16, math.ceil(phase_mm2_ref / 2))

def calculate_current(power_kw, voltage_v, phase_number, power_factor):
    if voltage_v == 0 or power_factor == 0: return 0
    power_w = power_kw * 1000
    if phase_number == 3: return power_w / (math.sqrt(3) * voltage_v * power_factor)
    elif phase_number == 1: return power_w / (voltage_v * power_factor)
    return 0

# --- App Body ---
st.image("Logo_ASEPEYO.png", width=300)
st.title("Generador de Guía de Instalaciones Eléctricas")
st.markdown("Genere requisitos eléctricos detallados según las normas de las compañías distribuidoras.")

# --- Input Section ---
st.header("Parámetros de Entrada")
col1, col2 = st.columns(2)
with col1:
    company = st.selectbox("Seleccione Compañía Distribuidora", options=["Endesa", "Iberdrola", "Unión Fenosa"], index=0)
    power_kw = st.number_input("Potencia Máxima Contratada (kW)", min_value=0.0, value=20.0, step=1.0)
    voltage_v = st.number_input("Tensión Nominal de Red (V)", min_value=0.0, value=400.0, step=1.0)
with col2:
    phase_number = st.selectbox("Número de Fases", options=[1, 3], index=1)
    load_factor = st.slider("Factor de Carga (Factor de Potencia)", 0.8, 1.0, 0.9, 0.01)
    voltage_drop_limit = st.slider("Límite de Caída de Tensión (%)", 0.5, 5.0, 0.5, 0.1)

st.info("También puede introducir directamente la corriente de diseño si la conoce.")
input_design_current_a = st.number_input("Corriente de Diseño Calculada (A) (Opcional)", min_value=0.0, value=0.0, step=1.0)

# --- Calculation & Logic ---
st.header("Requisitos Generados")

if input_design_current_a > 0:
    calculated_current = input_design_current_a
    current_source_note = "Corriente de Diseño proporcionada."
    power_kw_for_lookup = (calculated_current * voltage_v * math.sqrt(3) * load_factor) / 1000 if phase_number == 3 else (calculated_current * voltage_v * load_factor) / 1000
else:
    calculated_current = calculate_current(power_kw, voltage_v, phase_number, load_factor)
    current_source_note = f"Calculada (Basada en {power_kw} kW)."
    power_kw_for_lookup = power_kw

st.write(f"Corriente de Diseño (I_B): **{calculated_current:.2f} A** ({current_source_note})")

# --- Data Lookup & Display Logic ---
selected_company_data = None
# This line is moved up to ensure it's always available
uf_ref_data_for_ground = find_data(power_kw_for_lookup, ufd_table)

if company == "Endesa":
    selected_company_data = find_data(power_kw_for_lookup, endesa_contracted_power_data)
elif company == "Unión Fenosa":
    selected_company_data = find_data(power_kw_for_lookup, ufd_table)
elif company == "Iberdrola":
    if input_design_current_a > 0:
        selected_company_data = find_data(calculated_current, iberdrola_ide_table, lookup_key='conductor_amp_rating')
    else:
        selected_company_data = find_data(power_kw_for_lookup, iberdrola_ide_table)

if selected_company_data:
    display_basis = f"{calculated_current:.2f} A" if input_design_current_a > 0 else f"{power_kw:.2f} kW"
    st.subheader(f"Requisitos para {company} (Basado en {display_basis})")

    # This dictionary will collect all our sources
    fuentes_utilizadas = {}

    # --- Cable Sections ---
    st.markdown("#### Secciones de Cables (mm²)")
    phase_mm2_info, neutral_mm2_info, ground_mm2_info = {}, {}, {}
    
    if company == "Endesa":
        required_nom_int_info = selected_company_data.get('nominal_protection_current_a', {})
        required_nom_int_val = required_nom_int_info.get('valor')
        fuentes_utilizadas["Corriente Nominal de Protección"] = required_nom_int_info.get('fuente')
        
        found_cable = next((c for c in generic_cable_diameter_data if c["three_phase_amps"]["valor"] >= required_nom_int_val), generic_cable_diameter_data[-1])
        phase_mm2_info = found_cable.get('area_mm2', {})
        fuentes_utilizadas["Sección de Fase"] = "Tabla Genérica de Cables (basado en Corriente de Protección)"
        
        neutral_mm2_info = {"valor": phase_mm2_info.get('valor'), "fuente": "Endesa Guía NRZ103, Pág. 23 (Regla: Neutro = Fase)"}
        fuentes_utilizadas["Sección de Neutro"] = neutral_mm2_info.get('fuente')

        ground_mm2_info = {"valor": get_guia_bt_15_ground_size_by_phase(phase_mm2_info.get('valor')), "fuente": "GUÍA - BT-15, Pág. 56, 'Tabla 14 PE'"}
        fuentes_utilizadas["Sección de Tierra"] = ground_mm2_info.get('fuente')
        
    else: # Logic for Iberdrola and Unión Fenosa
        phase_mm2_info = selected_company_data.get('phase_mm2', {})
        neutral_mm2_info = selected_company_data.get('neutral_mm2', {})
        ground_mm2_info = selected_company_data.get('ground_mm2', {})
        fuentes_utilizadas["Sección de Fase"] = phase_mm2_info.get('fuente')
        fuentes_utilizadas["Sección de Neutro"] = neutral_mm2_info.get('fuente')
        fuentes_utilizadas["Sección de Tierra"] = ground_mm2_info.get('fuente')

    st.write(f"- **Sección de Cable de Fase:** {phase_mm2_info.get('valor', 'N/A')} mm²")
    st.write(f"- **Sección de Neutro:** {neutral_mm2_info.get('valor', 'N/A')} mm²")
    st.write(f"- **Sección de Conductor de Protección (Tierra):** {ground_mm2_info.get('valor', 'N/A')} mm²")
    
    # --- Installation Details ---
    st.markdown("#### Detalles de Instalación")
    tube_dia_mm_info = selected_company_data.get('tube_dia_mm', {})
    fuentes_utilizadas["Diámetro Mínimo del Tubo"] = tube_dia_mm_info.get('fuente')
    st.write(f"- **Diámetro Mínimo del Tubo:** {tube_dia_mm_info.get('valor', 'N/A')} mm")

    max_len_0_5_info = selected_company_data.get('max_len_0_5', {})
    fuentes_utilizadas["Longitud Máxima"] = max_len_0_5_info.get('fuente')
    if max_len_0_5_info.get('valor', 'N/A') != 'N/A':
        st.write(f"- **Longitud Máxima @ 0.5% Caída de Tensión:** {max_len_0_5_info.get('valor')} m")
        st.write(f"- **Longitud Máxima @ 1.0% Caída de Tensión:** {selected_company_data.get('max_len_1', {}).get('valor')} m")

    # --- Electrical Devices ---
    st.markdown("#### Dispositivos Eléctricos y Capacidades")
    if company == "Endesa":
        igm_info = get_endesa_igm_capacity(power_kw_for_lookup)
        fuse_info = selected_company_data.get('nominal_protection_current_a', {})
        cgp_info = get_endesa_cgp_type(fuse_info.get('valor'))
        
        fuentes_utilizadas["Capacidad del IGM"] = igm_info.get('fuente')
        fuentes_utilizadas["Tipo de CGP"] = cgp_info[1]
        fuentes_utilizadas["Capacidad de Fusible"] = fuse_info.get('fuente')
        
        st.write(f"- **Capacidad del IGM:** {igm_info.get('valor')}")
        st.write(f"- **Tipo de CGP:** {cgp_info[0]}")
        st.write(f"- **Capacidad de Fusible/Interruptor:** {fuse_info.get('valor')} A")

    elif company == "Iberdrola":
        igm_info = get_iberdrola_igm_capacity(power_kw_for_lookup)
        fuse_info = selected_company_data.get('conductor_amp_rating', {})
        cgp_info = get_iberdrola_cgp_type(fuse_info.get('valor'))
        
        fuentes_utilizadas["Capacidad del IGM"] = igm_info.get('fuente')
        fuentes_utilizadas["Tipo de CGP"] = cgp_info[1]
        fuentes_utilizadas["Capacidad de Fusible"] = fuse_info.get('fuente')
        
        st.write(f"- **Capacidad del IGM:** {igm_info.get('valor')}")
        st.write(f"- **Tipo de CGP:** {cgp_info[0]}")
        if "CGP-1-100/BUC" in cgp_info[0]:
            st.info("*(Nota: El tipo CGP-1-100/BUC puede estar restringido a mantenimiento.)*")
        st.write(f"- **Capacidad de Fusible/Interruptor:** {fuse_info.get('valor')} A")

    elif company == "Unión Fenosa":
        cgp_type, fuse_cap, cgp_source = get_uf_cgp_type_and_fuse(calculated_current)
        fuentes_utilizadas["Tipo de CGP"] = cgp_source
        fuentes_utilizadas["Capacidad de Fusible"] = cgp_source

        st.write(f"- **Tipo de CGP:** {cgp_type}")
        st.write(f"- **Capacidad de Fusible/Interruptor:** {fuse_cap} A")
        st.write("- **Capacidad del IGM:** N/A (Consulte la documentación de Unión Fenosa)")

    # --- Display All Collected Sources ---
    st.markdown("---")
    st.markdown("#### Fuentes de Datos Utilizadas para esta Recomendación")
    # Clean up the set from potential None or N/A values before displaying
    fuentes_validas = {key: value for key, value in fuentes_utilizadas.items() if value and value != "N/A"}
    if fuentes_validas:
        for key, value in fuentes_validas.items():
            st.write(f"- **{key}:** *{value}*")
    else:
        st.write("No se utilizaron fuentes específicas para esta recomendación.")

else:
    st.warning(f"No se encontró una entrada en la tabla de {company} para la potencia o corriente especificada. El valor puede exceder los límites de la tabla. Mostrando recomendaciones genéricas.")
    # ... (Your existing generic fallback code) ...

# --- Disclaimer ---
st.warning(
    "**Descargo de Responsabilidad:** Esta herramienta es una guía informativa y Siempre verifique los requisitos con la Refrencia abajo"
)
# --- References ---

st.markdown("""
---
### Documentos de Referencia:
* **Endesa:** [Guía de Interpretación NRZ103, Edición 6.1, 03-2024]
* **Unión Fenosa:** [Especificaciones Particulares para Instalaciones de Conexión ES.0100.ES.RE.EIC, Edición: 5, 08/09/2011]
* **Iberdrola (i-DE):** [Manual Técnico de Distribución MT 2.80.12, Edición 05, Mayo 2019]
* **Iberdrola (i-DE) Tipos de CGP:** [NORMA NI 76.50.01, Edición 6a, Julio 2010]
* **Guías Técnicas de Aplicación (Ministerio para la Transición Ecológica y el Reto Demográfico):**
    * [GUÍA-BT-10: Previsión de Cargas, Edición: sep 03, Revisión: 1]
    * [GUÍA-BT-12: Esquemas, Edición: sep 03, Revisión: 1]
    * [GUÍA-BT-13: Cajas Generales de Protección, Edición: sep 03, Revisión: 1]
    * [GUÍA-BT-14: Línea General de Alimentación, Edición: sep 03, Revisión: 1]
    * [GUÍA-BT-15: Derivaciones Individuales, Edición: sep 03, Revisión: 1]
    * [GUÍA-BT-16: Contadores: Ubicación y Sistemas de Instalación, Edición: sep 03, Revisión: 1]
""")

