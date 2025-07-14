import streamlit as st
import math

# Import data and functions from the new modules
from endesa_data import endesa_contracted_power_data, get_endesa_igm_capacity, get_endesa_cgp_type
from iberdrola_data import iberdrola_ide_table, get_iberdrola_cgp_type
from union_fenosa_data import ufd_table, get_uf_cgp_type_and_fuse
from shared_data import guia_bt_14_table_1, generic_cable_diameter_data

# --- Helper Functions ---
def find_data_by_power(lookup_value, data_table, lookup_key='power_kw'):
    """
    Finds the appropriate row in a data table based on a lookup value.
    Can search by power ('power_kw') or current ('conductor_amp_rating').
    """
    for row in data_table:
        
# Check if the key exists in the row to avoid errors
        if lookup_key in row and row[lookup_key]["valor"] >= lookup_value:
            return row
    return data_table[-1] if data_table else None

def find_guia_bt_14_tube_diameter_by_sections(phase_mm2, neutral_mm2):
    for row in guia_bt_14_table_1:
        if row.get("phase_mm2_cu") and row["phase_mm2_cu"]["valor"] == phase_mm2 and \
           row.get("neutral_mm2") and row["neutral_mm2"]["valor"] == neutral_mm2:
            return row["tube_dia_mm"]["valor"], row["tube_dia_mm"]["fuente"]
    return "N/A", guia_bt_14_table_1[0]["tube_dia_mm"]["fuente"] if guia_bt_14_table_1 else "N/A"

def get_guia_bt_15_ground_size_by_phase(phase_mm2_ref):
    if not isinstance(phase_mm2_ref, (int, float)): return "N/A"
    if phase_mm2_ref <= 16: return phase_mm2_ref
    elif phase_mm2_ref <= 35: return 16
    else: return max(16, math.ceil(phase_mm2_ref / 2))

def get_generic_diameter_from_area(area_mm2):
    if not isinstance(area_mm2, (int, float)): return {"valor": "N/A", "fuente": "N/A"}
    for cable in generic_cable_diameter_data:
        if cable["area_mm2"]["valor"] == area_mm2:
            return {"valor": cable["diameter_mm"]["valor"], "fuente": cable["diameter_mm"]["fuente"]}
    return {"valor": "N/A", "fuente": "N/A"}

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
    power_kw = st.number_input("Potencia Máxima Contratada (kW)", min_value=0.0, value=100.0, step=1.0)
    voltage_v = st.number_input("Tensión Nominal de Red (V)", min_value=0.0, value=400.0, step=1.0)
with col2:
    phase_number = st.selectbox("Número de Fases", options=[1, 3], index=1)
    load_factor = st.slider("Factor de Carga (Factor de Potencia)", 0.8, 1.0, 0.9, 0.01)
    voltage_drop_limit = st.slider("Límite de Caída de Tensión (%)", 0.5, 5.0, 0.5, 0.1)

st.info("También puede introducir directamente la corriente de diseño si la conoce.")
input_design_current_a = st.number_input("Corriente de Diseño Calculada (A) (Opcional)", 0.0, value=0.0, step=1.0)

# --- Calculation & Logic ---
# --- Calculation & Logic ---
st.header("Requisitos Generados")

# This section is now updated to handle custom current correctly.
# First, determine the final current to be used for all lookups.
if input_design_current_a > 0:
    calculated_current = input_design_current_a
    current_source_note = "Corriente de Diseño proporcionada."
    # Reverse-calculate an approximate power to use for lookups in power-based tables.
    power_kw_for_lookup = (calculated_current * voltage_v * math.sqrt(phase_number) * load_factor) / 1000
else:
    calculated_current = calculate_current(power_kw, voltage_v, phase_number, load_factor)
    current_source_note = f"Calculada (Basada en {power_kw} kW)."
    power_kw_for_lookup = power_kw

st.write(f"Corriente de Diseño (I_B): **{calculated_current:.2f} A** ({current_source_note})")

# --- Data Lookup Logic ---
selected_company_data = None
if company == "Endesa":
    # Endesa's table is based on power, so we use the calculated or approximate power.
    selected_company_data = find_data_by_power(power_kw_for_lookup, endesa_contracted_power_data)
    # Get a reference from the UF table for the ground conductor size lookup.
    uf_ref_data_for_ground = find_data_by_power(power_kw_for_lookup, ufd_table)
elif company == "Unión Fenosa":
    # UF's table is also based on power.
    selected_company_data = find_data_by_power(power_kw_for_lookup, ufd_table)
elif company == "Iberdrola":
    # Iberdrola's table is special; we can look up by power OR current.
    if input_design_current_a > 0:
        # If custom current is given, use it to search the 'conductor_amp_rating' column.
        selected_company_data = find_data_by_power(calculated_current, iberdrola_ide_table, lookup_key='conductor_amp_rating')
    else:
        # Otherwise, use power.
        selected_company_data = find_data_by_power(power_kw_for_lookup, iberdrola_ide_table)

# --- Display Logic ---
if selected_company_data:
    # This subheader now correctly reflects what the data is based on.
    display_basis = f"{calculated_current:.2f} A de Corriente de Diseño" if input_design_current_a > 0 else f"{power_kw} kW de Potencia Contratada"
    st.subheader(f"Requisitos para {company} (Basado en {display_basis})")
    
    # (The rest of your display logic for Cable Sections, Installation Details, etc.
    # remains exactly the same as before and should follow here.)
    
    # --- Cable Sections ---
    st.markdown("#### Secciones de Cables (mm²)")
else:
    st.warning(f"No se encontraron datos para los parámetros introducidos. Mostrando recomendaciones genéricas.")

if selected_company_data and use_company_power_tables:
    st.subheader(f"Requisitos para {company} (Basado en {power_kw} kW de Potencia Contratada)")
    
    # --- Cable Sections ---
    st.markdown("#### Secciones de Cables (mm²)")
    phase_mm2, neutral_mm2, ground_mm2 = {"valor": "N/A"}, {"valor": "N/A"}, {"valor": "N/A"}
    
    if company == "Endesa":
        required_nom_int_val = selected_company_data['nominal_protection_current_a']['valor']
        found_cable = next((c for c in generic_cable_diameter_data if c["three_phase_amps"]["valor"] >= required_nom_int_val), None)
        if found_cable:
            phase_mm2 = found_cable['area_mm2']
            neutral_mm2 = {"valor": phase_mm2['valor'], "fuente": "Endesa NRZ103, Pág. 23"}
            if uf_ref_data_for_ground:
                ground_mm2 = uf_ref_data_for_ground.get('ground_mm2', {"valor": "N/A"})
            else:
                ground_mm2 = {"valor": get_guia_bt_15_ground_size_by_phase(phase_mm2['valor'])}
    else:
        phase_mm2 = selected_company_data.get('phase_mm2', {"valor": "N/A"})
        neutral_mm2 = selected_company_data.get('neutral_mm2', {"valor": "N/A"})
        ground_mm2 = selected_company_data.get('ground_mm2', {"valor": "N/A"})

    st.write(f"- **Sección de Cable de Fase:** {phase_mm2.get('valor', 'N/A')} mm²")
    st.write(f"- **Sección de Neutro:** {neutral_mm2.get('valor', 'N/A')} mm²")
    st.write(f"- **Sección de Conductor de Protección (Tierra):** {ground_mm2.get('valor', 'N/A')} mm²")
    
    # --- Installation Details ---
    st.markdown("#### Detalles de Instalación")
    if company == "Endesa":
        tube_dia_val, _ = find_guia_bt_14_tube_diameter_by_sections(phase_mm2.get('valor'), neutral_mm2.get('valor'))
        st.write(f"- **Diámetro Mínimo del Tubo:** {tube_dia_val} mm")
    else:
        st.write(f"- **Diámetro Mínimo del Tubo:** {selected_company_data.get('tube_dia_mm', {}).get('valor', 'N/A')} mm")

    max_len_0_5 = selected_company_data.get('max_len_0_5', {}).get('valor', 'N/A')
    max_len_1 = selected_company_data.get('max_len_1', {}).get('valor', 'N/A')
    if max_len_0_5 != 'N/A':
         st.write(f"- **Longitud Máxima @ 0.5% Caída de Tensión:** {max_len_0_5} m")
         st.write(f"- **Longitud Máxima @ 1.0% Caída de Tensión:** {max_len_1} m")

    # --- Electrical Devices ---
    st.markdown("#### Dispositivos Eléctricos y Capacidades")
    if company == "Endesa":
        igm_cap = get_endesa_igm_capacity(power_kw)
        cgp_type, _ = get_endesa_cgp_type(selected_company_data['nominal_protection_current_a']['valor'])
        fuse_cap = selected_company_data['nominal_protection_current_a']['valor']
        st.write(f"- **Capacidad del Interruptor General de Maniobra (IGM):** {igm_cap.get('valor')}")
        st.write(f"- **Tipo de CGP (Caja General de Protección):** {cgp_type}")
        st.write(f"- **Capacidad de Fusible/Interruptor Recomendada:** {fuse_cap} A")
    elif company == "Iberdrola":
        igm_cap = get_endesa_igm_capacity(power_kw) # Same rule as Endesa
        cgp_type, _ = get_iberdrola_cgp_type(selected_company_data['conductor_amp_rating']['valor'])
        fuse_cap = selected_company_data['conductor_amp_rating']['valor']
        st.write(f"- **Capacidad del Interruptor General de Maniobra (IGM):** {igm_cap.get('valor')}")
        st.write(f"- **Tipo de CGP (Caja General de Protección):** {cgp_type}")
        st.write(f"- **Capacidad de Fusible/Interruptor Recomendada:** {fuse_cap} A")
    elif company == "Unión Fenosa":
        cgp_type, fuse_cap, _ = get_uf_cgp_type_and_fuse(calculated_current)
        st.write(f"- **Tipo de CGP (Caja General de Protección):** {cgp_type}")
        st.write(f"- **Capacidad de Fusible/Interruptor Recomendada:** {fuse_cap} A")
        st.write("- **Interruptor General de Maniobra (IGM) Capacity:** N/A (Consulte la documentación de Unión Fenosa)")

else:
    st.warning(f"No se encontraron datos para {power_kw} kW. Mostrando recomendaciones genéricas.")
    st.markdown("#### Recomendación Genérica de Cable (Respaldo)")
    found_generic_cable = next((c for c in generic_cable_diameter_data if c["three_phase_amps"]["valor"] >= calculated_current), None)
    if found_generic_cable:
        st.write(f"- **Área de Sección Transversal de Cable Requerida (aprox.):** {found_generic_cable['area_mm2']['valor']} mm²")
        st.write(f"- **Diámetro Total Aproximado del Cable:** {found_generic_cable['diameter_mm']['valor']} mm")
    else:
        st.error("No se encontró un cable genérico adecuado para la corriente calculada.")
    st.markdown("#### Dispositivos Eléctricos y Capacidades (Genéricos)")
    st.write(f"- **Capacidad de Fusible/Interruptor Recomendada (Mín.):** Aprox. {calculated_current * 1.25:.2f} A (Regla general de seguridad)")
    st.write("- **Tipo de CGP y Capacidad IGM:** N/A (Consulte al distribuidor)")

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
