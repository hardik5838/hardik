import streamlit as st
import math

# --- Data for Distribution Companies (Parsed from your Excel) ---

# Endesa Table AIDE Data
# Potencia prevista (kW), Phase (mm²), Neutral (mm²), Ground (mm²), Max_Len_0.5% (m), Max_Len_1% (m), Tube_Dia (mm), CGP_Amp_Range, Conductor_Amp
endesa_aide_table = [
    {"power_kw": 3, "phase_mm2": 9, "neutral_mm2": 16, "ground_mm2": 10, "max_len_0_5": 101, "max_len_1": 428, "tube_dia_mm": 75, "cgp_amp_range": "60", "conductor_amp_rating": 10},
    {"power_kw": 6, "phase_mm2": 10, "neutral_mm2": 16, "ground_mm2": 10, "max_len_0_5": 106, "max_len_1": 450, "tube_dia_mm": 75, "cgp_amp_range": "80", "conductor_amp_rating": 16},
    {"power_kw": 10, "phase_mm2": 16, "neutral_mm2": 16, "ground_mm2": 16, "max_len_0_5": 173, "max_len_1": 311, "tube_dia_mm": 100, "cgp_amp_range": "100", "conductor_amp_rating": 25},
    {"power_kw": 15, "phase_mm2": 25, "neutral_mm2": 16, "ground_mm2": 16, "max_len_0_5": 173, "max_len_1": 311, "tube_dia_mm": 100, "cgp_amp_range": "125", "conductor_amp_rating": 35},
    {"power_kw": 20, "phase_mm2": 25, "neutral_mm2": 25, "ground_mm2": 25, "max_len_0_5": 204, "max_len_1": 411, "tube_dia_mm": 125, "cgp_amp_range": "160", "conductor_amp_rating": 50},
    {"power_kw": 30, "phase_mm2": 50, "neutral_mm2": 25, "ground_mm2": 25, "max_len_0_5": 224, "max_len_1": 441, "tube_dia_mm": 125, "cgp_amp_range": "200", "conductor_amp_rating": 70},
    {"power_kw": 50, "phase_mm2": 70, "neutral_mm2": 35, "ground_mm2": 35, "max_len_0_5": 244, "max_len_1": 481, "tube_dia_mm": 125, "cgp_amp_range": "250", "conductor_amp_rating": 95},
    {"power_kw": 75, "phase_mm2": 95, "neutral_mm2": 50, "ground_mm2": 50, "max_len_0_5": 275, "max_len_1": 531, "tube_dia_mm": 140, "cgp_amp_range": "250-400", "conductor_amp_rating": 120},
    {"power_kw": 100, "phase_mm2": 120, "neutral_mm2": 70, "ground_mm2": 70, "max_len_0_5": 295, "max_len_1": 571, "tube_dia_mm": 140, "cgp_amp_range": "250-400", "conductor_amp_rating": 150},
    {"power_kw": 156, "phase_mm2": 150, "neutral_mm2": 95, "ground_mm2": 95, "max_len_0_5": 332, "max_len_1": 641, "tube_dia_mm": 160, "cgp_amp_range": "250-400", "conductor_amp_rating": 185},
    {"power_kw": 223, "phase_mm2": 185, "neutral_mm2": 95, "ground_mm2": 95, "max_len_0_5": 352, "max_len_1": 691, "tube_dia_mm": 180, "cgp_amp_range": "250-400", "conductor_amp_rating": 240},
    {"power_kw": 312, "phase_mm2": 240, "neutral_mm2": 150, "ground_mm2": 150, "max_len_0_5": 382, "max_len_1": 761, "tube_dia_mm": 200, "cgp_amp_range": "250-400", "conductor_amp_rating": 300},
]

# Unión Fenosa (ufd) Table Data
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

# Iberdrola (IDE Table) - Placeholder. Needs data.
iberdrola_ide_table = [] # This will be filled when you provide the data

# Generic Cable Diameter Lookup (from previous version, simplified for demonstration)
# This table is used if a direct company lookup doesn't give diameter, or for general reference.
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


def find_cable_data_by_power(power_kw, company_table):
    """Finds the appropriate cable data in a company-specific table based on power."""
    for row in company_table:
        if power_kw <= row["power_kw"]:
            return row
    return None # If power exceeds all listed values


def get_generic_diameter_from_area(area_mm2):
    """Finds the approximate overall diameter for a given cross-sectional area."""
    # This function assumes cable_data is sorted by area_mm2
    for cable in generic_cable_diameter_data:
        if cable["area_mm2"] == area_mm2:
            return cable["diameter_mm"]
    return "N/A" # Diameter not found for this exact area


def calculate_current(power_kw, voltage_v, phase_number, power_factor):
    """Calculates the current based on power, voltage, phase, and power factor."""
    if voltage_v == 0 or power_factor == 0:
        return 0 # Avoid division by zero

    power_w = power_kw * 1000
    if phase_number == 3:
        return power_w / (math.sqrt(3) * voltage_v * power_factor)
    elif phase_number == 1:
        return power_w / (voltage_v * power_factor)
    return 0 # Should not happen with valid phase_number

# --- Streamlit App ---
st.set_page_config(page_title="Installation Guide Generator", layout="centered", icon="⚡")

st.title("⚡ Electrical Installation Guide Generator")
st.markdown("Generate tailored electrical requirements based on distribution company standards.")

# --- Input Section ---
st.header("Input Parameters")

col1, col2 = st.columns(2)
with col1:
    company = st.selectbox(
        "Select Distribution Company",
        options=["Endesa", "Iberdrola", "Unión Fenosa"],
        index=0 # Default to Endesa
    )
    power_kw = st.number_input("Maximum Contracted Power (kW)", min_value=0.0, value=10.0, step=1.0, help="The maximum power expected for the installation.")
    voltage_v = st.number_input("Nominal Network Voltage (V)", min_value=0.0, value=400.0, step=1.0, help="Typically 400V for 3-phase, 230V for 1-phase in Spain.")

with col2:
    phase_number = st.selectbox("Phase Number", options=[1, 3], index=1, help="1-phase or 3-phase system.")
    load_factor = st.slider("Load Factor (Power Factor)", min_value=0.8, max_value=1.0, value=0.9, step=0.01, help="Also known as Power Factor (cos phi).")
    voltage_drop_limit = st.slider("Voltage Drop Limit (%)", min_value=0.5, max_value=5.0, value=0.5, step=0.1, help="Maximum allowed voltage drop in the installation.")


st.info("You can also directly input the design current if you have it (overrides power calculation).")
input_design_current_a = st.number_input("Calculated Design Current (A) (Optional)", min_value=0.0, value=0.0, step=1.0, help="If provided, this current will be used directly for sizing purposes.")


# --- Calculations & Logic ---
st.header("Generated Requirements")

selected_table = []
if company == "Endesa":
    selected_table = endesa_aide_table
elif company == "Unión Fenosa":
    selected_table = ufd_table
elif company == "Iberdrola":
    # Placeholder for Iberdrola data - will need to be populated
    selected_table = iberdrola_ide_table
    st.warning("Iberdrola (IDE) data is not yet integrated. Results may be based on generic calculations or placeholder data.")

# Determine the current to use for sizing
if input_design_current_a > 0:
    calculated_current = input_design_current_a
    st.write(f"Using provided Design Current: **{calculated_current:.2f} A**")
else:
    calculated_current = calculate_current(power_kw, voltage_v, phase_number, load_factor)
    st.write(f"Calculated Design Current (I_B) based on inputs: **{calculated_current:.2f} A**")


# Lookup values from the company-specific table based on Power
company_specific_results = find_cable_data_by_power(power_kw, selected_table)

if company_specific_results:
    st.subheader(f"Requirements for {company} (Based on Power)")

    # Cable Sections
    st.markdown("#### Cable Sections (mm²)")
    st.write(f"- **Phase Wire Section:** {company_specific_results['phase_mm2']} mm²")
    st.write(f"- **Neutral Section:** {company_specific_results['neutral_mm2']} mm²")
    st.write(f"- **Protective Earth (Ground) Section:** {company_specific_results['ground_mm2']} mm²")

    # Overall Cable Diameter (derived from phase wire section if possible)
    # The company tables directly give tube diameter, but we can also infer cable diameter
    overall_cable_diameter = get_generic_diameter_from_area(company_specific_results['phase_mm2'])
    st.write(f"- **Approx. Overall Cable Diameter (derived):** {overall_cable_diameter} mm (Based on Phase Wire Section)")


    # Installation Details
    st.markdown("#### Installation Specifics")
    st.write(f"- **Minimum Tube Diameter:** {company_specific_results['tube_dia_mm']} mm")

    if 'max_len_0_5' in company_specific_results and 'max_len_1' in company_specific_results:
        # Determine which max length to show based on user's voltage drop limit
        if voltage_drop_limit <= 0.5:
             st.write(f"- **Maximum Recommended Length (for {voltage_drop_limit:.1f}% voltage drop):** {company_specific_results['max_len_0_5']} m")
        elif voltage_drop_limit <= 1.0:
            st.write(f"- **Maximum Recommended Length (for {voltage_drop_limit:.1f}% voltage drop):** {company_specific_results['max_len_1']} m")
        else:
            st.write(f"- **Maximum Length @ 0.5% Voltage Drop:** {company_specific_results['max_len_0_5']} m")
            st.write(f"- **Maximum Length @ 1.0% Voltage Drop:** {company_specific_results['max_len_1']} m")
    else:
        st.info(f"Max length data for {company} not directly available in selected table, or is fixed for specific voltage drops.")


    # Electrical Devices & Capacities
    st.markdown("#### Electrical Devices & Capacities")

    # CGP (Caja General de Protección)
    if company == "Endesa":
        cgp_info = company_specific_results.get('cgp_amp_range', 'N/A')
        st.write(f"- **Tipo De CGP (General Protection Box):** Related to **{cgp_info} Amps**")
        # Fuse and Breaker Capacity from conductor_amp_rating from Endesa
        st.write(f"- **Recommended Fuse Capacity:** {company_specific_results.get('conductor_amp_rating', 'N/A')} A")
        st.write(f"- **Recommended Breaker Capacity:** {company_specific_results.get('conductor_amp_rating', 'N/A')} A")
        st.info("*(Note: Fuse and Breaker capacities are typically based on the associated conductor's current rating from the Endesa table.)*")

    elif company == "Unión Fenosa":
        # Union Fenosa table doesn't directly specify CGP/Fuse/Breaker capacity.
        # We can make a general recommendation based on calculated current.
        st.write("- **Tipo De CGP (General Protection Box):** Based on general regulations, likely a standard CGP for this power range.")
        # Basic breaker/fuse sizing: 1.25 * calculated_current is a common rule of thumb.
        # However, company tables often provide specific values. We'll use the calculated current for now.
        st.write(f"- **Recommended Fuse Capacity (Min):** Approx. {calculated_current * 1.25:.2f} A (needs company-specific lookup)")
        st.write(f"- **Recommended Breaker Capacity (Min):** Approx. {calculated_current * 1.25:.2f} A (needs company-specific lookup)")
        st.info("*(Note: Fuse/Breaker capacities for Unión Fenosa are not directly in the provided table; general sizing rule used.)*")

    elif company == "Iberdrola":
         st.info("Specific device recommendations for Iberdrola (IDE) will appear here once data is integrated.")


else:
    st.warning(f"No specific data found for {company} for a contracted power of {power_kw} kW. Results may be based on general current calculation only.")
    # Fallback to generic cable diameter if no company-specific data
    # (This assumes the generic table's three_phase_amps are suitable as a backup)
    # The previous generic cable lookup was based on 'three_phase_amps'
    # We can try to find the closest generic cable for the calculated current
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
* [Endesa Table AIDE (Provided by User)]
* [Unión Fenosa Table (Provided by User)]
* [Electrical Wiring Guide Cable Size Calculator Current Rating Chart Amps](https://smartshop.lk-ea.com/blog-articles/post/electrical-wiring-guide-cable-size-calculator-current-rating-chart-amps.html)
* [Cable Size Current Rating Chart](https://www.spwales.com/cable-size-current-rating-chart)
* [Table 4E1A](https://www.cse-distributors.co.uk/cable/technical-tables-useful-info/table-4e1a.html)
""")
