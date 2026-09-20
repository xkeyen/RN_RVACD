FROM python:3.11-slim

WORKDIR /app

# Evita archivos .pyc y permite ver logs inmediatamente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

# Ejecutar ETL
CMD ["python", "main.py"]