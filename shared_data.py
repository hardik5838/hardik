# shared_data.py

# --- Source Definitions ---
FUENTE_GUIA_BT_14_PG9_TABLA1 = "GUÍA - BT-14, Pág. 9, 'Tabla 1'"
FUENTE_GUIA_BT_15_PG56_TABLA14 = "GUÍA - BT-15, Pág. 56, 'Tabla 14 PE'"
FUENTE_GENERICO_CABLE = "Tabla General de Calibres de Cable"

# --- Data Tables ---
guia_bt_14_table_1 = [
    {"phase_mm2_cu": {"valor": 10, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "neutral_mm2": {"valor": 10, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "tube_dia_mm": {"valor": 75, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}},
    {"phase_mm2_cu": {"valor": 16, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "neutral_mm2": {"valor": 10, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "tube_dia_mm": {"valor": 75, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}},
    {"phase_mm2_cu": {"valor": 25, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "neutral_mm2": {"valor": 16, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "tube_dia_mm": {"valor": 110, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}},
    {"phase_mm2_cu": {"valor": 35, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "neutral_mm2": {"valor": 16, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "tube_dia_mm": {"valor": 110, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}},
    {"phase_mm2_cu": {"valor": 50, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "neutral_mm2": {"valor": 25, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "tube_dia_mm": {"valor": 125, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}},
    {"phase_mm2_cu": {"valor": 70, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "neutral_mm2": {"valor": 35, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "tube_dia_mm": {"valor": 140, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}},
    {"phase_mm2_cu": {"valor": 95, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "neutral_mm2": {"valor": 50, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "tube_dia_mm": {"valor": 140, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}},
    {"phase_mm2_cu": {"valor": 120, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "neutral_mm2": {"valor": 70, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "tube_dia_mm": {"valor": 160, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}},
    {"phase_mm2_cu": {"valor": 150, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "neutral_mm2": {"valor": 70, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "tube_dia_mm": {"valor": 160, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}},
    {"phase_mm2_cu": {"valor": 185, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "neutral_mm2": {"valor": 95, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "tube_dia_mm": {"valor": 180, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}},
    {"phase_mm2_cu": {"valor": 240, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "neutral_mm2": {"valor": 120, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}, "tube_dia_mm": {"valor": 200, "fuente": FUENTE_GUIA_BT_14_PG9_TABLA1}},
]

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
