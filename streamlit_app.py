import streamlit as st
import math

# --- Source Definitions ---
FUENTE_ENDESA_NRZ103_PG54_IGM_REGLA = "Endesa Guía NRZ103, Pág. 54, 'Unidad IGM'"
FUENTE_IBERDROLA_MT_PG19_IGM_REGLA = "Iberdrola MT 2.80.12, Pág. 19, 'Unidad IGM'"
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
   
    if not isinstance(phase_mm2, (int, float)):
        return "N/A", "Sección de fase no válida"

    for row in guia_bt_14_table_1:
        if row.get("phase_mm2_cu") and row["phase_mm2_cu"]["valor"] >= phase_mm2:
            return row["tube_dia_mm"]["valor"], row["tube_dia_mm"]["fuente"]
        if row.get("phase_mm2_al") and row["phase_mm2_al"]["valor"] >= phase_mm2:
            return guia_bt_14_table_1[-1]["tube_dia_mm"]["valor"], "Sección excede la tabla; usando el valor más grande."
    
    return "N/A", "No se encontraron datos aplicables."
            
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
st.image("Logo_ASEPEYO.png", width=250)
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


    # This dictionary will collect all our sources
fuentes_utilizadas = {}


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

 # Taking data for the scheme 
    # 1. First, we gather all the specifications needed for the diagram

    acometida_spec = "Conexión a Red BT"

    if company == "Endesa":
        required_nom_int_info = selected_company_data.get('nominal_protection_current_a', {})
        required_nom_int_val = required_nom_int_info.get('valor')
        fuentes_utilizadas["Corriente Nominal de Protección"] = required_nom_int_info.get('fuente')
        found_cable = next((c for c in generic_cable_diameter_data if c["three_phase_amps"]["valor"] >= required_nom_int_val), generic_cable_diameter_data[-1])
        phase_mm2 = found_cable['area_mm2']['valor'] if found_cable else "N/A"
        neutral_mm2 = phase_mm2
        ground_mm2 = get_guia_bt_15_ground_size_by_phase(phase_mm2)
        cgp_spec = f"Tipo: {get_endesa_cgp_type(required_nom_int_val)[0]}<br>Fusible: {required_nom_int_val} A"
        igm_spec = f"Capacidad: {get_endesa_igm_capacity(power_kw_for_lookup).get('valor')}"
        lga_spec = f"Fase: {phase_mm2} mm²<br>Neutro: {neutral_mm2} mm²<br>Tierra: {ground_mm2} mm²"
        tubo_spec = f"Diámetro: {find_guia_bt_14_tube_diameter_by_sections(phase_mm2)[0]} mm"
    elif company == "Iberdrola" or company == "Unión Fenosa":
        phase_mm2 = selected_company_data.get('phase_mm2', {}).get('valor', 'N/A')
        neutral_mm2 = selected_company_data.get('neutral_mm2', {}).get('valor', 'N/A')
        ground_mm2 = selected_company_data.get('ground_mm2', {}).get('valor', 'N/A')
        lga_spec = f"Fase: {phase_mm2} mm²<br>Neutro: {neutral_mm2} mm²<br>Tierra: {ground_mm2} mm²"
        tubo_spec = f"Diámetro: {selected_company_data.get('tube_dia_mm', {}).get('valor', 'N/A')} mm"

        if company == "Iberdrola":
            fuse_val = selected_company_data.get('conductor_amp_rating', {}).get('valor', 'N/A')
            cgp_spec = f"Tipo: {get_iberdrola_cgp_type(fuse_val)[0]}<br>Fusible: {fuse_val} A"
            igm_spec = f"Capacidad: {get_iberdrola_igm_capacity(power_kw_for_lookup).get('valor')}"
        elif company == "Unión Fenosa":
            cgp_type, fuse_cap, _ = get_uf_cgp_type_and_fuse(calculated_current)
            cgp_spec = f"Tipo: {cgp_type}<br>Fusible: {fuse_cap} A"
            igm_spec = "N/A"



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

        st.info("*(Nota: La sección del conductor de protección (tierra), Endesa no lo especifica directamente, este reccomendation es de GUÍA-BT-13.")


    
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

    if company == "Endesa":
        # Get the phase_mm2 value again to ensure it's in scope
        phase_mm2 = phase_mm2_info.get('valor', 'N/A')
        tube_dia_val, tube_fuente = find_guia_bt_14_tube_diameter_by_sections(phase_mm2)
    else:
        # For other companies, we get it directly from their data table
        tube_info = selected_company_data.get('tube_dia_mm', {})
        tube_dia_val = tube_info.get('valor', 'N/A')
        tube_fuente = tube_info.get('fuente')

    st.write(f"- **Diámetro Mínimo del Tubo:** {tube_dia_val} mm")
    fuentes_utilizadas["Diámetro Mínimo del Tubo"] = tube_fuente

    max_len_0_5_info = selected_company_data.get('max_len_0_5', {})
    fuentes_utilizadas["Longitud Máxima"] = max_len_0_5_info.get('fuente')
    if max_len_0_5_info.get('valor', 'N/A') != 'N/A':
        st.write(f"- **Longitud Máxima @ 0.5% Caída de Tensión:** {max_len_0_5_info.get('valor')} m")
        st.write(f"- **Longitud Máxima @ 1.0% Caída de Tensión:** {selected_company_data.get('max_len_1', {}).get('valor')} m")
# 
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
        
        
        st.header("Requisitos Generados")

        st.markdown("""---""")


    # --- Visual Scheme Section ---
    diagram_html = f"""
    <div class="responsibility-container">
    </div>
    <style>
        .responsibility-container {{
            display: flex;
            align-items: flex-start; /* Aligns zones to the top */
            justify-content: center;
            gap: 10px;
            font-family: sans-serif;
            padding: 10px 0;
            width: 100%;
        }}
        .zone {{
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid;
        }}
        .zone-title {{
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 15px;
            border-bottom: 2px solid;
            padding-bottom: 8px;
        }}
        .flow-boxes-in-zone {{
            display: flex;
            align-items: center;
            justify-content: center;
            flex-wrap: nowrap; /* Ensures boxes stay in one line */
            gap: 10px;
            min-height: 80px; /* Give space for content */
        }}
        .flow-box {{
            background-color: #FFFFFF;
            border: 1px solid #D0D7DE;
            border-radius: 8px;
            padding: 12px;
            text-align: center;
            min-width: 130px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        }}
        .flow-box h5 {{ margin: 0 0 5px 0; color: #000; }}
        .flow-box p {{ margin: 0; font-size: 0.9em; color: #333; line-height: 1.4;}}
        .flow-arrow {{ font-size: 2em; color: #586069; margin: auto 15px; }}
        
        /* Zone Colors */
        .zone.yellow {{ background-color: #FFFBEA; border-color: #FDCF47; }}
        .zone.yellow .zone-title {{ color: #B54A09; border-color: #FDCF47; }}
        .zone.blue {{ background-color: #EBF5FF; border-color: #6CB4EE; }}
        .zone.blue .zone-title {{ color: #00529B; border-color: #6CB4EE; }}
        .zone.green {{ background-color: #E6FFED; border-color: #54C176; }}
        .zone.green .zone-title {{ color: #1E7E34; border-color: #54C176; }}
    </style>
    <div class="responsibility-container">
        <div class="zone yellow">
            <div class="zone-title">Compañía</div>
            <div class="flow-boxes-in-zone">
                <div class="flow-box"><h5>Acometida</h5><p>{tubo_spec} {lga_spec}</p></div>
            </div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="zone blue">
            <div class="zone-title">Común</div>
            <div class="flow-boxes-in-zone">
                <div class="flow-box"><h5>CGP</h5><p>{cgp_spec}</p></div>
            </div>
        </div>
        <div class="flow-arrow">→</div>
        <div class="zone green">
            <div class="zone-title">Usuario</div>
            <div class="flow-boxes-in-zone">
                <div class="flow-box"><h5>IGM</h5><p>{igm_spec}</p></div>
                <div class="flow-arrow">→</div>
                <div class="flow-box"><h5>LGA</h5><p>{lga_spec}</p></div>
                <div class="flow-arrow">→</div>
                <div class="flow-box"><h5>Tubo</h5><p>{tubo_spec}</p></div>
            </div>
        </div>
    </div>
    """
    st.markdown(diagram_html, unsafe_allow_html=True)
    st.markdown("""---""")

    
    # --- Display All Collected Sources ---
    st.markdown("#### Fuentes de Datos Utilizadas para esta Recomendación")
    fuentes_validas = {key: value for key, value in fuentes_utilizadas.items() if value and value != "N/A"}
    
    if fuentes_validas:
        for key, value in fuentes_validas.items():
            st.write(f"- **{key}:** *{value}*")
    else:
        st.write("No se utilizaron fuentes específicas para esta recomendación.")
else:
    st.warning(f"No se encontró una entrada en la tabla de {company} para la potencia o corriente especificada. El valor puede exceder los límites de la tabla. Mostrando recomendaciones genéricas.")
    
    found_generic_cable = find_data(calculated_current, generic_cable_diameter_data, lookup_key='three_phase_amps')
    if found_generic_cable:
        st.markdown("#### Recomendación Genérica de Cable (Respaldo)")
        st.write(f"- **Área de Sección Transversal de Cable Requerida (aprox.):** {found_generic_cable['area_mm2']['valor']} mm²")
    else:
        st.error("No se encontró un cable genérico adecuado para la corriente calculada.")


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

