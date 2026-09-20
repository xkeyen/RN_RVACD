# RN_RVACD - ETL Automatizado

Pipeline ETL desarrollado en Python para automatizar la extracción,
transformación y carga de información.

## Arquitectura

- Python
- Docker
- Google Cloud Run Jobs
- Google Cloud Storage
- Google Secret Manager
- Google Sheets
- Pandas
- Gspread

## Flujo

Cloud Storage
    ↓
Cloud Run Job
    ↓
Extract
    ↓
Transform
    ↓
Load
    ↓
Google Sheets

## Estructura

RN_RVACD/
│
├── data/
│   ├── external/
│   └── raw/
│
├── scripts/
│   ├── extract/
│   ├── transformation/
│   └── loading/
│
├── main.py
├── Dockerfile
├── requirements.txt
└── README.md

## Ejecución local

```bash
python main.py