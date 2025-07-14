import streamlit as st
import math

# --- Definiciones de Fuentes (para citaciones granulares) ---
FUENTE_ENDESA_NRZ103_PG69_CONTRATACION = "Endesa Guía NRZ103, Pág. 69, 'POTENCIAS A CONTRATAR'"
FUENTE_ENDESA_NRZ103_PG54_IGM_REGLA = "Endesa Guía NRZ103, Pág. 54, 'Unidad IGM'"
FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS = "Endesa Guía NRZ103, Pág. 21, 'Tipos CGP'"
FUENTE_ENDESA_NRZ103_PG23_NEUTRO_REGLA = "Endesa Guía NRZ103, Pág. 23, 'Conductores LGA'"
FUENTE_ENDESA_NRZ103_PG22_LGA_LIMITE = "Endesa Guía NRZ103, Pág. 22, 'LGA'"

FUENTE_UF_TABLA = "Tabla Unión Fenosa (Proporcionada por Usuario)"
FUENTE_UF_TABLA_SUELO = "Tabla Unión Fenosa (Proporcionada por Usuario)" # Específico para diferenciar si se usa solo para suelo

FUENTE_IBERDROLA_MT_PG17_TABLA1 = "Iberdrola MT 2.80.12, Pág. 17, 'Tabla 1'"
FUENTE_IBERDROLA_MT_PG19_IGM_REGLA = "Iberdrola MT 2.80.12, Pág. 19, 'Unidad IGM'"
FUENTE_IBERDROLA_NI_PG5_TABLA1 = "Iberdrola NI 76.50.01, Pág. 5, 'Tabla 1'"

FUENTE_GUIA_BT_14_PG9_TABLA1 = "GUÍA - BT-14, Pág. 9, 'Tabla 1'"
FUENTE_GUIA_BT_14_PG9_NEUTRO_REGLA = "GUÍA - BT-14, Pág. 9, 'Sección Conductor Neutro'" # Regla de 50% fase para neutro
FUENTE_GUIA_BT_14_GENERAL_REBT_TIERRA = "GUÍA - BT-14, Pág. 9 (Regla General REBT para PE)" # Regla general para tierra

FUENTE_GENERICO_CABLE = "Tabla General de Calibres de Cable"

# --- Datos para Compañías Distribuidoras (con citación granular) ---

# Datos de Endesa (NRZ103, Anexo Pág. 69)
endesa_contracted_power_data = [
    {"power_kw": {"valor": 3.46, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 5, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 5.19, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 7.5, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 6.92, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 10, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 10.39, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 15, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 13.85, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 20, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 17.32, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 25, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 20.78, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 30, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 24.24, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 35, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 27.71, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 40, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 31.17, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 45, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 34.64, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 50, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 43.64, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 55.42, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 80, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 100, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 69.30, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 100, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 100, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 88.60, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 125, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 160, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 103.92, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 150, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 160, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 138.60, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 200, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 250, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 173.20, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 250, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 250, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 207.84, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 300, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 400, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 218.30, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 315, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 400, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 277.10, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 400, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 400, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 346.40, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 500, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nom_int_a": {"valor": 630, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
]

# Regla de Dimensionamiento del IGM de Endesa (NRZ103, Pág. 54)
def get_endesa_igm_capacity(power_kw):
    if power_kw <= 90:
        return {"valor": "160 A", "fuente": FUENTE_ENDESA_NRZ103_PG54_IGM_REGLA}
    elif power_kw <= 150:
        return {"valor": "250 A", "fuente": FUENTE_ENDESA_NRZ103_PG54_IGM_REGLA}
    else:
        return {"valor": "Consultar EDE (>400A)", "fuente": FUENTE_ENDESA_NRZ103_PG54_IGM_REGLA}

# Mapeo de Tipos de CGP de Endesa (NRZ103, Pág. 21, Sección 5.4)
endesa_cgp_types = [
    {"max_current_a": 100, "tipo": "BUC - esquema 7-100 A", "fuente": FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS},
    {"max_current_a": 160, "tipo": "BUC - esquema 7-160 A o 9-160 A", "fuente": FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS},
    {"max_current_a": 250, "tipo": "BUC - esquema 7-250 A o 9-250 A", "fuente": FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS},
    {"max_current_a": 400, "tipo": "BUC - esquema 7-400 A o 9-400 A", "fuente": FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS},
]

# Datos de la Tabla de Unión Fenosa (proporcionada por el usuario)
ufd_table = [
    {"power_kw": {"valor": 24.9, "fuente": FUENTE_UF_TABLA}, "phase_mm2": {"valor": 10, "fuente": FUENTE_UF_TABLA}, "neutral_mm2": {"valor": 10, "fuente": FUENTE_UF_TABLA}, "ground_mm2": {"valor": 10, "fuente": FUENTE_UF_TABLA_SUELO}, "max_len_0_5": {"valor": 18, "fuente": FUENTE_UF_TABLA}, "max_len_1": {"valor": 35, "fuente": FUENTE_UF_TABLA}, "tube_dia_mm": {"valor": 75, "fuente": FUENTE_UF_TABLA}},
    {"power_kw": {"valor": 37.4, "fuente": FUENTE_UF_TABLA}, "phase_mm2": {"valor": 16, "fuente": FUENTE_UF_TABLA}, "neutral_mm2": {"valor": 10, "fuente": FUENTE_UF_TABLA}, "ground_mm2": {"valor": 10, "fuente": FUENTE_UF_TABLA_SUELO}, "max_len_0_5": {"valor": 12, "fuente": FUENTE_UF_TABLA}, "max_len_1": {"valor": 24, "fuente": FUENTE_UF_TABLA}, "tube_dia_mm": {"valor": 75, "fuente": FUENTE_UF_TABLA}},
    {"power_kw": {"valor": 50.5, "fuente": FUENTE_UF_TABLA}, "phase_mm2": {"valor": 16, "fuente": FUENTE_UF_TABLA}, "neutral_mm2": {"valor": 16, "fuente": FUENTE_UF_TABLA}, "ground_mm2": {"valor": 16, "fuente": FUENTE_UF_TABLA_SUELO}, "max_len_0_5": {"valor": 14, "fuente": FUENTE_UF_TABLA}, "max_len_1": {"valor": 28, "fuente": FUENTE_UF_TABLA}, "tube_dia_mm": {"valor": 75, "fuente": FUENTE_UF_TABLA}},
    {"power_kw": {"valor": 65.8, "fuente": FUENTE_UF_TABLA}, "phase_mm2": {"valor": 25, "fuente": FUENTE_UF_TABLA}, "neutral_mm2": {"valor": 16, "fuente": FUENTE_UF_TABLA}, "ground_mm2": {"valor": 16, "fuente": FUENTE_UF_TABLA_SUELO}, "max_len_0_5": {"valor": 17, "fuente": FUENTE_UF_TABLA}, "max_len_1": {"valor": 33, "fuente": FUENTE_UF_TABLA}, "tube_dia_mm": {"valor": 110, "fuente": FUENTE_UF_TABLA}},
    {"power_kw": {"valor": 82.4, "fuente": FUENTE_UF_TABLA}, "phase_mm2": {"valor": 35, "fuente": FUENTE_UF_TABLA}, "neutral_mm2": {"valor": 25, "fuente": FUENTE_UF_TABLA}, "ground_mm2": {"valor": 16, "fuente": FUENTE_UF_TABLA_SUELO}, "max_len_0_5": {"valor": 19, "fuente": FUENTE_UF_TABLA}, "max_len_1": {"valor": 37, "fuente": FUENTE_UF_TABLA}, "tube_dia_mm": {"valor": 110, "fuente": FUENTE_UF_TABLA}},
    {"power_kw": {"valor": 100.5, "fuente": FUENTE_UF_TABLA}, "phase_mm2": {"valor": 50, "fuente": FUENTE_UF_TABLA}, "neutral_mm2": {"valor": 25, "fuente": FUENTE_UF_TABLA}, "ground_mm2": {"valor": 25, "fuente": FUENTE_UF_TABLA_SUELO}, "max_len_0_5": {"valor": 22, "fuente": FUENTE_UF_TABLA}, "max_len_1": {"valor": 44, "fuente": FUENTE_UF_TABLA}, "tube_dia_mm": {"valor": 110, "fuente": FUENTE_UF_TABLA}},
    {"power_kw": {"valor": 128.2, "fuente": FUENTE_UF_TABLA}, "phase_mm2": {"valor": 70, "fuente": FUENTE_UF_TABLA}, "neutral_mm2": {"valor": 35, "fuente": FUENTE_UF_TABLA}, "ground_mm2": {"valor": 35, "fuente": FUENTE_UF_TABLA_SUELO}, "max_len_0_5": {"valor": 24, "fuente": FUENTE_UF_TABLA}, "max_len_1": {"valor": 48, "fuente": FUENTE_UF_TABLA}, "tube_dia_mm": {"valor": 125, "fuente": FUENTE_UF_TABLA}},
    {"power_kw": {"valor": 155.2, "fuente": FUENTE_UF_TABLA}, "phase_mm2": {"valor": 95, "fuente": FUENTE_UF_TABLA}, "neutral_mm2": {"valor": 50, "fuente": FUENTE_UF_TABLA}, "ground_mm2": {"valor": 50, "fuente": FUENTE_UF_TABLA_SUELO}, "max_len_0_5": {"valor": 27, "fuente": FUENTE_UF_TABLA}, "max_len_1": {"valor": 54, "fuente": FUENTE_UF_TABLA}, "tube_dia_mm": {"valor": 140, "fuente": FUENTE_UF_TABLA}},
    {"power_kw": {"valor": 180.1, "fuente": FUENTE_UF_TABLA}, "phase_mm2": {"valor": 120, "fuente": FUENTE_UF_TABLA}, "neutral_mm2": {"valor": 70, "fuente": FUENTE_UF_TABLA}, "ground_mm2": {"valor": 70, "fuente": FUENTE_UF_TABLA_SUELO}, "max_len_0_5": {"valor": 29, "fuente": FUENTE_UF_TABLA}, "max_len_1": {"valor": 59, "fuente": FUENTE_UF_TABLA}, "tube_dia_mm": {"valor": 140, "fuente": FUENTE_UF_TABLA}},
    {"power_kw": {"valor": 207.2, "fuente": FUENTE_UF_TABLA}, "phase_mm2": {"valor": 150, "fuente": FUENTE_UF_TABLA}, "neutral_mm2": {"valor": 95, "fuente": FUENTE_UF_TABLA}, "ground_mm2": {"valor": 95, "fuente": FUENTE_UF_TABLA_SUELO}, "max_len_0_5": {"valor": 32, "fuente": FUENTE_UF_TABLA}, "max_len_1": {"valor": 64, "fuente": FUENTE_UF_TABLA}, "tube_dia_mm": {"valor": 160, "fuente": FUENTE_UF_TABLA}},
    {"power_kw": {"valor": 236.3, "fuente": FUENTE_UF_TABLA}, "phase_mm2": {"valor": 185, "fuente": FUENTE_UF_TABLA}, "neutral_mm2": {"valor": 95, "fuente": FUENTE_UF_TABLA}, "ground_mm2": {"valor": 95, "fuente": FUENTE_UF_TABLA_SUELO}, "max_len_0_5": {"valor": 35, "fuente": FUENTE_UF_TABLA}, "max_len_1": {"valor": 69, "fuente": FUENTE_UF_TABLA}, "tube_dia_mm": {"valor": 180, "fuente": FUENTE_UF_TABLA}},
    {"power_kw": {"valor": 277.8, "fuente": FUENTE_UF_TABLA}, "phase_mm2": {"valor": 240, "fuente": FUENTE_UF_TABLA}, "neutral_mm2": {"valor": 150, "fuente": FUENTE_UF_TABLA}, "ground_mm2": {"valor": 150, "fuente": FUENTE_UF_TABLA_SUELO}, "max_len_0_5": {"valor": 38, "fuente": FUENTE_UF_TABLA}, "max_len_1": {"valor": 76, "fuente": FUENTE_UF_TABLA}, "tube_dia_mm": {"valor": 200, "fuente": FUENTE_UF_TABLA}},
]

# Datos de la Tabla IDE de Iberdrola (MT 2.80.12, Pág. 17, Tabla 1)
iberdrola_ide_table = [
    {"power_kw": {"valor": 3, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "phase_mm2": {"valor": 9, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "neutral_mm2": {"valor": 16, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "ground_mm2": {"valor": 10, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_0_5": {"valor": 101, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_1": {"valor": 428, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "tube_dia_mm": {"valor": 75, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "cgp_amp_range": {"valor": "63", "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "conductor_amp_rating": {"valor": 63, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}},
    {"power_kw": {"valor": 50, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "phase_mm2": {"valor": 25, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "neutral_mm2": {"valor": 16, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "ground_mm2": {"valor": 16, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_0_5": {"valor": 17, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_1": {"valor": 33, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "tube_dia_mm": {"valor": 110, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "cgp_amp_range": {"valor": "80", "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "conductor_amp_rating": {"valor": 80, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}},
    {"power_kw": {"valor": 78, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "phase_mm2": {"valor": 50, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "neutral_mm2": {"valor": 25, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "ground_mm2": {"valor": 25, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_0_5": {"valor": 20, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_1": {"valor": 41, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "tube_dia_mm": {"valor": 125, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "cgp_amp_range": {"valor": "125", "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "conductor_amp_rating": {"valor": 125, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}},
    {"power_kw": {"valor": 125, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "phase_mm2": {"valor": 95, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "neutral_mm2": {"valor": 50, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "ground_mm2": {"valor": 50, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_0_5": {"valor": 22, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_1": {"valor": 44, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "tube_dia_mm": {"valor": 140, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "cgp_amp_range": {"valor": "200", "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "conductor_amp_rating": {"valor": 200, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}},
    {"power_kw": {"valor": 156, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "phase_mm2": {"valor": 150, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "neutral_mm2": {"valor": 95, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "ground_mm2": {"valor": 95, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_0_5": {"valor": 27, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_1": {"valor": 53, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "tube_dia_mm": {"valor": 180, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "cgp_amp_range": {"valor": "250-400", "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "conductor_amp_rating": {"valor": 250, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}},
    {"power_kw": {"valor": 196, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "phase_mm2": {"valor": 240, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "neutral_mm2": {"valor": 150, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "ground_mm2": {"valor": 150, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_0_5": {"valor": 29, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_1": {"valor": 57, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "tube_dia_mm": {"valor": 225, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "cgp_amp_range": {"valor": "400", "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "conductor_amp_rating": {"valor": 315, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}},
]

# Tipos de CGP de Iberdrola (NI 76.50.01, Pág. 5, Tabla 1)
iberdrola_cgp_types = [
    {"max_fuse_a": 100, "tipo": "CGP-1-100/BUC, CGP-7-100/BUC", "fuente": FUENTE_IBERDROLA_NI_PG5_TABLA1},
    {"max_fuse_a": 160, "tipo": "CGP-7-160/BUC", "fuente": FUENTE_IBERDROLA_NI_PG5_TABLA1},
    {"max_fuse_a": 250, "tipo": "CGP-7-250/BUC, CGP-9-250/BUC, CGP-10-250/BUC, CGP-11-250/BUC", "fuente": FUENTE_IBERDROLA_NI_PG5_TABLA1},
    {"max_fuse_a": 400, "tipo": "CGP-7-400/BUC, CGP-9-400/BUC", "fuente": FUENTE_IBERDROLA_NI_PG5_TABLA1},
]

# GUIA - BT-14 Tabla 1 (Pág. 9) - Secciones generales y diámetros de tubo para LGA
guia_bt_14_table_1 = [
    {"power_kw_ref": 10, "phase_mm2_cu": 10, "neutral_mm2": 10, "tube_dia_mm": 75, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1},
    {"power_kw_ref": 16, "phase_mm2_cu": 16, "neutral_mm2": 10, "tube_dia_mm": 75, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1},
    {"power_kw_ref": 16, "phase_mm2_al": 16, "neutral_mm2": 16, "tube_dia_mm": 75, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, # Opción de Aluminio
    {"power_kw_ref": 25, "phase_mm2_cu": 25, "neutral_mm2": 16, "tube_dia_mm": 110, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1},
    {"power_kw_ref": 35, "phase_mm2_cu": 35, "neutral_mm2": 16, "tube_dia_mm": 110, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1},
    {"power_kw_ref": 50, "phase_mm2_cu": 50, "neutral_mm2": 25, "tube_dia_mm": 125, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1},
    {"power_kw_ref": 70, "phase_mm2_cu": 70, "neutral_mm2": 35, "tube_dia_mm": 140, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1},
    {"power_kw_ref": 95, "phase_mm2_cu": 95, "neutral_mm2": 50, "tube_dia_mm": 140, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1},
    {"power_kw_ref": 120, "phase_mm2_cu": 120, "neutral_mm2": 70, "tube_dia_mm": 160, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1},
    {"power_kw_ref": 150, "phase_mm2_cu": 150, "neutral_mm2": 70, "tube_dia_mm": 160, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1},
    {"power_kw_ref": 185, "phase_mm2_cu": 185, "neutral_mm2": 95, "tube_dia_mm": 180, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1},
    {"power_kw_ref": 240, "phase_mm2_cu": 240, "neutral_mm2": 120, "tube_dia_mm": 200, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1},
]


# Búsqueda de Diámetro de Cable Genérico - Usado como respaldo o para derivar el diámetro de la sección
generic_cable_diameter_data = [
    {"area_mm2": {"valor": 1.5, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 2.9, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 15.5, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 2.5, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 3.5, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 21, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 4, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 4.4, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 28, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 6, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 4.6, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 36, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 10, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 5.9, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 50, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 16, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 6.9, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 68, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 25, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 8.7, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 89, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 35, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 10.0, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 110, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 50, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 11.8, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 134, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 70, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 13.5, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 171, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 95, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 15.7, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 207, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 120, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 17.4, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 239, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 150, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 19.3, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 262, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 185, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 21.5, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 296, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 240, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 24.6, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 346, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 300, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 27.9, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 394, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 400, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 30.8, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 467, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 500, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 33.8, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 533, "fuente": FUENTE_GENERICO_CABLE}},
    {"area_mm2": {"valor": 630, "fuente": FUENTE_GENERICO_CABLE}, "diameter_mm": {"valor": 37.6, "fuente": FUENTE_GENERICO_CABLE}, "three_phase_amps": {"valor": 611, "fuente": FUENTE_GENERICO_CABLE}},
]

# --- Funciones Auxiliares ---

def find_data_by_power(power_kw, data_table):
    """Encuentra la fila de datos apropiada en una tabla de compañía específica basada en la potencia.
    Asume que la tabla está ordenada por power_kw de forma ascendente.
    Devuelve la fila donde power_kw del usuario es <= power_kw de la fila."""
    for row in data_table:
        # Acceder al valor numérico de power_kw dentro del diccionario anidado
        if power_kw <= row["power_kw"]["valor"]:
            return row
    # Si la potencia supera todos los valores listados, devuelve el último elemento o None si la tabla está vacía
    return data_table[-1] if data_table else None

def get_endesa_cgp_type(nominal_current_a):
    """Obtiene el tipo específico de CGP de Endesa basado en la corriente nominal."""
    for cgp in endesa_cgp_types:
        if nominal_current_a <= cgp["max_current_a"]:
            return cgp["tipo"], cgp["fuente"] # Devuelve el tipo y la fuente
    return "N/A (Consultar EDE para >400A)", FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS

def get_iberdrola_cgp_type(max_fuse_a):
    """Obtiene el tipo específico de CGP de Iberdrola basado en la corriente máxima del fusible."""
    for cgp in iberdrola_cgp_types:
        if max_fuse_a <= cgp["max_fuse_a"]:
            return cgp["tipo"], cgp["fuente"] # Devuelve el tipo y la fuente
    return "N/A (Consultar i-DE para >400A)", FUENTE_IBERDROLA_NI_PG5_TABLA1

def get_guia_bt_14_ground_size_by_phase(phase_mm2_ref):
    """Estima la sección del conductor de tierra según GUÍA BT-14, Pág. 9 (regla general REBT para PE).
    La GUÍA BT-14 se refiere a la ITC-BT-18 para PE sizing. Regla común es 50% de fase, mínimo 16mm2 si fase > 35mm2.
    O 100% de fase si fase <= 16mm2."""
    if not isinstance(phase_mm2_ref, (int, float)):
        return "N/A"

    # Regla simplificada basada en ITC-BT-18 y prácticas comunes:
    if phase_mm2_ref <= 16:
        return phase_mm2_ref # O 10mm2 como mínimo absoluto, pero por simplicidad se usa el mismo.
    elif phase_mm2_ref <= 35: # Ej: fase 25 o 35mm2, tierra 16mm2
        return 16
    else: # Fase > 35mm2, tierra = 0.5 * fase, no menor que 16mm2
        return max(16, math.ceil(phase_mm2_ref / 2)) # Redondea hacia arriba al entero más cercano


def get_generic_diameter_from_area(area_mm2):
    """Encuentra el diámetro total aproximado para un área de sección transversal dada."""
    if not isinstance(area_mm2, (int, float)):
        return {"valor": "N/A", "fuente": FUENTE_GENERICO_CABLE}

    for cable in generic_cable_diameter_data:
        if cable["area_mm2"]["valor"] == area_mm2: # Acceder al valor numérico
            return {"valor": cable["diameter_mm"]["valor"], "fuente": cable["diameter_mm"]["fuente"]}
    return {"valor": "N/A", "fuente": FUENTE_GENERICO_CABLE}


def calculate_current(power_kw, voltage_v, phase_number, power_factor):
    """Calcula la corriente (I_B) basada en la potencia, voltaje, fase y factor de potencia."""
    if voltage_v == 0 or power_factor == 0:
        return 0 

    power_w = power_kw * 1000 
    if phase_number == 3:
        # Formula for 3-phase: I = P / (sqrt(3) * V * PF)
        return power_w / (math.sqrt(3) * voltage_v * power_factor)
    elif phase_number == 1:
        # Formula for 1-phase: I = P / (V * PF)
        return power_w / (voltage_v * power_factor)
    return 0

# --- Diseño y Lógica de la Aplicación Streamlit ---

st.set_page_config(page_title="Generador de Guía de Instalaciones Eléctricas", layout="centered")

st.title("⚡ Generador de Guía de Instalaciones Eléctricas")
st.markdown("Genere requisitos eléctricos detallados según las normas de las compañías distribuidoras.")

# --- Sección de Entrada ---
st.header("Parámetros de Entrada")

col1, col2 = st.columns(2)
with col1:
    company = st.selectbox(
        "Seleccione Compañía Distribuidora",
        options=["Endesa", "Iberdrola", "Unión Fenosa"],
        index=0, # Por defecto Endesa
        help="Elija la compañía distribuidora de electricidad para obtener regulaciones específicas."
    )
    power_kw = st.number_input(
        "Potencia Máxima Contratada (kW)",
        min_value=0.0, value=100.0, step=1.0,
        help="La potencia eléctrica máxima (en kilovatios) prevista para la instalación, según contrato."
    )
    voltage_v = st.number_input(
        "Tensión Nominal de Red (V)",
        min_value=0.0, value=400.0, step=1.0,
        help="Normalmente 400V para trifásica, 230V para monofásica en España."
    )

with col2:
    phase_number = st.selectbox(
        "Número de Fases",
        options=[1, 3],
        index=1, # Por defecto 3-fases
        help="Seleccione si el sistema es monofásico o trifásico."
    )
    load_factor = st.slider(
        "Factor de Carga (Factor de Potencia)",
        min_value=0.8, max_value=1.0, value=0.9, step=0.01,
        help="También conocido como Factor de Potencia (cos phi). Representa la eficiencia de la utilización de energía."
    )
    voltage_drop_limit = st.slider(
        "Límite de Caída de Tensión (%)",
        min_value=0.5, max_value=5.0, value=0.5, step=0.1,
        help="Caída de tensión máxima permitida en la instalación, según la normativa."
    )

st.info("También puede introducir directamente la corriente de diseño si la conoce (anula el cálculo de potencia).")
input_design_current_a = st.number_input(
    "Corriente de Diseño Calculada (A) (Opcional)",
    min_value=0.0, value=0.0, step=1.0,
    help="Si se proporciona y es mayor que 0, esta corriente se utilizará directamente para fines de dimensionamiento."
)


# --- Cálculos y Lógica ---
st.header("Requisitos Generados")

selected_company_data = None
uf_ref_data_for_ground = None # Para almacenar datos de UF para referencia de conductor de tierra para Endesa

# Seleccionar la tabla de la compañía apropiada
if company == "Endesa":
    selected_company_data = find_data_by_power(power_kw, endesa_contracted_power_data)
    # Para Endesa, referenciamos datos de Unión Fenosa para el dimensionamiento del cable de tierra,
    # ya que la tabla de Endesa no lo proporciona explícitamente.
    uf_ref_data_for_ground = find_data_by_power(power_kw, ufd_table)
    if power_kw > 346.40:
         st.warning(f"Para potencias contratadas superiores a 346.40 kW con Endesa, consulte la documentación oficial de Endesa para requisitos específicos.")

elif company == "Unión Fenosa":
    selected_company_data = find_data_by_power(power_kw, ufd_table)
    if power_kw > 277.8:
        st.warning(f"Para potencias contratadas superiores a 277.8 kW con Unión Fenosa, consulte la documentación oficial de Unión Fenosa para requisitos específicos.")

elif company == "Iberdrola":
    selected_company_data = find_data_by_power(power_kw, iberdrola_ide_table)
    if power_kw > 196:
        st.warning(f"Para potencias contratadas superiores a 196 kW con Iberdrola, consulte la documentación oficial de Iberdrola (MT 2.80.12) para requisitos específicos.")


# Determinar la corriente (I_B) a utilizar para el dimensionamiento
if input_design_current_a > 0:
    calculated_current = input_design_current_a
    st.write(f"Utilizando Corriente de Diseño proporcionada: **{calculated_current:.2f} A**")
else:
    calculated_current = calculate_current(power_kw, voltage_v, phase_number, load_factor)
    st.write(f"Corriente de Diseño Calculada (I_B) según las entradas: **{calculated_current:.2f} A**")


if selected_company_data:
    st.subheader(f"Requisitos para {company} (Basado en {power_kw} kW de Potencia Contratada)")

    # --- Secciones de Cables ---
    st.markdown("#### Secciones de Cables (mm²)")
    
    phase_mm2 = {"valor": "N/A", "fuente": "N/A"}
    neutral_mm2 = {"valor": "N/A", "fuente": "N/A"}
    ground_mm2 = {"valor": "N/A", "fuente": "N/A"}
    overall_cable_diameter_info = {"valor": "N/A", "fuente": "N/A"}

    if company == "Endesa":
        # Para Endesa, derivamos las secciones de cable de la corriente nominal encontrada en la tabla.
        required_nom_int_val = selected_company_data['nom_int_a']['valor']
        found_generic_cable_for_nom_int = None
        for cable in generic_cable_diameter_data:
            if cable["three_phase_amps"]["valor"] >= required_nom_int_val:
                found_generic_cable_for_nom_int = cable
                break

        if found_generic_cable_for_nom_int:
            phase_mm2 = found_generic_cable_for_nom_int['area_mm2']
            neutral_mm2 = {"valor": phase_mm2['valor'], "fuente": FUENTE_ENDESA_NRZ103_PG23_NEUTRO_REGLA} # Neutro igual a fase para Endesa

            # Tierra para Endesa: Priorizar UF, luego GUIA BT-14 (regla general REBT para PE)
            if uf_ref_data_for_ground and uf_ref_data_for_ground.get('ground_mm2'):
                ground_mm2 = uf_ref_data_for_ground['ground_mm2']
                ground_mm2['fuente'] = FUENTE_UF_TABLA_SUELO # Asegurar la fuente correcta
            else:
                ground_mm2_valor_fallback = get_guia_bt_14_ground_size_by_phase(phase_mm2['valor'])
                ground_mm2 = {"valor": ground_mm2_valor_fallback, "fuente": FUENTE_GUIA_BT_14_GENERAL_REBT_TIERRA}
                
            st.write(f"- **Sección de Cable de Fase:** {phase_mm2['valor']} mm²}]")
            st.write(f"- **Sección de Neutro:** {neutral_mm2['valor']} mm²}]")
            st.write(f"- **Sección de Conductor de Protección (Tierra):** {ground_mm2['valor']} mm²}]")
            st.info("*(Nota: Para Endesa, la sección del Neutro se recomienda igual a la de Fase (NRZ103). La sección de Tierra se deriva de una tabla de referencia general (GUÍA BT-14) o de Unión Fenosa, ya que las tablas primarias de Endesa no la especifican explícitamente.)*")
            
            if isinstance(phase_mm2['valor'], (int, float)):
                overall_cable_diameter_info = get_generic_diameter_from_area(phase_mm2['valor'])
            st.write(f"- **Diámetro Total Aproximado del Cable:** {overall_cable_diameter_info['valor']} mm (Basado en la Sección de Fase)}]")
        else:
            st.write("- **Secciones de Cable:** No determinadas con los datos disponibles. Consulte la documentación de Endesa.")

    else: # Para Unión Fenosa e Iberdrola (ya que sus tablas tienen secciones explícitas)
        phase_mm2 = selected_company_data.get('phase_mm2', {"valor": "N/A", "fuente": "N/A"})
        neutral_mm2 = selected_company_data.get('neutral_mm2', {"valor": "N/A", "fuente": "N/A"})
        ground_mm2 = selected_company_data.get('ground_mm2', {"valor": "N/A", "fuente": "N/A"})
        
        st.write(f"- **Sección de Cable de Fase:** {phase_mm2['valor']} mm²}]")
        st.write(f"- **Sección de Neutro:** {neutral_mm2['valor']} mm²}]")
        st.write(f"- **Sección de Conductor de Protección (Tierra):** {ground_mm2['valor']} mm²}]")
        
        if isinstance(phase_mm2['valor'], (int, float)):
            overall_cable_diameter_info = get_generic_diameter_from_area(phase_mm2['valor'])
        st.write(f"- **Diámetro Total Aproximado del Cable:** {overall_cable_diameter_info['valor']} mm (Basado en la Sección de Fase)}]")

    # --- Detalles de Instalación ---
    st.markdown("#### Detalles de Instalación")
    tube_dia_mm_info = selected_company_data.get('tube_dia_mm', {"valor": "N/A", "fuente": "N/A"})
    st.write(f"- **Diámetro Mínimo del Tubo:** {tube_dia_mm_info['valor']} mm}]")

    # Límites de Caída de Tensión y Longitud Máxima
    max_len_0_5_info = selected_company_data.get('max_len_0_5', {"valor": "N/A", "fuente": "N/A"})
    max_len_1_info = selected_company_data.get('max_len_1', {"valor": "N/A", "fuente": "N/A"})

    if max_len_0_5_info['valor'] != "N/A" and max_len_1_info['valor'] != "N/A":
        if voltage_drop_limit <= 0.5:
             st.write(f"- **Longitud Máxima Recomendada (para {voltage_drop_limit:.1f}% de caída de tensión):** {max_len_0_5_info['valor']} m}]")
        elif voltage_drop_limit <= 1.0:
            st.write(f"- **Longitud Máxima Recomendada (para {voltage_drop_limit:.1f}% de caída de tensión):** {max_len_1_info['valor']} m}]")
        else:
            st.write(f"- **Longitud Máxima @ 0.5% Caída de Tensión:** {max_len_0_5_info['valor']} m}]")
            st.write(f"- **Longitud Máxima @ 1.0% Caída de Tensión:** {max_len_1_info['valor']} m}]")
            st.info("*(Nota: Para límites de caída de tensión superiores al 1.0%, es posible que deba consultar las guías específicas de la compañía para longitudes mayores.)*")
    else:
        st.info(f"Datos de longitud máxima para {company} no disponibles directamente en la tabla seleccionada para varias caídas de tensión.")


    # --- Dispositivos Eléctricos y Capacidades ---
    st.markdown("#### Dispositivos Eléctricos y Capacidades")

    # CGP (Caja General de Protección) y Fusible/Interruptor Lógica
    if company == "Endesa":
        # Capacidad IGM (de Endesa NRZ103 Pág. 54)
        igm_capacity_info = get_endesa_igm_capacity(power_kw)
        st.write(f"- **Capacidad del Interruptor General de Maniobra (IGM):** {igm_capacity_info['valor']}}]")
        if power_kw > 150:
            st.info("*(Nota: Para potencias contratadas superiores a 150kW con Endesa, la capacidad del IGM requiere acuerdo con Endesa.)*")

        # Tipo de CGP (de Endesa NRZ103 Pág. 21)
        nominal_current_for_cgp = selected_company_data.get('nom_int_a', {"valor": 0})['valor']
        cgp_type, cgp_source = get_endesa_cgp_type(nominal_current_for_cgp)
        st.write(f"- **Tipo de CGP (Caja General de Protección):** {cgp_type}")

        # Capacidad de Fusible/Interruptor (de Endesa NRZ103 Pág. 69, 'nom_int_a')
        fuse_breaker_capacity_info = selected_company_data.get('nom_int_a', {"valor": "N/A", "fuente": "N/A"})
        st.write(f"- **Capacidad de Fusible Recomendada:** {fuse_breaker_capacity_info['valor']} A}]")
        st.write(f"- **Capacidad de Interruptor Recomendada:** {fuse_breaker_capacity_info['valor']} A}]")
        st.info("*(Nota: Las capacidades de Fusibles e Interruptores para Endesa se basan típicamente en la 'Intensidad Nominal' de la tabla de potencia contratada.)*")

        # Verificación de Capacidad de LGA (Endesa NRZ103 Pág. 22)
        lga_max_current = 250 # Capacidad máxima típica
        if calculated_current > lga_max_current:
            st.warning(f"La capacidad máxima de LGA para Endesa es típicamente 250A. Su corriente calculada ({calculated_current:.2f} A) excede esto. Consulte a Endesa para excepciones de hasta 400A.")


    elif company == "Iberdrola": # Lógica específica para Iberdrola basada en MT 2.80.12 y NI 76.50.01
        # Capacidad IGM (de MT 2.80.12 Pág. 19, misma regla que Endesa)
        igm_capacity_info = get_endesa_igm_capacity(power_kw) # Reutilizando esta función ya que la regla es idéntica
        st.write(f"- **Capacidad del Interruptor General de Maniobra (IGM):** {igm_capacity_info['valor']}}]")
        if power_kw > 150:
            st.info("*(Nota: Para potencias contratadas superiores a 150kW con Iberdrola, la capacidad del IGM requiere acuerdo con i-DE.)*")

        # Tipo de CGP para Iberdrola (de NI 76.50.01 Tabla 1)
        max_fuse_for_cgp = selected_company_data.get('conductor_amp_rating', {"valor": 0})['valor']
        cgp_type, cgp_source = get_iberdrola_cgp_type(max_fuse_for_cgp)
        st.write(f"- **Tipo de CGP (Caja General de Protección):** {cgp_type}")
        st.info("*(Nota: Para Iberdrola, el tipo de CGP se deriva de la corriente máxima del fusible (Intensidad nominal CGP) en NI 76.50.01 Tabla 1.)*")

        # Capacidad de Fusible/Interruptor para Iberdrola (de MT 2.80.12 Tabla 1, columna "Intensidad nominal CGP")
        fuse_breaker_capacity_info = selected_company_data.get('conductor_amp_rating', {"valor": "N/A", "fuente": "N/A"})
        st.write(f"- **Capacidad de Fusible Recomendada:** {fuse_breaker_capacity_info['valor']} A}]")
        st.write(f"- **Capacidad de Interruptor Recomendada:** {fuse_breaker_capacity_info['valor']} A}]")
        st.info("*(Nota: Las capacidades de Fusibles e Interruptores para Iberdrola se basan típicamente en la 'Intensidad nominal CGP' de MT 2.80.12 Tabla 1.)*")
        
        # Capacidad de LGA (MT 2.80.12 Pág. 17, Tabla 1 sugiere 400A es el máximo en tabla)
        if calculated_current > 400: # Valor máximo en su tabla 1 para CGP
             st.warning(f"La capacidad máxima de LGA para Iberdrola es típicamente de hasta 400A. Su corriente calculada ({calculated_current:.2f} A) excede esto. Consulte a i-DE para requisitos específicos para corrientes más altas.")


    elif company == "Unión Fenosa": # Lógica existente para Union Fenosa
        # Para Unión Fenosa, usamos el 'conductor_amp_rating' o el respaldo calculado.
        fuse_breaker_capacity_info = selected_company_data.get('conductor_amp_rating', {"valor": "N/A", "fuente": "N/A"})
        if fuse_breaker_capacity_info['valor'] != "N/A":
            st.write(f"- **Capacidad de Fusible Recomendada:** {fuse_breaker_capacity_info['valor']} A}]")
            st.write(f"- **Capacidad de Interruptor Recomendada:** {fuse_breaker_capacity_info['valor']} A}]")
            st.info("*(Nota: Las capacidades de Fusibles e Interruptores para esta compañía se basan en valores de tabla específicos.)*")
        else:
            st.write(f"- **Capacidad de Fusible Recomendada (Mín.):** Aprox. {calculated_current * 1.25:.2f} A (requiere consulta a tabla específica de la compañía)")
            st.write(f"- **Capacidad de Interruptor Recomendada (Mín.):** Aprox. {calculated_current * 1.25:.2f} A (requiere consulta a tabla específica de la compañía)")
            st.info("*(Nota: Las capacidades de Fusibles/Interruptores no están directamente en la tabla proporcionada por esta compañía; se utiliza una regla de dimensionamiento general como marcador de posición.)*")
        
        cgp_info = selected_company_data.get('cgp_amp_range', {"valor": "N/A", "fuente": "N/A"})
        if cgp_info['valor'] != "N/A":
            st.write(f"- **Tipo de CGP (Caja General de Protección):** Relacionado con **{cgp_info['valor']} Amps**}]")
        else:
            st.write("- **Tipo de CGP (Caja General de Protección):** Información no disponible directamente en la tabla de esta compañía.")


else: # Si no se encuentran datos para la compañía y potencia seleccionadas
    st.warning(f"No se encontraron datos específicos para {company} para una potencia contratada de {power_kw} kW. Por favor, verifique la potencia de entrada o consulte las tablas oficiales de la compañía.")
    
    # Respaldo a la recomendación de cable genérico basado en la corriente calculada
    found_generic_cable = None
    for cable in generic_cable_diameter_data:
        if cable["three_phase_amps"]["valor"] >= calculated_current:
            found_generic_cable = cable
            break
    if found_generic_cable:
        st.markdown("#### Recomendación Genérica de Cable (Respaldo)")
        st.write(f"- **Área de Sección Transversal de Cable Requerida (aprox.):** {found_generic_cable['area_mm2']['valor']} mm²['fuente']}]")
        st.write(f"- **Diámetro Total Aproximado del Cable:** {found_generic_cable['diameter_mm']['valor']} mm (Basado en la Sección de Fase)['fuente']}]")
        st.write(f"*(Basado en la corriente calculada {calculated_current:.2f} A)*")
    else:
        st.error("No se encontró un cable genérico adecuado para la corriente calculada en los datos disponibles.")


st.markdown("""
---
### Documentos de Referencia:
* **Endesa:** [Guía de Interpretación NRZ103, Edición 6.1, 03-2024]
    * [**Enlace a Google Drive:** (Añada aquí su enlace al PDF de Endesa NRZ103)]
* **Unión Fenosa:** [Referencia de tabla proporcionada por el usuario]
    * [**Enlace a Google Drive:** (Añada aquí su enlace a la tabla/documento de Unión Fenosa)]
* **Iberdrola (i-DE):** [Manual Técnico de Distribución MT 2.80.12, Edición 05, Mayo 2019]
    * [**Enlace a Google Drive:** (Añada aquí su enlace al PDF de Iberdrola MT 2.80.12)]
* **Iberdrola (i-DE) Tipos de CGP:** [NORMA NI 76.50.01, Edición 6a, Julio 2010]
    * [**Enlace a Google Drive:** (Añada aquí su enlace al PDF de Iberdrola NI 76.50.01)]
* **Guía Técnica de Aplicación:** [GUÍA - BT-14, Ministerio de Ciencia y Tecnología, Edición: sep 03, Revisión: 1]
    * [**Enlace a Google Drive:** (Añada aquí su enlace al PDF de GUÍA - BT-14)]
* **Tablas Generales de Calibre de Cable:**
    * [Tabla 1]: https://smartshop.lk-ea.com/blog-articles/post/electrical-wiring-guide-cable-size-calculator-current-rating-chart-amps.html
    * [Tabla 2]: https://www.spwales.com/cable-size-current-rating-chart
    * [Tabla 3]: https://www.cse-distributors.co.uk/cable/technical-tables-useful-info/table-4e1a.html
""")
