import requests
from pathlib import Path
from datetime import date
hoy = date.today()
url = "http://oiteopendata.diresacallao.gob.pe/Opendata.beta/Req/Report/Consultas/Por_hasta_10Codigos.php"


payload = {
    'Fcha1': '2026-01-01',
    'Fcha2': hoy,
    'Codigo_CIE_1': '90585',
    'Desc_Codigo_1': 'VACUNA BCG',
    'Codigo_CIE_2': '90744',
    'Codigo_CIE_3': '36416',
    'Diagnostico_1': 'T',
    'id_eess': '000000000',
    'eess_text': 'DIRECCION REGIONAL DE SALUD DEL CALLAO - DIRESA CALLAO',
    'edad1': '1',
    'edad2': '28'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://oiteopendata.diresacallao.gob.pe',
    'Referer': 'http://oiteopendata.diresacallao.gob.pe/Opendata.beta/Req/Interface/Consultas/Por_hasta_10Codigos.php'
}


carpeta = Path("datos")
carpeta.mkdir(exist_ok=True)

nombre_archivo = carpeta / "2026_vacuna_1.xlsx"

print("Enviando petición al servidor de DIRESA Callao...")

try:
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        print("¡Conexión exitosa!")
        with open(nombre_archivo, "wb") as f:
            f.write(response.content)            
        print(f"Descarga completada. El archivo se guardó como: {nombre_archivo}")
    else:
        print(f"Error en el servidor. Código de estado: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Ocurrió un error al conectar con el servidor: {e}")