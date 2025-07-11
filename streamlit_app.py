import streamlit as st
import math

# --- Data for Distribution Companies ---

# Endesa NRZ103 Annex Table (Page 69) - Main reference for Endesa's contracted power to nominal current mapping
# This table maps Potencia prevista (kW) for 400V 3-phase to corresponding Nominal Current (A) for Main Breaker/Fuse
endesa_contracted_power_data = [
    # Power_kW, Base_Contractual_A, Nom_Int_A (Nominal Intensity of protection devices)
    {"power_kw": 3.46, "base_contractual_a": 5, "nom_int_a": 63},
    {"power_kw": 5.19, "base_contractual_a": 7.5, "nom_int_a": 63},
    {"power_kw": 6.92, "base_contractual_a": 10, "nom_int_a": 63},
    {"power_kw": 10.39, "base_contractual_a": 15, "nom_int_a": 63},
    {"power_kw": 13.85, "base_contractual_a": 20, "nom_int_a": 63},
    {"power_kw": 17.32, "base_contractual_a": 25, "nom_int_a": 63},
    {"power_kw": 20.78, "base_contractual_a": 30, "nom_int_a": 63},
    {"power_kw": 24.24, "base_contractual_a": 35, "nom_int_a": 63},
    {"power_kw": 27.71, "base_contractual_a": 40, "nom_int_a": 63},
    {"power_kw": 31.17, "base_contractual_a": 45, "nom_int_a": 63},
    {"power_kw": 34.64, "base_contractual_a": 50, "nom_int_a": 63},
    {"power_kw": 43.64, "base_contractual_a": 63, "nom_int_a": 63},
    {"power_kw": 55.42, "base_contractual_a": 80, "nom_int_a": 100},
    {"power_kw": 69.30, "base_contractual_a": 100, "nom_int_a": 100},
    {"power_kw": 88.60, "base_contractual_a": 125, "nom_int_a": 160},
    {"power_kw": 103.92, "base_contractual_a": 150, "nom_int_a": 160},
    {"power_kw": 138.60, "base_contractual_a": 200, "nom_int_a": 250},
    {"power_kw": 173.20, "base_contractual_a": 250, "nom_int_a": 250},
    {"power_kw": 207.84, "base_contractual_a": 300, "nom_int_a": 400},
    {"power_kw": 218.30, "base_contractual_a": 315, "nom_int_a": 400},
    {"power_kw": 277.10, "base_contractual_a": 400, "nom_int_a": 400},
    {"power_kw": 346.40, "base_contractual_a": 500, "nom_int_a": 630},
]

# Endesa NRZ103 IGM Sizing Rule (Page 54) - Specific rule for the main switch
def get_endesa_igm_capacity(power_kw):
    if power_kw <= 90:
        return "160 A"
    elif power_kw <= 150:
        return "250 A"
    else:
        return "Appropriate switch/disconnector (consult EDE for >400A)" # As per document text

# Endesa NRZ103 CGP Type Mapping (Page 21, Section 5.4) - Maps nominal current to CGP model
endesa_cgp_types = [
    {"max_current_a": 100, "type": "BUC - esquema 7-100 A"},
    {"max_current_a": 160, "type": "BUC - esquema 7-160 A or 9-160 A"},
    {"max_current_a": 250, "type": "BUC - esquema 7-250 A or 9-250 A"},
    {"max_current_a": 400, "type": "BUC - esquema 7-400 A or 9-400 A"},
]

# Union Fenosa (ufd) Table Data - Contains explicit phase, neutral, ground sections
ufd_table = [
    {"power_kw": 24.9, "phase_mm2": 10, "neutral_mm2": 10, "ground_mm2": 10, "max_len_0_5": 18, "max_len_1": 35, "tube_dia_mm": 75},
    {"power_kw": 37.4, "phase_mm2": 16, "neutral_mm2": 10, "ground_mm2": 10, "max_len_0_5": 12, "max_len_1": 24, "tube_dia_mm": 75},
    {"power_kw": 50.5, "phase_mm2": 16, "neutral_mm2": 16, "ground_mm2": 16, "max_len_0_5": 14, "max_len_1": 28, "tube_dia_mm": 75},
    {"power_kw": 65.8, "phase_mm2": 25, "neutral_mm2": 16, "ground_mm2": 16, "max_len_0_5": 17, "max_len_1": 33, "tube_dia_mm": 110},
    {"power_kw": 82.4, "phase_mm2": 35, "neutral_mm2": 25, "ground_mm2": 16, "max_len_0_5": 19, "max_len_1": 37, "tube_dia_mm": 110},
    {"power_kw": 100.5, "phase_mm2": 50, "neutral_mm2": 25, "ground_mm2": 25, "max_len_0_5": 22, "max_len_1": 44, "tube_dia_mm": 110},
    {"power_kw": 128.2, "phase_mm2": 70, "neutral_mm2": 35, "ground_mm2": 35, "max_len_0_5": 24, "max_len_1": 48, "tube_dia_mm": 125},
    {"power_kw": 155.2, "phase_mm2": 95, "neutral_mm2": 50, "ground_mm2": 50, "max_len_0_5": 27, "max_len_1": 54, "tube_dia_mm": 140},
    {"power_kw": 180.1, "phase_mm2": 120, "neutral_mm2": 70, "ground_mm2": 70, "max_len_0_5": 29, "max_len_1": 59, "tube_dia_mm": 140},
    {"power_kw": 207.2, "phase_mm2": 150, "neutral_mm2": 95, "ground_mm2": 95, "max_len_0_5": 32, "max_len_1": 64, "tube_dia_mm": 160},
    {"power_kw": 236.3, "phase_mm2": 185, "neutral_mm2": 95, "ground_mm2": 95, "max_len_0_5": 35, "max_len_1": 69, "tube_dia_mm": 180},
    {"power_kw": 277.8, "phase_mm2": 240, "neutral_mm2": 150, "ground_mm2": 150, "max_len_0_5": 38, "max_len_1": 76, "tube_dia_mm": 200},
]

# Iberdrola (IDE) Table Data - Parsed from your provided Excel snippet
iberdrola_ide_table = [
    # Power_kW, Phase (mm²), Neutral (mm²), Ground (mm²), Max_Len_0.5% (m), Max_Len_1% (m), Tube_Dia (mm), CGP_Amp_Range, Conductor_Amp_Rating (used for Fuse/Breaker)
    # Note: Power_kw values were inferred for some rows based on the AMP column or context.
    {"power_kw": 3, "phase_mm2": 9, "neutral_mm2": 16, "ground_mm2": 10, "max_len_0_5": 101, "max_len_1": 428, "tube_dia_mm": 75, "cgp_amp_range": "60", "conductor_amp_rating": 10},
    {"power_kw": 6, "phase_mm2": 10, "neutral_mm2": 16, "ground_mm2": 10, "max_len_0_5": 106, "max_len_1": 450, "tube_dia_mm": 75, "cgp_amp_range": "80", "conductor_amp_rating": 16},
    {"power_kw": 10, "phase_mm2": 16, "neutral_mm2": 16, "ground_mm2": 16, "max_len_0_5": 173, "max_len_1": 311, "tube_dia_mm": 100, "cgp_amp_range": "100", "conductor_amp_rating": 25},
    {"power_kw": 25, "phase_mm2": 16, "neutral_mm2": 16, "ground_mm2": 16, "max_len_0_5": 173, "max_len_1": 311, "tube_dia_mm": 100, "cgp_amp_range": "100", "conductor_amp_rating": 25},
    {"power_kw": 50, "phase_mm2": 25, "neutral_mm2": 25, "ground_mm2": 25, "max_len_0_5": 204, "max_len_1": 411, "tube_dia_mm": 125, "cgp_amp_range": "160", "conductor_amp_rating": 50},
    {"power_kw": 78, "phase_mm2": 50, "neutral_mm2": 25, "ground_mm2": 25, "max_len_0_5": 224, "max_len_1": 441, "tube_dia_mm": 125, "cgp_amp_range": "200", "conductor_amp_rating": 70},
    {"power_kw": 95, "phase_mm2": 50, "neutral_mm2": 50, "ground_mm2": 50, "max_len_0_5": 224, "max_len_1": 441, "tube_dia_mm": 125, "cgp_amp_range": "250", "conductor_amp_rating": 95},
    {"power_kw": 125, "phase_mm2": 95, "neutral_mm2": 50, "ground_mm2": 50, "max_len_0_5": 275, "max_len_1": 531, "tube_dia_mm": 140, "cgp_amp_range": "250-400", "conductor_amp_rating": 150},
    {"power_kw": 150, "phase_mm2": 95, "neutral_mm2": 95, "ground_mm2": 95, "max_len_0_5": 275, "max_len_1": 531, "tube_dia_mm": 140, "cgp_amp_range": "250-400", "conductor_amp_rating": 150},
    {"power_kw": 196, "phase_mm2": 150, "neutral_mm2": 150, "ground_mm2": 150, "max_len_0_5": 295, "max_len_1": 571, "tube_dia_mm": 140, "cgp_amp_range": "250-400", "conductor_amp_rating": 240},
    {"power_kw": 240, "phase_mm2": 150, "neutral_mm2": 150, "ground_mm2": 150, "max_len_0_5": 295, "max_len_1": 571, "tube_dia_mm": 140, "cgp_amp_range": "250-400", "conductor_amp_rating": 240},
    {"power_kw": 315, "phase_mm2": 225, "neutral_mm2": 225, "ground_mm2": 225, "max_len_0_5": 332, "max_len_1": 641, "tube_dia_mm": 160, "cgp_amp_range": "250-400", "conductor_amp_rating": 315},
]


# Generic Cable Diameter Lookup - Used as a fallback or for deriving diameter from section
generic_cable_diameter_data = [
    {"area_mm2": 1.5, "diameter_mm": 2.9, "three_phase_amps": 15.5},
    {"area_mm2": 2.5, "diameter_mm": 3.5, "three_phase_amps": 21},
    {"area_mm2": 4, "diameter_mm": 4.4, "three_phase_amps": 28},
    {"area_mm2": 6, "diameter_mm": 4.6, "three_phase_amps": 36},
    {"area_mm2": 10, "diameter_mm": 5.9, "three_phase_amps": 50},
    {"area_mm2": 16, "diameter_mm": 6.9, "three_phase_amps": 68},
    {"area_mm2": 25, "diameter_mm": 8.7, "three_phase_amps": 89},
    {"area_mm2": 35, "diameter_mm": 10.0, "three_phase_amps": 110},
    {"area_mm2": 50, "diameter_mm": 11.8, "three_phase_amps": 134},
    {"area_mm2": 70, "diameter_mm": 13.5, "three_phase_amps": 171},
    {"area_mm2": 95, "diameter_mm": 15.7, "three_phase_amps": 207},
    {"area_mm2": 120, "diameter_mm": 17.4, "three_phase_amps": 239},
    {"area_mm2": 150, "diameter_mm": 19.3, "three_phase_amps": 262},
    {"area_mm2": 185, "diameter_mm": 21.5, "three_phase_amps": 296},
    {"area_mm2": 240, "diameter_mm": 24.6, "three_phase_amps": 346},
    {"area_mm2": 300, "diameter_mm": 27.9, "three_phase_amps": 394},
    {"area_mm2": 400, "diameter_mm": 30.8, "three_phase_amps": 467},
    {"area_mm2": 500, "diameter_mm": 33.8, "three_phase_amps": 533},
    {"area_mm2": 630, "diameter_mm": 37.6, "three_phase_amps": 611},
]

# --- Helper Functions ---

def find_data_by_power(power_kw, data_table):
    """Finds the appropriate data row in a company-specific table based on power.
    Assumes table is sorted by power_kw ascending. Returns the row where power_kw is <= row's power_kw."""
    for row in data_table:
        if power_kw <= row["power_kw"]:
            return row
    return data_table[-1] if data_table else None # Return max available if power exceeds known range, or None if table is empty


def get_generic_diameter_from_area(area_mm2):
    """Finds the approximate overall diameter for a given cross-sectional area from generic data."""
    if not isinstance(area_mm2, (int, float)):
        return "N/A" # Handle non-numeric input gracefully

    for cable in generic_cable_diameter_data:
        if cable["area_mm2"] == area_mm2:
            return cable["diameter_mm"]
    return "N/A" # Diameter not found for this exact area


def calculate_current(power_kw, voltage_v, phase_number, power_factor):
    """Calculates the current (I_B) based on power, voltage, phase, and power factor."""
    if voltage_v == 0 or power_factor == 0:
        return 0 # Avoid division by zero

    power_w = power_kw * 1000 # Convert kW to Watts
    if phase_number == 3:
        # Formula for 3-phase: I = P / (sqrt(3) * V * PF)
        return power_w / (math.sqrt(3) * voltage_v * power_factor)
    elif phase_number == 1:
        # Formula for 1-phase: I = P / (V * PF)
        return power_w / (voltage_v * power_factor)
    return 0 # Should not happen with valid phase_number input

# --- Streamlit Application Layout and Logic ---

st.set_page_config(page_title="Electrical Installation Guide Generator", layout="centered")

st.title("⚡ Electrical Installation Guide Generator")
st.markdown("Generate tailored electrical requirements based on distribution company standards.")

# --- Input Section ---
st.header("Input Parameters")

col1, col2 = st.columns(2)
with col1:
    company = st.selectbox(
        "Select Distribution Company",
        options=["Endesa", "Iberdrola", "Unión Fenosa"],
        index=0, # Default to Endesa
        help="Choose the electricity distribution company for specific regulations."
    )
    power_kw = st.number_input(
        "Maximum Contracted Power (kW)",
        min_value=0.0, value=100.0, step=1.0,
        help="The maximum power expected for the installation, as contracted with the utility."
    )
    voltage_v = st.number_input(
        "Nominal Network Voltage (V)",
        min_value=0.0, value=400.0, step=1.0,
        help="Typically 400V for 3-phase, 230V for 1-phase in Spain."
    )

with col2:
    phase_number = st.selectbox(
        "Phase Number",
        options=[1, 3],
        index=1, # Default to 3-phase
        help="Select if the system is 1-phase or 3-phase."
    )
    load_factor = st.slider(
        "Load Factor (Power Factor)",
        min_value=0.8, max_value=1.0, value=0.9, step=0.01,
        help="Also known as Power Factor (cos phi). Represents the ratio of real power to apparent power."
    )
    voltage_drop_limit = st.slider(
        "Voltage Drop Limit (%)",
        min_value=0.5, max_value=5.0, value=0.5, step=0.1,
        help="Maximum allowed voltage drop in the installation, as per regulation."
    )

st.info("You can also directly input the design current if you have it (this will override power calculation for sizing).")
input_design_current_a = st.number_input(
    "Calculated Design Current (A) (Optional)",
    min_value=0.0, value=0.0, step=1.0,
    help="If provided and greater than 0, this current will be used directly for sizing purposes instead of calculating from Power/Voltage."
)


# --- Calculations & Logic ---
st.header("Generated Requirements")

selected_company_data = None
uf_ref_data_for_ground = None # To store UF data for ground conductor reference for Endesa

# Select the appropriate company table
if company == "Endesa":
    selected_company_data = find_data_by_power(power_kw, endesa_contracted_power_data)
    # For Endesa, we reference Union Fenosa data for ground wire sizing as Endesa's table doesn't explicitly provide it.
    uf_ref_data_for_ground = find_data_by_power(power_kw, ufd_table)
    if power_kw > 346.40: # Max power in Endesa's primary table
         st.warning("For contracted power above 346.40 kW with Endesa, consult official Endesa documentation for specific requirements.")
elif company == "Unión Fenosa":
    selected_company_data = find_data_by_power(power_kw, ufd_table)
    if power_kw > 277.8: # Max power in Union Fenosa's table
        st.warning("For contracted power above 277.8 kW with Unión Fenosa, consult official Unión Fenosa documentation for specific requirements.")
elif company == "Iberdrola":
    selected_company_data = find_data_by_power(power_kw, iberdrola_ide_table)
    if power_kw > 315: # Max power in Iberdrola's table
        st.warning("For contracted power above 315 kW with Iberdrola, consult official Iberdrola documentation for specific requirements.")

# Determine the current (I_B) to use for sizing
if input_design_current_a > 0:
    calculated_current = input_design_current_a
    st.write(f"Using provided Design Current: **{calculated_current:.2f} A**")
else:
    calculated_current = calculate_current(power_kw, voltage_v, phase_number, load_factor)
    st.write(f"Calculated Design Current (I_B) based on inputs: **{calculated_current:.2f} A**")


if selected_company_data:
    st.subheader(f"Requirements for {company} (Based on {power_kw} kW Contracted Power)")

    # --- Cable Sections ---
    st.markdown("#### Cable Sections (mm²)")
    
    phase_mm2 = "N/A"
    neutral_mm2 = "N/A"
    ground_mm2 = "N/A"
    overall_cable_diameter = "N/A" # Initialize here to ensure it's always defined

    if company == "Endesa":
        # For Endesa, we derive cable sections based on the nominal current from the contracted power data.
        # This requires cross-referencing with the generic cable data's ampacities.
        required_nom_int = selected_company_data['nom_int_a']
        found_generic_cable_for_nom_int = None
        for cable in generic_cable_diameter_data:
            if cable["three_phase_amps"] >= required_nom_int:
                found_generic_cable_for_nom_int = cable
                break

        if found_generic_cable_for_nom_int:
            phase_mm2 = found_generic_cable_for_nom_int['area_mm2']
            neutral_mm2 = phase_mm2 # Endesa NRZ103 Page 23: Neutral recommended same as phase
            
            # Ground (Terra) for Endesa: Use UF table as reference based on equivalent power
            if uf_ref_data_for_ground and 'ground_mm2' in uf_ref_data_for_ground:
                ground_mm2 = uf_ref_data_for_ground['ground_mm2']
                st.write(f"- **Phase Wire Section:** {phase_mm2} mm²")
                st.write(f"- **Neutral Section:** {neutral_mm2} mm²")
                st.write(f"- **Protective Earth (Ground) Section:** {ground_mm2} mm²")
                st.info("*(Note: For Endesa, Neutral section is recommended equal to Phase (NRZ103). Ground section is derived from an equivalent power rating in the Unión Fenosa table, as explicit ground sections are not in Endesa's primary tables.)*")
            else:
                st.write(f"- **Phase Wire Section:** {phase_mm2} mm²")
                st.write(f"- **Neutral Section:** {neutral_mm2} mm²")
                st.write(f"- **Protective Earth (Ground) Section:** N/A (Consult REBT ITC-BT 14 or specific Endesa documentation. UF data not found.)")
                st.info("*(Note: For Endesa, Neutral section is recommended equal to Phase (NRZ103). Ground section not explicitly in Endesa's primary tables or a suitable reference could not be found.)*")
            
            # Get overall diameter only if phase_mm2 is a number
            if isinstance(phase_mm2, (int, float)):
                overall_cable_diameter = get_generic_diameter_from_area(phase_mm2)
            st.write(f"- **Approx. Overall Cable Diameter (derived):** {overall_cable_diameter} mm (Based on Phase Wire Section)")
        else:
            st.write("- **Cable Sections:** Not determined from available data. Consult Endesa documentation.")

    else: # For Unión Fenosa and Iberdrola (as their tables have explicit sections)
        phase_mm2 = selected_company_data.get('phase_mm2', 'N/A')
        neutral_mm2 = selected_company_data.get('neutral_mm2', 'N/A')
        ground_mm2 = selected_company_data.get('ground_mm2', 'N/A')
        
        st.write(f"- **Phase Wire Section:** {phase_mm2} mm²")
        st.write(f"- **Neutral Section:** {neutral_mm2} mm²")
        st.write(f"- **Protective Earth (Ground) Section:** {ground_mm2} mm²")
        
        # Get overall diameter only if phase_mm2 is a number
        if isinstance(phase_mm2, (int, float)):
            overall_cable_diameter = get_generic_diameter_from_area(phase_mm2)
        st.write(f"- **Approx. Overall Cable Diameter (derived):** {overall_cable_diameter} mm (Based on Phase Wire Section)")

    # --- Installation Details ---
    st.markdown("#### Installation Specifics")
    st.write(f"- **Minimum Tube Diameter:** {selected_company_data.get('tube_dia_mm', 'N/A')} mm")

    # Voltage Drop Limits and Max Length
    if 'max_len_0_5' in selected_company_data and 'max_len_1' in selected_company_data:
        if voltage_drop_limit <= 0.5:
             st.write(f"- **Maximum Recommended Length (for {voltage_drop_limit:.1f}% voltage drop):** {selected_company_data['max_len_0_5']} m")
        elif voltage_drop_limit <= 1.0:
            st.write(f"- **Maximum Recommended Length (for {voltage_drop_limit:.1f}% voltage drop):** {selected_company_data['max_len_1']} m")
        else:
            st.write(f"- **Maximum Length @ 0.5% Voltage Drop:** {selected_company_data['max_len_0_5']} m")
            st.write(f"- **Maximum Length @ 1.0% Voltage Drop:** {selected_company_data['max_len_1']} m")
            st.info("*(Note: For voltage drop limits above 1.0%, you might need to consult specific company guidelines for longer lengths.)*")
    else:
        st.info(f"Max length data for {company} not directly available in selected table for various voltage drops.")


    # --- Electrical Devices & Capacities ---
    st.markdown("#### Electrical Devices & Capacities")

    # CGP (Caja General de Protección) and Fuse/Breaker Logic
    if company == "Endesa":
        # IGM Capacity (from Endesa NRZ103 Page 54)
        igm_capacity = get_endesa_igm_capacity(power_kw)
        st.write(f"- **Interruptor General de Maniobra (IGM) Capacity:** {igm_capacity}")
        if power_kw > 150:
            st.info("*(Note: For contracted power above 150kW with Endesa, IGM capacity requires agreement with Endesa.)*")

        # CGP Type (from Endesa NRZ103 Page 21)
        nominal_current_for_cgp = selected_company_data.get('nom_int_a', 0)
        cgp_type = get_endesa_cgp_type(nominal_current_for_cgp)
        st.write(f"- **Tipo De CGP (General Protection Box):** {cgp_type}")

        # Fuse/Breaker Capacity (from Endesa NRZ103 Page 69, 'nom_int_a')
        fuse_breaker_capacity = selected_company_data.get('nom_int_a', 'N/A')
        st.write(f"- **Recommended Fuse Capacity:** {fuse_breaker_capacity} A")
        st.write(f"- **Recommended Breaker Capacity:** {fuse_breaker_capacity} A")
        st.info("*(Note: Fuse and Breaker capacities for Endesa are typically based on the 'Intensidad Nominal' from the contracted power table.)*")

        # LGA Capacity Check (Endesa NRZ103 Page 22)
        lga_max_current = 250 # Typical max capacity
        if calculated_current > lga_max_current:
            st.warning(f"LGA maximum capacity for Endesa is typically 250A. Your calculated current ({calculated_current:.2f} A) exceeds this. Consult Endesa for exceptions up to 400A.")


    elif company in ["Iberdrola", "Unión Fenosa"]:
        # For Iberdrola and Union Fenosa, use 'conductor_amp_rating' if available, else general rule
        if 'conductor_amp_rating' in selected_company_data:
            st.write(f"- **Recommended Fuse Capacity:** {selected_company_data['conductor_amp_rating']} A")
            st.write(f"- **Recommended Breaker Capacity:** {selected_company_data['conductor_amp_rating']} A")
            st.info("*(Note: Fuse and Breaker capacities for this company are based on specific table values.)*")
        else:
            st.write(f"- **Recommended Fuse Capacity (Min):** Approx. {calculated_current * 1.25:.2f} A (needs company-specific lookup)")
            st.write(f"- **Recommended Breaker Capacity (Min):** Approx. {calculated_current * 1.25:.2f} A (needs company-specific lookup)")
            st.info("*(Note: Fuse/Breaker capacities are not directly in this company's provided table; general sizing rule used as a placeholder.)*")
        
        # CGP for Iberdrola/Union Fenosa
        if 'cgp_amp_range' in selected_company_data:
            st.write(f"- **Tipo De CGP (General Protection Box):** Related to **{selected_company_data['cgp_amp_range']} Amps**")
        else:
            st.write("- **Tipo De CGP (General Protection Box):** Information not directly available in this company's table.")


else: # If no data found for the selected company and power (should ideally not happen if tables are complete)
    st.warning(f"No specific data found for {company} for a contracted power of {power_kw} kW. Please check the input power or consult official company tables.")
    
    # Fallback to generic cable diameter based on calculated current if no company-specific data
    found_generic_cable = None
    for cable in generic_cable_diameter_data:
        if cable["three_phase_amps"] >= calculated_current:
            found_generic_cable = cable
            break
    if found_generic_cable:
        st.markdown("#### Generic Cable Recommendation (Fallback)")
        st.write(f"- **Required Cable Cross-Sectional Area (approx):** {found_generic_cable['area_mm2']} mm²")
        st.write(f"- **Approx. Overall Cable Diameter:** {found_generic_cable['diameter_mm']} mm")
        st.write(f"*(Based on calculated current {calculated_current:.2f} A)*")
    else:
        st.error("No suitable generic cable found for the calculated current in the available data.")


st.markdown("""
---
### Reference Tables:
* [Endesa Guía NRZ103 (Provided by User)]
* [Unión Fenosa Table (Provided by User)]
* [Iberdrola IDE Table (Provided by User)]
* [General Cable Size Chart 1](https://smartshop.lk-ea.com/blog-articles/post/electrical-wiring-guide-cable-size-calculator-current-rating-chart-amps.html)
* [General Cable Size Chart 2](https://www.spwales.com/cable-size-current-rating-chart)
* [General Cable Size Chart 3](https://www.cse-distributors.co.uk/cable/technical-tables-useful-info/table-4e1a.html)
""")



