import streamlit as st
import math

# --- Data for Distribution Companies (Parsed from your Excel and Endesa NRZ103) ---

# Endesa NRZ103 Annex Table (Page 69) - Main reference for Endesa
# Potencia prevista (kW) for 400V 3-phase, corresponding Nominal Current (A) for Main Breaker/Fuse
endesa_contracted_power_data = [
    # Power_kW, Base_Contractual_A, Nom_Int_A
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

# Endesa NRZ103 IGM Sizing Rule (Page 54)
def get_endesa_igm_capacity(power_kw):
    if power_kw <= 90:
        return "160 A"
    elif power_kw <= 150:
        return "250 A"
    else:
        return "Appropriate switch/disconnector (consult EDE for >400A)"

# Endesa NRZ103 CGP Type Mapping (Page 21, Section 5.4)
endesa_cgp_types = [
    {"max_current_a": 100, "type": "BUC - esquema 7-100 A"},
    {"max_current_a": 160, "type": "BUC - esquema 7-160 A or 9-160 A"},
    {"max_current_a": 250, "type": "BUC - esquema 7-250 A or 9-250 A"},
    {"max_current_a": 400, "type": "BUC - esquema 7-400 A or 9-400 A"},
]

# Union Fenosa (ufd) Table Data
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

# Iberdrola (IDE) Table Data
iberdrola_ide_table = [
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
    {"power_kw": 315, "phase_mm2": 225, "neutral_mm2": 225, "ground_mm2": 225, "max_len_0_5":
