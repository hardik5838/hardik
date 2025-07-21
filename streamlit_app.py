import streamlit as st
import math
from report_generator import get_report_download_link

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

acometida_diametro = "N/A"
acometida_fase = "N/A"
acometida_neutro = "N/A"
acometida_tierra = "N/A"
cgp_tipo = "N/A"
cgp_fusible = "N/A"
igm_capacidad = "N/A"
lga_fase = "N/A"
lga_neutro = "N/A"
lga_tierra = "N/A"
tubo_diametro = "N/A" 

if selected_company_data:
    display_basis = f"{calculated_current:.2f} A" if input_design_current_a > 0 else f"{power_kw:.2f} kW"
    st.subheader(f"Requisitos para {company} (Basado en {display_basis})")

 # Taking data for the scheme 

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

    # --- Update individual variables for HTML injection after all company-specific logic ---
    # Acometida/Tubo values
    acometida_diametro = tubo_spec.replace("Diámetro: ", "") 
    lga_parts = lga_spec.split("<br>")
    acometida_fase = lga_parts[0].replace("Fase: ", "") 
    acometida_neutro = lga_parts[1].replace("Neutro: ", "") 
    acometida_tierra = lga_parts[2].replace("Tierra: ", "") 

    # CGP values
    cgp_parts = cgp_spec.split("<br>")
    cgp_tipo = cgp_parts[0].replace("Tipo: ", "") 
    cgp_fusible = cgp_parts[1].replace("Fusible: ", "") 

    # IGM values
    igm_capacidad = igm_spec.replace("Capacidad: ", "") 

    # For LGA values in the diagram, reuse the extracted acometida_fase, etc.
    lga_fase = acometida_fase
    lga_neutro = acometida_neutro
    lga_tierra = acometida_tierra

    # For the final Tubo, reuse the extracted acometida_diametro
    tubo_diametro = acometida_diametro

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


# Define the HTML template as a plain string (NO 'f' prefix)
diagram_html_template ="""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagrama Eléctrico de Acometida</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom styles for SVG elements for better clarity */
        svg {{
            display: block;
            margin: auto;
            overflow: visible; /* Allow elements to extend slightly beyond viewBox if needed */
        }}
        .line {{
            stroke: black;
            stroke-width: 3; /* Thicker lines for better visibility */
            fill: none;
            stroke-linecap: round;
        }}
        .symbol-stroke {{
            stroke: black;
            stroke-width: 3; /* Thicker lines for better visibility */
            fill: none;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}
        .symbol-fill {{
            fill: black;
        }}
        .label {{
            font-family: 'Inter', sans-serif;
            font-size: 20px; /* Increased further for readability */
            fill: #333;
            font-weight: bold;
            text-anchor: middle; /* Center text by default */
        }}
        .value-label {{
            font-family: 'Inter', sans-serif;
            font-size: 16px; /* Increased further for readability */
            fill: #555;
            text-anchor: middle;
        }}
        .section-background {{
            stroke-dasharray: 5 5; /* Dashed border for sections */
            stroke: #6b7280; /* Gray-500 */
            stroke-width: 1;
            fill: none;
        }}
        /* Tooltip styles */
        .tooltip {{
            position: absolute;
            background-color: #333;
            color: #fff;
            padding: 10px 15px; /* Increased padding */
            border-radius: 8px; /* More rounded */
            font-family: 'Inter', sans-serif;
            font-size: 16px; /* Increased for readability */
            pointer-events: none; /* Allows mouse events to pass through to elements below */
            opacity: 0;
            transition: opacity 0.2s;
            z-index: 1000;
            white-space: nowrap; /* Keep text on one line if possible */
            box-shadow: 0 4px 8px rgba(0,0,0,0.3); /* More prominent shadow */
            text-align: left;
        }}
        .tooltip.visible {{
            opacity: 1;
        }}
        .tooltip-content p {{
            margin: 0;
            line-height: 1.5; /* Increased line height */
        }}
        .tooltip-content strong {{
            display: block;
            margin-bottom: 6px; /* More space */
            font-size: 18px; /* Increased for prominence */
        }}
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">
    <div class="bg-white rounded-lg shadow-xl p-6 md:p-8 max-w-5xl w-full">
        <h1 class="text-2xl md:text-3xl font-bold text-center text-gray-800 mb-6">Diagrama de Acometida Eléctrica</h1>

        <div class="flex flex-col items-center justify-center w-full relative">
            <svg viewBox="0 0 1744 368" class="w-full h-auto max-h-[368px]">
                <rect x="0" y="0" width="580" height="368" fill="#FFFBEA" rx="0" ry="0"/> <rect x="580" y="0" width="580" height="368" fill="#EBF5FF" rx="0" ry="0"/> <rect x="1160" y="0" width="584" height="368" fill="#E6FFED" rx="0" ry="0"/> <line x1="580" y1="0" x2="580" y2="368" class="section-background" />
                <line x1="1160" y1="0" x2="1160" y2="368" class="section-background" />

                <line x1="100" y1="100" x2="300" y2="100" class="line" />
                <text x="50" y="105" class="label">L1</text>
                <line x1="100" y1="140" x2="300" y2="140" class="line" />
                <text x="50" y="145" class="label">L2</text>
                <line x1="100" y1="180" x2="300" y2="180" class="line" />
                <text x="50" y="185" class="label">L3</text>
                <line x1="100" y1="220" x2="300" y2="220" class="line" />
                <text x="50" y="225" class="label">N</text>
                <line x1="100" y1="260" x2="300" y2="260" class="line" />
                <text x="50" y="265" class="label">T</text>

                <line x1="300" y1="100" x2="300" y2="260" class="line" />
                <text x="200" y="70" class="label" id="label-acometida">Acometida</text>

                <text x="200" y="290" class="value-label">Diámetro: {acometida_diametro}</text>
                <text x="200" y="305" class="value-label">Fase: {acometida_fase}</text>
                <text x="200" y="320" class="value-label">Neutro: {acometida_neutro}</text>
                <text x="200" y="335" class="value-label">Tierra: {acometida_tierra}</text>

                <line x1="300" y1="180" x2="1680" y2="180" class="line" />

                <rect x="700" y="100" width="200" height="160" class="symbol-stroke" id="symbol-cgp"/>
                <text x="800" y="285" class="label">CGP</text>

                <rect x="750" y="150" width="100" height="60" class="symbol-stroke" />
                <line x1="750" y1="180" x2="850" y2="180" class="symbol-stroke" />
                <text x="800" y="140" class="label">Fusible</text>

                <text x="800" y="310" class="value-label">Tipo: {cgp_tipo}</text>
                <text x="800" y="325" class="value-label">Fusible: {cgp_fusible}</text>

                <g id="symbol-igm">
                    <line x1="1290" y1="180" x2="1290" y2="100" class="line" />
                    <line x1="1290" y1="100" x2="1320" y2="130" class="symbol-stroke" />
                    <line x1="1310" y1="120" x2="1330" y2="140" class="symbol-stroke" />
                    <line x1="1310" y1="140" x2="1330" y2="120" class="symbol-stroke" />
                    <text x="1290" y="90" class="label">IGM</text>
                </g>

                <text x="1290" y="205" class="value-label">Capacidad: {igm_capacidad}</text>

                <line x1="1450" y1="180" x2="1550" y2="180" class="line" id="symbol-lga"/>
                <line x1="1470" y1="170" x2="1470" y2="190" class="symbol-stroke" transform="rotate(45 1470 180)" />
                <line x1="1485" y1="170" x2="1485" y2="190" class="symbol-stroke" transform="rotate(45 1485 180)" />
                <line x1="1500" y1="170" x2="1500" y2="190" class="symbol-stroke" transform="rotate(45 1500 180)" />
                <line x1="1515" y1="170" x2="1515" y2="190" class="symbol-stroke" transform="rotate(45 1515 180)" />
                <line x1="1530" y1="170" x2="1530" y2="190" class="symbol-stroke" transform="rotate(45 1530 180)" />
                <text x="1500" y="120" class="label">LGA</text>

                <text x="1500" y="235" class="value-label">Fase: {lga_fase}</text>
                <text x="1500" y="250" class="value-label">Neutro: {lga_neutro}</text>
                <text x="1500" y="265" class="value-label">Tierra: {lga_tierra}</text>

                <line x1="1680" y1="180" x2="1700" y2="180" class="line" id="symbol-tubo"/>
                <circle cx="1700" cy="180" r="20" class="symbol-stroke" fill="white" />
                <text x="1700" y="120" class="label">Tubo</text>

                <text x="1700" y="235" class="value-label">Diámetro: {tubo_diametro}</text>
            </svg>

            <div id="tooltip" class="tooltip"></div>

            <script>
                const tooltip = document.getElementById('tooltip');
                const svg = document.querySelector('svg'); // Get the SVG element

                // Function to get the position of an SVG element relative to the viewport
                function getSvgElementPosition(element) {
                    const svgRect = svg.getBoundingClientRect();
                    const elementRect = element.getBoundingClientRect();
                    return {
                        x: elementRect.left - svgRect.left,
                        y: elementRect.top - svgRect.top,
                        width: elementRect.width,
                        height: elementRect.height
                    };
                }

                // Data for tooltips - ENSURE THESE ARE CORRECTLY POPULATED BY PYTHON .format()
                const tooltipData = {
                    'label-acometida': `
                        <strong>Acometida</strong>
                        <p>Diámetro: {acometida_diametro}</p>
                        <p>Fase: {acometida_fase}</p>
                        <p>Neutro: {acometida_neutro}</p>
                        <p>Tierra: {acometida_tierra}</p>
                    `,
                    'symbol-cgp': `
                        <strong>Caja General de Protección (CGP)</strong>
                        <p>Tipo: {cgp_tipo}</p>
                        <p>Fusible: {cgp_fusible}</p>
                    `,
                    'symbol-igm': `
                        <strong>Interruptor General de Maniobra (IGM)</strong>
                        <p>Capacidad: {igm_capacidad}</p>
                    `,
                    'symbol-lga': `
                        <strong>Línea General de Alimentación (LGA)</strong>
                        <p>Fase: {lga_fase}</p>
                        <p>Neutro: {lga_neutro}</p>
                        <p>Tierra: {lga_tierra}</p>
                    `,
                    'symbol-tubo': `
                        <strong>Tubo (Salida LGA)</strong>
                        <p>Diámetro: {tubo_diametro}</p>
                    `
                };

                // Add event listeners to elements that should show tooltips
                // Note: For 'g' elements (like symbol-igm), the mouseenter/mouseleave might be tricky
                // to trigger correctly if the 'g' itself doesn't have a visible fill/stroke.
                // It's often better to attach to a rect/path within the group or use a transparent rect.
                const elementsWithTooltips = [
                    document.getElementById('label-acometida'),
                    document.getElementById('symbol-cgp'),
                    document.getElementById('symbol-igm'),
                    document.getElementById('symbol-lga'),
                    document.getElementById('symbol-tubo')
                ].filter(Boolean); // Filter out any nulls if elements aren't found

                elementsWithTooltips.forEach(element => {
                    element.addEventListener('mouseenter', (e) => {
                        const id = element.id;
                        if (tooltipData[id]) {
                            tooltip.innerHTML = tooltipData[id];
                            tooltip.classList.add('visible');

                            // Position the tooltip relative to the mouse cursor
                            // Adjusting for scroll and parent offset
                            const parentRect = svg.parentElement.getBoundingClientRect();
                            const xOffset = e.clientX - parentRect.left + 15; // 15px right of cursor
                            const yOffset = e.clientY - parentRect.top + 15;  // 15px below cursor

                            tooltip.style.left = `${xOffset}px`;
                            tooltip.style.top = `${yOffset}px`;
                        }
                    });

                    element.addEventListener('mouseleave', () => {
                        tooltip.classList.remove('visible');
                    });

                    // Optional: Update tooltip position on mousemove for smoother tracking
                    element.addEventListener('mousemove', (e) => {
                        if (tooltip.classList.contains('visible')) {
                            const parentRect = svg.parentElement.getBoundingClientRect();
                            const xOffset = e.clientX - parentRect.left + 15;
                            const yOffset = e.clientY - parentRect.top + 15;
                            tooltip.style.left = `${xOffset}px`;
                            tooltip.style.top = `${yOffset}px`;
                        }
                    });
                });
            </script>
        </div>
    </div>
</body>
</html>

    

    #< --- Print Button Section ---
    st.header("Exportar Reporte")
    if st.button("Generar Reporte para Imprimir"):
        # 1. Collect all input data into a dictionary
        inputs_data = {
            'company': company,
            'power_kw': power_kw,
            'voltage_v': voltage_v,
            'phase_number': phase_number,
            'load_factor': load_factor,
        }
        
        # 2. Collect all output data into a dictionary
        outputs_data = {
            'calculated_current': calculated_current,
            'igm_spec': igm_spec,
            'cgp_spec': cgp_spec,
            'lga_spec': lga_spec,
            'tubo_spec': tubo_spec,
            'diagram_styles': diagram_styles, 
        }
        href = get_report_download_link(inputs_data, outputs_data, diagram_html)
        st.markdown(href, unsafe_allow_html=True)
        st.info("Haga clic en el enlace de arriba. La ventana de impresión se abrirá automáticamente en la nueva pestaña.")
    
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

st.markdown(
---
### Documentos de Referencia:
* **Endesa:** [Guía de Interpretación NRZ103, Edición 6.1]
* **Unión Fenosa:** [Especificaciones Particulares para Instalaciones de Conexión ES.0100.ES.RE.EIC, Edición: 5,]
* **Iberdrola (i-DE):** [Manual Técnico de Distribución MT 2.80.12, Edición 5, Mayo 2019]  # <-- CHANGED '05' to '5'
* **Iberdrola (i-DE) Tipos de CGP:** [NORMA NI 76.50.01, Edición6a, Julio 2010]
* **Guías Técnicas de Aplicación (Ministerio para la Transición Ecológica y el Reto Demográfico):**
    * [GUÍA-BT-10: Previsión de Cargas, Edición: sep 3, Revisión: 1] # Review '03' here if it's causing issues
    * [GUÍA-BT-12: Esquemas, Edición: sep 3, Revisión: 1] # Review '03' here
    * [GUÍA-BT-13: Cajas Generales de Protección, Edición: sep 3, Revisión: 1] # Review '03' here
    * [GUÍA-BT-14: Línea General de Alimentación, Edición: sep 3, Revisión: 1] # Review '03' here
    * [GUÍA-BT-15: Derivaciones Individuales, Edición: sep 3, Revisión: 1] # Review '03' here
    * [GUÍA-BT-16: Contadores: Ubicación y Sistemas de Instalación, Edición: sep 3, Revisión: 1] # Review '03' here
)
