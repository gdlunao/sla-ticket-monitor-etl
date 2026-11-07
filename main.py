from core.config import GCP_CREDENTIALS_DICT, SPREADSHEET_NAME, SLA_THRESHOLD_DAYS
from core.config import SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL
from modules.google_sheets.service import extract_tickets_data, transform_tickets_data
from modules.notifications.email_service import send_alert_email
from core.logger import get_logger

log = get_logger("Main_Pipeline")

def main():
    log.info("=== INICIANDO PIPELINE DE ALERTAS SLA (ETL) ===")
    
    try:
        # 1. Extract
        df_raw = extract_tickets_data(GCP_CREDENTIALS_DICT, SPREADSHEET_NAME)
        
        # 2. Transform
        df_overdue = transform_tickets_data(df_raw, SLA_THRESHOLD_DAYS)
        
        # 3. Load / Notify
        if not df_overdue.empty:
            send_alert_email(df_overdue, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL)
            
        log.info("=== PIPELINE COMPLETADO EXITOSAMENTE ===")
            
    except Exception as e:
        log.critical(f"Pipeline interrumpido por error de ejecución: {e}")

if __name__ == "__main__":
    main()