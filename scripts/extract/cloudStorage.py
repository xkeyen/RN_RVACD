from google.cloud import storage
from pathlib import Path

BUCKET_NAME = "proyectos_etl_rv"
GCS_PREFIX = "rn_rvacd/external"
BASE_DIR = Path(__file__).resolve().parents[2]
EXTERNAL_DIR = BASE_DIR / "data" / "external"

def descargar_archivos_external():
    EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    archivos = [
        "Libro1.xlsx",
        "Libro2.xlsx"
    ]
    for nombre_archivo in archivos:
        blob_path = f"{GCS_PREFIX}/{nombre_archivo}"
        destino = EXTERNAL_DIR / nombre_archivo
        print(f"Descargando: {blob_path}")
        blob = bucket.blob(blob_path)
        blob.download_to_filename(destino)
        print(f"✓ Guardado en: {destino}")
