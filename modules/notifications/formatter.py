def generate_sla_html_report(df_tickets):
    total_tickets = len(df_tickets)
    
    rows_html = ""
    for _, row in df_tickets.iterrows():
        dias = row['Dias_SLA']
        if dias >= 10:
            badge_style = "background-color: #ef4444; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;"
        else:
            badge_style = "background-color: #f97316; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;"
            
        rows_html += f"""
        <tr style="border-bottom: 1px solid #e2e8f0;">
            <td style="padding: 10px; text-align: center; font-weight: 600;">{row['ID_Ticket']}</td>
            <td style="padding: 10px; text-align: left;">{row['Responsable']}</td>
            <td style="padding: 10px; text-align: center;">{row['Estado_Ticket']}</td>
            <td style="padding: 10px; text-align: center;">{row['Fecha_Creacion']}</td>
            <td style="padding: 10px; text-align: center;"><span style="{badge_style}">{dias} días</span></td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px;">
        <div style="max-width: 650px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">
            <div style="background-color: #1e293b; color: #ffffff; padding: 20px; text-align: center;">
                <h2 style="margin: 0; font-size: 20px;">🔴 Alerta Operativa: Monitoreo SLA</h2>
            </div>
            <div style="padding: 24px;">
                <div style="background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 12px 16px; margin-bottom: 20px; border-radius: 4px;">
                    <p style="margin: 0; color: #991b1b; font-weight: 600; font-size: 14px;">
                        Se han detectado <strong>{total_tickets}</strong> tickets que superan el umbral máximo tolerado.
                    </p>
                </div>
                <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #334155;">
                    <thead>
                        <tr style="background-color: #f1f5f9; color: #475569; text-align: left;">
                            <th style="padding: 10px; text-align: center;">ID Ticket</th>
                            <th style="padding: 10px;">Responsable</th>
                            <th style="padding: 10px; text-align: center;">Estado</th>
                            <th style="padding: 10px; text-align: center;">Fecha Creación</th>
                            <th style="padding: 10px; text-align: center;">Días SLA</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
            <div style="background-color: #f1f5f9; padding: 12px; text-align: center; color: #64748b; font-size: 11px;">
                Este reporte fue generado automáticamente por el pipeline de monitoreo SLA.
            </div>
        </div>
    </body>
    </html>
    """
    return html_content