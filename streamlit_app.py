# main_app.py
import streamlit as st
import math

# Import data and functions from the new modules
from endesa_data import endesa_contracted_power_data, get_endesa_igm_capacity, get_endesa_cgp_type
from iberdrola_data import iberdrola_ide_table, get_iberdrola_cgp_type
from union_fenosa_data import ufd_table, get_uf_cgp_type_and_fuse
from shared_data import guia_bt_14_table_1, generic_cable_diameter_data

# --- Helper Functions (can also be moved to a 'utils.py' file for further cleanup) ---
def find_data_by_power(power_kw, data_table):
    for row in data_table:
        if row["power_kw"]["valor"] >= power_kw:
            return row
    return data_table[-1] if data_table else None

def find_guia_bt_14_tube_diameter_by_sections(phase_mm2, neutral_mm2):
    for row in guia_bt_14_table_1:
        if row.get("phase_mm2_cu") and row["phase_mm2_cu"]["valor"] == phase_mm2 and \
           row.get("neutral_mm2") and row["neutral_mm2"]["valor"] == neutral_mm2:
            return row["tube_dia_mm"]["valor"], row["tube_dia_mm"]["fuente"]
    return "N/A", guia_bt_14_table_1[0]["tube_dia_mm"]["fuente"]

def get_guia_bt_15_ground_size_by_phase(phase_mm2_ref):
    if not isinstance(phase_mm2_ref, (int, float)): return "N/A"
    if phase_mm2_ref <= 16: return phase_mm2_ref
    elif phase_mm2_ref <= 35: return 16
    else: return max(16, math.ceil(phase_mm2_ref / 2))

def get_generic_diameter_from_area(area_mm2):
    if not isinstance(area_mm2, (int, float)): return {"valor": "N/A"}
    for cable in generic_cable_diameter_data:
        if cable["area_mm2"]["valor"] == area_mm2:
            return {"valor": cable["diameter_mm"]["valor"], "fuente": cable["diameter_mm"]["fuente"]}
    return {"valor": "N/A"}

def calculate_current(power_kw, voltage_v, phase_number, power_factor):
    if voltage_v == 0 or power_factor == 0: return 0
    power_w = power_kw * 1000
    if phase_number == 3: return power_w / (math.sqrt(3) * voltage_v * power_factor)
    elif phase_number == 1: return power_w / (voltage_v * power_factor)
    return 0

# --- Streamlit App ---
st.set_page_config(page_title="Generador de Guía de Instalaciones Eléctricas", layout="centered")

st.markdown("""
<style>
.main .block-container {
    border: 3px solid #4682B4; padding: 1.5rem; border-radius: 15px;
}
div[data-testid="stSlider"] div[role="slider"] + div > div {
    background-color: #4682B4;
}
div[data-testid="stSlider"] div[role="slider"] {
    background-color: #1E90FF;
}
div[data-testid="stSlider"] div[role="slider"]:hover {
    background-color: #4169E1;
}
</style>
""", unsafe_allow_html=True)

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
st.header("Requisitos Generados")

# Determine which current to use
if input_design_current_a > 0:
    calculated_current = input_design_current_a
    current_source_note = "Corriente de Diseño proporcionada."
else:
    calculated_current = calculate_current(power_kw, voltage_v, phase_number, load_factor)
    current_source_note = f"Calculada (Basada en {power_kw} kW)."
st.write(f"Corriente de Diseño (I_B): **{calculated_current:.2f} A** ({current_source_note})")

# Logic to select and display data
use_company_power_tables = not (power_kw == 0.0 and input_design_current_a > 0)
if not use_company_power_tables:
    st.warning("Potencia contratada es 0 kW. Los resultados se basarán en la corriente de diseño y datos genéricos.")

selected_company_data = None
if use_company_power_tables:
    if company == "Endesa":
        selected_company_data = find_data_by_power(power_kw, endesa_contracted_power_data)
    elif company == "Unión Fenosa":
        selected_company_data = find_data_by_power(power_kw, ufd_table)
    elif company == "Iberdrola":
        selected_company_data = find_data_by_power(power_kw, iberdrola_ide_table)

if selected_company_data and use_company_power_tables:
    st.subheader(f"Requisitos para {company} (Basado en {power_kw} kW)")
    # (The rest of the display logic from your original file goes here)
    # This part is simplified for brevity but you would include all your `st.write` calls
    # for cable sections, installation details, and electrical devices.
    st.success("Datos específicos de la compañía cargados y mostrados.") # Placeholder
else:
    st.warning(f"No se encontraron datos para {power_kw} kW. Mostrando recomendaciones genéricas.")
    # (The generic fallback logic from your original file goes here)
    st.info("Recomendaciones genéricas mostradas.") # Placeholder

# --- Footer with References ---
st.markdown("---")
st.header("Documentos de Referencia")
# (Your reference markdown section)
