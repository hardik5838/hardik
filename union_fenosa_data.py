# union_fenosa_data.py

# --- Source Definitions ---
FUENTE_UF_TABLA = "Tabla Unión Fenosa (Proporcionada por Usuario)"
FUENTE_UF_TABLA_SUELO = "Tabla Unión Fenosa (Proporcionada por Usuario)"
FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2 = "Unión Fenosa ES.0100.ES.RE.EIC, Pág. 14, 'Tabla 2 CGP'"

# --- Data Tables ---
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

uf_cgp_fuse_data = [
    {"designacion": {"valor": "CGP1-100-/BUC", "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}, "imax_a": {"valor": 100, "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}, "potencia_disipada_w": {"valor": 7, "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}},
    {"designacion": {"valor": "CGP-7-160/BUC", "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}, "imax_a": {"valor": 160, "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}, "potencia_disipada_w": {"valor": 12, "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}},
    {"designacion": {"valor": "CGP-7-250/BUC", "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}, "imax_a": {"valor": 250, "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}, "potencia_disipada_w": {"valor": 20, "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}},
    {"designacion": {"valor": "CGP-7-400/BUC", "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}, "imax_a": {"valor": 400, "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}, "potencia_disipada_w": {"valor": 30, "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}},
    {"designacion": {"valor": "CGP-9-250/BUC", "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}, "imax_a": {"valor": 250, "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}, "potencia_disipada_w": {"valor": 20, "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}},
    {"designacion": {"valor": "CGP-9-400/BUC", "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}, "imax_a": {"valor": 400, "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}, "potencia_disipada_w": {"valor": 30, "fuente": FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2}},
]

# --- Functions ---
def get_uf_cgp_type_and_fuse(nominal_current_a):
    for cgp_entry in uf_cgp_fuse_data:
        if nominal_current_a <= cgp_entry["imax_a"]["valor"]:
            return cgp_entry["designacion"]["valor"], cgp_entry["imax_a"]["valor"], cgp_entry["designacion"]["fuente"]
    return "N/A (Consultar UF Dist.)", "N/A", FUENTE_UF_ES_0100_ES_RE_EIC_PG14_TABLA2
