import base64

def generate_printable_report(inputs, outputs, scheme_html, logo_base64):
    """Generates an HTML report for printing with visual improvements."""
    
    diagram_styles = outputs.get('diagram_styles', '')

    report_html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte de Instalación Eléctrica</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {{ 
                font-family: 'Inter', sans-serif; 
                margin: 20px; 
                color: #333; 
            }}
            .report-container {{ 
                max-width: 800px; 
                margin: auto; 
            }}
            .logo-container {{
                text-align: left;
                margin-bottom: 30px;
                border-bottom: 1px solid #eee;
                padding-bottom: 20px;
            }}
            .logo-container img {{
                max-width: 200px;
                height: auto;
            }}
            h1, h2 {{ 
                color: #000; 
                border-bottom: 2px solid #eee; 
                padding-bottom: 10px; 
            }}
            h1 {{ font-size: 24px; }}
            h2 {{ font-size: 20px; margin-top: 30px; }}
            .section {{ margin-bottom: 25px; }}
            .grid {{ 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 15px; 
            }}
            .grid-item strong {{ 
                display: block; 
                margin-bottom: 5px; 
                color: #555; 
            }}
            .scheme-container {{ margin-top: 30px; }}
            
            /* Printer-specific styles */
            @media print {{
                body {{ margin: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
                .no-print {{ display: none; }}
                .diagram-container {{ 
                    box-shadow: none; 
                    border: 1px solid #ccc; 
                    background-color: #fff !important;
                    transform: scale(0.9);
                    transform-origin: top left;
                    width: 111%;
                }}
                .zone {{
                    background-color: #fff !important;
                }}
            }}
            
            /* Include the diagram styles directly */
            {diagram_styles}
        </style>
    </head>
    <body onload="window.print()">
        <div class="report-container">
            <div class="logo-container">
                <!-- THIS IS THE CORRECTED LINE -->
                <img src="data:image/png;base64,{logo_base64}" alt="Logo ASEPEYO">
            </div>

            <h1>Reporte de Instalación Eléctrica</h1>
            
            <div class="section">
                <h2>Parámetros de Entrada</h2>
                <div class="grid">
                    <div class="grid-item"><strong>Compañía:</strong> {inputs.get('company', 'N/A')}</div>
                    <div class="grid-item"><strong>Potencia (kW):</strong> {inputs.get('power_kw', 'N/A')}</div>
                    <div class="grid-item"><strong>Tensión (V):</strong> {inputs.get('voltage_v', 'N/A')}</div>
                    <div class="grid-item"><strong>Fases:</strong> {inputs.get('phase_number', 'N/A')}</div>
                    <div class="grid-item"><strong>Factor de Potencia:</strong> {inputs.get('load_factor', 'N/A')}</div>
                </div>
            </div>

            <div class="section">
                <h2>Resultados Generados</h2>
                <div class="grid">
                    <div class="grid-item"><strong>Corriente de Diseño (A):</strong> {outputs.get('calculated_current', 0):.2f} A</div>
                    <div class="grid-item"><strong>Capacidad del IGM:</strong> {outputs.get('igm_spec', 'N/A').replace('<strong>','').replace('</strong>','')}</div>
                    <div class="grid-item"><strong>Tipo de CGP:</strong> {outputs.get('cgp_spec', 'N/A').replace('<br>', ', ').replace('<strong>','').replace('</strong>','')}</div>
                    <div class="grid-item"><strong>LGA (Conductores):</strong> {outputs.get('lga_spec', 'N/A').replace('<br>', ', ').replace('<strong>','').replace('</strong>','')}</div>
                    <div class="grid-item"><strong>Tubo / Canalización:</strong> {outputs.get('tubo_spec', 'N/A').replace('<strong>','').replace('</strong>','')}</div>
                </div>
            </div>

            <div class="scheme-container">
                <h2>Esquema de Instalación</h2>
                {scheme_html}
            </div>
        </div>
    </body>
    </html>
    """
    return report_html

def get_report_download_link(inputs, outputs, scheme_html, logo_base64):
    """Generates a download link for the printable report."""
    report_html = generate_printable_report(inputs, outputs, scheme_html, logo_base64)
    b64 = base64.b64encode(report_html.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="reporte_electrico.html" target="_blank">Abrir Reporte en Nueva Pestaña para Imprimir</a>'
    return href
