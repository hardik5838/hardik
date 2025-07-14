# iberdrola_data.py

# --- Source Definitions ---
FUENTE_IBERDROLA_MT_PG17_TABLA1 = "Iberdrola MT 2.80.12, Pág. 17, 'Tabla 1'"
FUENTE_IBERDROLA_MT_PG19_IGM_REGLA = "Iberdrola MT 2.80.12, Pág. 19, 'Unidad IGM'"
FUENTE_IBERDROLA_NI_PG5_TABLA1 = "Iberdrola NI 76.50.01, Pág. 5, 'Tabla 1'"

# --- Data Tables ---
iberdrola_ide_table = [
    {"power_kw": {"valor": 3, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "phase_mm2": {"valor": 9, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "neutral_mm2": {"valor": 16, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "ground_mm2": {"valor": 10, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_0_5": {"valor": 101, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_1": {"valor": 428, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "tube_dia_mm": {"valor": 75, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "cgp_amp_range": {"valor": "63", "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "conductor_amp_rating": {"valor": 63, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}},
    {"power_kw": {"valor": 50, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "phase_mm2": {"valor": 25, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "neutral_mm2": {"valor": 16, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "ground_mm2": {"valor": 16, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_0_5": {"valor": 17, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_1": {"valor": 33, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "tube_dia_mm": {"valor": 110, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "cgp_amp_range": {"valor": "80", "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "conductor_amp_rating": {"valor": 80, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}},
    {"power_kw": {"valor": 78, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "phase_mm2": {"valor": 50, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "neutral_mm2": {"valor": 25, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "ground_mm2": {"valor": 25, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_0_5": {"valor": 20, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_1": {"valor": 41, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "tube_dia_mm": {"valor": 125, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "cgp_amp_range": {"valor": "125", "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "conductor_amp_rating": {"valor": 125, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}},
    {"power_kw": {"valor": 125, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "phase_mm2": {"valor": 95, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "neutral_mm2": {"valor": 50, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "ground_mm2": {"valor": 50, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_0_5": {"valor": 22, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_1": {"valor": 44, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "tube_dia_mm": {"valor": 140, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "cgp_amp_range": {"valor": "200", "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "conductor_amp_rating": {"valor": 200, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}},
    {"power_kw": {"valor": 156, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "phase_mm2": {"valor": 150, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "neutral_mm2": {"valor": 95, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "ground_mm2": {"valor": 95, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_0_5": {"valor": 27, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_1": {"valor": 53, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "tube_dia_mm": {"valor": 180, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "cgp_amp_range": {"valor": "250-400", "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "conductor_amp_rating": {"valor": 250, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}},
    {"power_kw": {"valor": 196, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "phase_mm2": {"valor": 240, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "neutral_mm2": {"valor": 150, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "ground_mm2": {"valor": 150, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_0_5": {"valor": 29, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "max_len_1": {"valor": 57, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "tube_dia_mm": {"valor": 225, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "cgp_amp_range": {"valor": "400", "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}, "conductor_amp_rating": {"valor": 315, "fuente": FUENTE_IBERDROLA_MT_PG17_TABLA1}},
]

iberdrola_cgp_types = [
    {"max_fuse_a": 100, "tipo": "CGP-1-100/BUC, CGP-7-100/BUC", "fuente": FUENTE_IBERDROLA_NI_PG5_TABLA1},
    {"max_fuse_a": 160, "tipo": "CGP-7-160/BUC", "fuente": FUENTE_IBERDROLA_NI_PG5_TABLA1},
    {"max_fuse_a": 250, "tipo": "CGP-7-250/BUC, CGP-9-250/BUC, CGP-10-250/BUC, CGP-11-250/BUC", "fuente": FUENTE_IBERDROLA_NI_PG5_TABLA1},
    {"max_fuse_a": 400, "tipo": "CGP-7-400/BUC, CGP-9-400/BUC", "fuente": FUENTE_IBERDROLA_NI_PG5_TABLA1},
]

# --- Functions ---
def get_iberdrola_cgp_type(max_fuse_a):
    for cgp in iberdrola_cgp_types:
        if max_fuse_a <= cgp["max_fuse_a"]:
            return cgp["tipo"], cgp["fuente"]
    return "N/A (Consultar i-DE para >400A)", FUENTE_IBERDROLA_NI_PG5_TABLA1
