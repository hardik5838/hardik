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
            fill: #333;
            font-weight: bold;
            text-anchor: middle; /* Center text by default */
        }}
        .value-label {{
            font-family: 'Inter', sans-serif;
            font-size: 12px; /* Smaller for detailed values */
            fill: #555;
            text-anchor: middle;
        }}
        .section-background {{
            stroke-dasharray: 5 5; /* Dashed border for sections */
            stroke: #6b7280; /* Gray-500 */
            stroke-width: 1;
            fill: none;
        }}
        .element-details {{
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            color: #4a5568; /* Tailwind gray-700 */
            line-height: 1.4;
            text-align: center;
        }}
        .element-title {{
            font-weight: bold;
            color: #2d3748; /* Tailwind gray-800 */
            margin-bottom: 4px;
        }}
        .detail-box {{
            @apply bg-white p-4 rounded-lg shadow-md border border-gray-200 flex flex-col items-center justify-center;
            min-width: 200px; /* Ensure boxes are wide enough */
            max-width: 300px;
        }}
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4">
    <div class="bg-white rounded-lg shadow-xl p-6 md:p-8 max-w-5xl w-full">
        <h1 class="text-2xl md:text-3xl font-bold text-center text-gray-800 mb-6">Diagrama de Acometida Eléctrica</h1>

        <div class="flex flex-col items-center justify-center w-full">
            <svg viewBox="0 0 1744 368" class="w-full h-auto max-h-[368px]">
                <!-- Background sections -->
                <rect x="0" y="0" width="580" height="368" fill="#FFFBEA" rx="0" ry="0"/> <!-- Left section (Acometida) -->
                <rect x="580" y="0" width="580" height="368" fill="#EBF5FF" rx="0" ry="0"/> <!-- Middle section (CGP) -->
                <rect x="1160" y="0" width="584" height="368" fill="#E6FFED" rx="0" ry="0"/> <!-- Right section (IGM, LGA, Tubo) -->

                <!-- Dashed borders between sections -->
                <line x1="580" y1="0" x2="580" y2="368" class="section-background" />
                <line x1="1160" y1="0" x2="1160" y2="368" class="section-background" />

                <!-- Acometida Lines (L1, L2, L3, N, T) and Connection Point -->
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

                <!-- Vertical line connecting Acometida lines -->
                <line x1="300" y1="100" x2="300" y2="260" class="line" />
                <!-- Acometida Label (Corrected Position) -->
                <text x="200" y="70" class="label">Acometida</text>

                <!-- Acometida Values (Dynamic Placeholders) -->
                <text x="200" y="290" class="value-label">Diámetro: {{acometida_diametro}}</text>
                <text x="200" y="305" class="value-label">Fase: {{acometida_fase}}</text>
                <text x="200" y="320" class="value-label">Neutro: {{acometida_neutro}}</text>
                <text x="200" y="335" class="value-label">Tierra: {{acometida_tierra}}</text>

                <!-- Main horizontal line (Continuous Path) -->
                <path d="M300,180 H650 M900,180 H1250 M1330,180 H1680" class="line" />

                <!-- CGP (Caja General de Protección) - Fusible Symbol -->
                <!-- Outer box of CGP -->
                <rect x="700" y="100" width="200" height="160" class="symbol-stroke" />
                <text x="800" y="285" class="label">CGP</text>

                <!-- Inner Fusible symbol (rectangle with horizontal line) -->
                <rect x="750" y="150" width="100" height="60" class="symbol-stroke" />
                <line x1="750" y1="180" x2="850" y2="180" class="symbol-stroke" />
                <text x="800" y="140" class="label">Fusible</text>

                <!-- CGP Values (Dynamic Placeholders) -->
                <text x="800" y="310" class="value-label">Tipo: {{cgp_tipo}}</text>
                <text x="800" y="325" class="value-label">Fusible: {{cgp_fusible}}</text>

                <!-- IGM (Interruptor General de Maniobra) - Automatic Switch Symbol (Updated) -->
                <g id="igm-symbol">
                    <!-- Main body of the breaker -->
                    <rect x="1250" y="130" width="80" height="100" class="symbol-stroke" />
                    <!-- Top connection -->
                    <line x1="1290" y1="130" x2="1290" y2="100" class="line" />
                    <!-- Thermal trip unit (small rectangle with line) -->
                    <rect x="1260" y="140" width="20" height="10" class="symbol-stroke" />
                    <line x1="1260" y1="145" x2="1280" y2="145" class="symbol-stroke" />
                    <!-- Magnetic trip unit (arc) -->
                    <path d="M1290,140 A 20 20 0 0 1 1290,160" class="symbol-stroke" />
                    <!-- Contacts (simplified, one per line for unifilar) -->
                    <line x1="1250" y1="180" x2="1270" y2="180" class="line" />
                    <line x1="1310" y1="180" x2="1330" y2="180" class="line" class="line" />
                    <!-- Operating mechanism / 'X' for breaking capacity -->
                    <line x1="1280" y1="160" x2="1300" y2="200" class="symbol-stroke" />
                    <line x1="1280" y1="200" x2="1300" y2="160" class="symbol-stroke" />
                    <text x="1290" y="120" class="label">IGM</text>
                </g>

                <!-- IGM Values (Dynamic Placeholders) -->
                <text x="1290" y="235" class="value-label">Capacidad: {{igm_capacidad}}</text>

                <!-- LGA (Línea General de Alimentación) - Multiple Conductors Symbol (Updated) -->
                <line x1="1450" y1="180" x2="1550" y2="180" class="line" />
                <!-- Oblique strokes (5 strokes for 3F+N+T) -->
                <line x1="1480" y1="170" x2="1480" y2="190" class="symbol-stroke" transform="rotate(45 1480 180)" />
                <line x1="1490" y1="170" x2="1490" y2="190" class="symbol-stroke" transform="rotate(45 1490 180)" />
                <line x1="1500" y1="170" x2="1500" y2="190" class="symbol-stroke" transform="rotate(45 1500 180)" />
                <line x1="1510" y1="170" x2="1510" y2="190" class="symbol-stroke" transform="rotate(45 1510 180)" />
                <line x1="1520" y1="170" x2="1520" y2="190" class="symbol-stroke" transform="rotate(45 1520 180)" />
                <text x="1500" y="120" class="label">LGA</text>

                <!-- LGA Values (Dynamic Placeholders) -->
                <text x="1500" y="235" class="value-label">Fase: {{lga_fase}}</text>
                <text x="1500" y="250" class="value-label">Neutro: {{lga_neutro}}</text>
                <text x="1500" y="265" class="value-label">Tierra: {{lga_tierra}}</text>

                <!-- Tubo Symbol (Circle at the end) -->
                <line x1="1680" y1="180" x2="1700" y2="180" class="line" />
                <circle cx="1700" cy="180" r="20" class="symbol-stroke" fill="white" />
                <text x="1700" y="120" class="label">Tubo</text>

                <!-- Tubo Values (Dynamic Placeholders) -->
                <text x="1700" y="235" class="value-label">Diámetro: {{tubo_diametro}}</text>
            </svg>

            <!-- Details for each element (kept for comprehensive info, can be removed if desired) -->
            <div class="flex flex-wrap justify-center w-full mt-8 gap-4 px-4">
                <!-- Acometida / Tubo Details -->
                <div class="detail-box">
                    <div class="element-title">Acometida</div>
                    <div class="element-details">
                        <p>Diámetro: {{acometida_diametro}}</p>
                        <p>Fase: {{acometida_fase}}</p>
                        <p>Neutro: {{acometida_neutro}}</p>
                        <p>Tierra: {{acometida_tierra}}</p>
                    </div>
                </div>

                <!-- CGP Details -->
                <div class="detail-box">
                    <div class="element-title">Caja General de Protección (CGP)</div>
                    <div class="element-details">
                        <p>Tipo: {{cgp_tipo}}</p>
                        <p>Fusible: {{cgp_fusible}}</p>
                    </div>
                </div>

                <!-- IGM Details -->
                <div class="detail-box">
                    <div class="element-title">Interruptor General de Maniobra (IGM)</div>
                    <div class="element-details">
                        <p>Capacidad: {{igm_capacidad}}</p>
                    </div>
                </div>

                <!-- LGA Details -->
                <div class="detail-box">
                    <div class="element-title">Línea General de Alimentación (LGA)</div>
                    <div class="element-details">
                        <p>Fase: {{lga_fase}}</p>
                        <p>Neutro: {{lga_neutro}}</p>
                        <p>Tierra: {{lga_tierra}}</p>
                    </div>
                </div>

                <!-- Tubo Details (assuming this refers to the final conduit/connection) -->
                <div class="detail-box">
                    <div class="element-title">Tubo (Salida LGA)</div>
                    <div class="element-details">
                        <p>Diámetro: {{tubo_diametro}}</p>
                    </div>
                </div>
            </div>
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

