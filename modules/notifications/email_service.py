import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.logger import get_logger
from modules.notifications.formatter import generate_sla_html_report

log = get_logger("Notification_Service")

def send_alert_email(df_tickets, sender_email, sender_password, receiver_email):
    if not sender_email or not sender_password or not receiver_email:
        log.error("[LOAD/NOTIFY] Variables de correo no configuradas en .env")
        raise ValueError("Credenciales SMTP o destinatario no definidos en .env")

    if df_tickets.empty:
        log.info("[LOAD/NOTIFY] No se registraron tickets fuera de SLA. Omitiendo envío de correo.")
        return

    log.info(f"[LOAD/NOTIFY] Preparando notificación SMTP para: {receiver_email}")
    
    html_content = generate_sla_html_report(df_tickets)
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"🔴 ALERTA: {len(df_tickets)} Tickets Fuera de SLA"
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        log.info("[LOAD/NOTIFY] Correo de alerta despachado exitosamente.")
    except Exception as e:
        log.error(f"[LOAD/NOTIFY] Error al despachar correo vía SMTP: {e}")
        raise