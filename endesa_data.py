# endesa_data.py

# --- Source Definitions ---
FUENTE_ENDESA_NRZ103_PG69_CONTRATACION = "Endesa Guía NRZ103, Pág. 69, 'POTENCIAS A CONTRATAR'"
FUENTE_ENDESA_NRZ103_PG54_IGM_REGLA = "Endesa Guía NRZ103, Pág. 54, 'Unidad IGM'"
FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS = "Endesa Guía NRZ103, Pág. 21, 'Tipos CGP'"
FUENTE_ENDESA_NRZ103_PG23_NEUTRO_REGLA = "Endesa Guía NRZ103, Pág. 23, 'Conductores LGA'"
FUENTE_ENDESA_NRZ103_PG22_LGA_LIMITE = "Endesa Guía NRZ103, Pág. 22, 'LGA'"

# --- Data Tables ---
endesa_contracted_power_data = [
    {"power_kw": {"valor": 3.46, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 5, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 40, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 5.19, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 7.5, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 6.92, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 10, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 10.39, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 15, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 13.85, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 20, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 17.32, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 25, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 20.78, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 30, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 24.24, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 35, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 27.71, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 40, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 31.17, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 45, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 34.64, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 50, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 43.64, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 63, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 55.42, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 80, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 100, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 69.30, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 100, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 100, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 88.60, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 125, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 160, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 103.92, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 150, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 160, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 138.60, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 200, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 250, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 173.20, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 250, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 250, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 207.84, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 300, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 400, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 218.30, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 315, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 400, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 277.10, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 400, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 400, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
    {"power_kw": {"valor": 346.40, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "base_contractual_a": {"valor": 500, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}, "nominal_protection_current_a": {"valor": 630, "fuente": FUENTE_ENDESA_NRZ103_PG69_CONTRATACION}},
]

endesa_cgp_types = [
    {"max_current_a": 100, "tipo": "BUC - esquema 7-100 A", "fuente": FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS},
    {"max_current_a": 160, "tipo": "BUC - esquema 7-160 A o 9-160 A", "fuente": FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS},
    {"max_current_a": 250, "tipo": "BUC - esquema 7-250 A o 9-250 A", "fuente": FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS},
    {"max_current_a": 400, "tipo": "BUC - esquema 7-400 A o 9-400 A", "fuente": FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS},
]

# --- Functions ---
def get_endesa_igm_capacity(power_kw):
    if power_kw <= 90:
        return {"valor": "160 A", "fuente": FUENTE_ENDESA_NRZ103_PG54_IGM_REGLA}
    elif power_kw <= 150:
        return {"valor": "250 A", "fuente": FUENTE_ENDESA_NRZ103_PG54_IGM_REGLA}
    else:
        return {"valor": "Consultar EDE (>400A)", "fuente": FUENTE_ENDESA_NRZ103_PG54_IGM_REGLA}

def get_endesa_cgp_type(nominal_current_a):
    for cgp in endesa_cgp_types:
        if nominal_current_a <= cgp["max_current_a"]:
            return cgp["tipo"], cgp["fuente"]
    return "N/A (Consultar EDE para >400A)", FUENTE_ENDESA_NRZ103_PG21_CGP_TIPOS
