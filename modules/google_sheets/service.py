import json
import os
from datetime import datetime, timezone
import pandas as pd
from modules.google_sheets.client import get_google_sheets_client
from core.logger import get_logger

log = get_logger("ETL_Service")

ARTIFACTS_DIR = "artifacts"
EXTRACT_ARTIFACT_PATH = os.path.join(ARTIFACTS_DIR, "data_mock_extract.json")
TRANSFORM_ARTIFACT_PATH = os.path.join(ARTIFACTS_DIR, "data_mock_transformed.json")

def extract_tickets_data(credentials_dict, spreadsheet_name):
    log.info(f"[EXTRACT] Conectando a origen de datos: '{spreadsheet_name}'")
    client = get_google_sheets_client(credentials_dict)
    
    try:
        sheet = client.open(spreadsheet_name).sheet1
        records = sheet.get_all_records()
        total_extracted = len(records)
        
        log.info(f"[EXTRACT] Extracción completada exitosamente. Total de filas procesadas: {total_extracted}")
        
        os.makedirs(ARTIFACTS_DIR, exist_ok=True)
        extract_payload = {
            "execution_timestamp": datetime.now(timezone.utc).isoformat(),
            "source": spreadsheet_name,
            "total_records_extracted": total_extracted,
            "raw_data": records
        }
        
        with open(EXTRACT_ARTIFACT_PATH, "w", encoding="utf-8") as f:
            json.dump(extract_payload, f, ensure_ascii=False, indent=2)
            
        log.info(f"[EXTRACT] Artefacto exportado en: {EXTRACT_ARTIFACT_PATH}")
        return pd.DataFrame(records)
        
    except Exception as e:
        log.error(f"[EXTRACT] Error crítico en extracción: {e}")
        raise

def transform_tickets_data(df, sla_threshold):
    if df.empty:
        log.warning("[TRANSFORM] DataFrame de entrada vacío. 0 filas procesadas.")
        return df

    log.info(f"[TRANSFORM] Evaluando reglas sobre {len(df)} filas...")
    
    overdue_df = df[(df['Estado_Ticket'] != 'Cerrado') & (df['Dias_SLA'] > sla_threshold)]
    total_overdue = len(overdue_df)
    
    log.info(f"[TRANSFORM] Regla de negocio aplicada (> {sla_threshold} días SLA). Filas filtradas (críticas): {total_overdue}")
    
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    transform_payload = {
        "execution_timestamp": datetime.now(timezone.utc).isoformat(),
        "sla_threshold_days": sla_threshold,
        "total_analyzed": len(df),
        "total_overdue": total_overdue,
        "overdue_tickets": overdue_df.to_dict(orient="records")
    }
    
    with open(TRANSFORM_ARTIFACT_PATH, "w", encoding="utf-8") as f:
        json.dump(transform_payload, f, ensure_ascii=False, indent=2)
        
    log.info(f"[TRANSFORM] Artefacto exportado en: {TRANSFORM_ARTIFACT_PATH}")
    return overdue_df