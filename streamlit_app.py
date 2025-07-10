
import streamlit as st

def calculate_cable_diameter(power_kw, voltage_v, phase_number, power_factor, input_amps=None):
    """
    Calculates the required cable diameter based on power, voltage, and phase.
    If input_amps is provided, it uses that directly for lookup.
    """

    # Cable data based on your provided table (for 3-phase current rating)
    # This is a simplified representation. In a real application, you might
    # have more detailed data including insulation type, material, etc.
    cable_data = [
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

    if input_amps is not None:
        # If amps are provided, use them directly for lookup
        calculated_current = input_amps
    else:
        # Calculate current based on power, voltage, and phase
        # For 3-phase: I = P / (sqrt(3) * V * PF)
        # For 1-phase: I = P / (V * PF)
        power_w = power_kw * 1000
        if phase_number == 3:
            calculated_current = power_w / (1.732 * voltage_v * power_factor)
        elif phase_number == 1:
            calculated_current = power_w / (voltage_v * power_factor)
        else:
            return None, "Invalid phase number. Please choose 1 or 3."

    # Find the smallest cable that can handle the calculated current
    recommended_cable = None
    for cable in cable_data:
        if cable["three_phase_amps"] >= calculated_current:
            recommended_cable = cable
            break

    return calculated_current, recommended_cable

# --- Streamlit App ---
st.set_page_config(page_title="Cable Diameter Calculator", layout="centered")

st.title("⚡ Cable Diameter Calculator for Internal Power Transmission")
st.markdown("Enter the electrical parameters to get the recommended cable diameter.")

# Input section
st.header("Input Parameters")

col1, col2 = st.columns(2)
with col1:
    power_kw = st.number_input("Power (kW)", min_value=0.0, value=100.0, step=1.0)
    voltage_v = st.number_input("Voltage (V)", min_value=0.0, value=400.0, step=1.0)
with col2:
    phase_number = st.selectbox("Phase Number", options=[1, 3], index=1) # Default to 3-phase
    power_factor = st.number_input("Power Factor (0.0 - 1.0)", min_value=0.0, max_value=1.0, value=0.9, step=0.01)

st.info("You can also directly input the calculated current if you already have it.")
input_iga_a = st.number_input("Intensidad I.G.A. (A) (Optional)", min_value=0.0, value=250.0, step=1.0)
# If the user provides I.G.A., we'll use that instead of calculating from Power/Voltage.
# If I.G.A. is 0, we assume the user wants to calculate from Power/Voltage.

# --- Calculations ---
st.header("Calculation Results")

# Determine whether to use input_iga_a or calculate current
if input_iga_a > 0:
    calculated_current, recommended_cable = calculate_cable_diameter(
        power_kw, voltage_v, phase_number, power_factor, input_amps=input_iga_a
    )
    st.write(f"Using provided Intensidad I.G.A.: **{input_iga_a:.2f} A**")
else:
    calculated_current, recommended_cable = calculate_cable_diameter(
        power_kw, voltage_v, phase_number, power_factor
    )
    st.write(f"Calculated Current (I): **{calculated_current:.2f} A**")


if recommended_cable:
    st.success(f"**Recommended Cable:**")
    st.write(f"**Cross-Sectional Area:** {recommended_cable['area_mm2']} mm²")
    st.write(f"**Approx. Overall Diameter:** {recommended_cable['diameter_mm']} mm")
    st.write(f"**Current Rating (3-phase):** {recommended_cable['three_phase_amps']} Amps")
    st.markdown(f"*(This cable can handle up to {recommended_cable['three_phase_amps']} Amps, which is sufficient for your calculated current of {calculated_current:.2f} A)*")
else:
    st.warning(f"Could not find a suitable cable for a current of {calculated_current:.2f} Amps with the available data.")
    st.info("Consider increasing the current capacity of the cables in the reference table or verify your input values.")

st.markdown("""
---
### Reference Tables:
* [Electrical Wiring Guide Cable Size Calculator Current Rating Chart Amps](https://smartshop.lk-ea.com/blog-articles/post/electrical-wiring-guide-cable-size-calculator-current-rating-chart-amps.html)
* [Cable Size Current Rating Chart](https://www.spwales.com/cable-size-current-rating-chart)
* [Table 4E1A](https://www.cse-distributors.co.uk/cable/technical-tables-useful-info/table-4e1a.html)
""")
