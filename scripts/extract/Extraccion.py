import requests
from pathlib import Path
from datetime import date

URL = ("http://oiteopendata.diresacallao.gob.pe/""Opendata.beta/Req/Report/Consultas/""Por_hasta_10Codigos.php")
CARPETA = Path("data/raw")
CARPETA.mkdir(exist_ok=True)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": (
        "http://oiteopendata.diresacallao.gob.pe"
    ),
    "Referer": (
        "http://oiteopendata.diresacallao.gob.pe/"
        "Opendata.beta/Req/Interface/Consultas/"
        "Por_hasta_10Codigos.php"
    ),
}

def descargar_excel(payload, nombre_archivo):
    ruta_archivo = CARPETA / nombre_archivo
    try:
        response = requests.post(
            URL,
            data=payload,
            headers=HEADERS,
            timeout=600
        )
        if response.status_code != 200:
            print(
                f"ERROR: El servidor respondió "
                f"con código {response.status_code}"
            )
            return False
        if not response.content:

            print(
                "ERROR: El servidor devolvió "
                "un archivo vacío."
            )
            return False
        with open(ruta_archivo, "wb") as archivo:
            archivo.write(response.content)
        print(f"✓ Guardado en: {ruta_archivo}")
        return True
    except requests.exceptions.Timeout:
        print(
            "ERROR: La consulta tardó demasiado "
        )
        return False
    except requests.exceptions.RequestException as e:
        print(f"ERROR de conexión: {e}")
        return False


def extraer_cred():
    hoy = date.today()
    payload = {
        "Fcha1": "2026-01-01",
        "Fcha2": hoy.strftime("%Y-%m-%d"),
        "Codigo_CIE_1": "99381.01",
        "Desc_Codigo_1": (
            "ATENCIÓN INTEGRAL DE SALUD DEL "
            "NIÑO-CRED NEONATO"
        ),
        "Diagnostico_1": "T",
        "id_eess": "000000003",
        "eess_text": (
            "CONSOLIDADO RED DE SALUD VENTANILLA"
        ),
        "edad1": "1",
        "edad2": "28",
    }
    return descargar_excel(payload,"2026_99381_1.xlsx")

def descargar_vacunas(fecha_inicio,fecha_fin,nombre_archivo):
    payload = {
        "Fcha1": fecha_inicio,
        "Fcha2": fecha_fin,
        "Codigo_CIE_1": "90585",
        "Desc_Codigo_1": "VACUNA BCG",
        "Codigo_CIE_2": "90744",
        "Codigo_CIE_3": "36416",
        "Diagnostico_1": "T",
        "id_eess": "000000000",
        "eess_text": (
            "DIRECCION REGIONAL DE SALUD DEL CALLAO - "
            "DIRESA CALLAO"
        ),
        "edad1": "1",
        "edad2": "28",
    }
    return descargar_excel(payload,nombre_archivo)


def extraer_vacunas():
    hoy = date.today()
    anio = hoy.year
    #FECHA 1
    fecha_inicio_1 = f"{anio}-01-01"
    fecha_fin_1 = f"{anio}-06-30"
    archivo_1 = f"{anio}_vacuna_1.xlsx"
    resultado_1 = descargar_vacunas(fecha_inicio_1,fecha_fin_1,archivo_1)
    #FECHA 2
    fecha_inicio_2 = f"{anio}-07-01"
    fecha_fin_2 = hoy.strftime("%Y-%m-%d")
    archivo_2 = f"{anio}_vacuna_2.xlsx"
    #RESULTADO
    resultado_2 = descargar_vacunas(fecha_inicio_2,fecha_fin_2,archivo_2)
    return resultado_1 and resultado_2


# EXTRACT COMPLETO
def ejecutar_extract():
    # 1. CRED
    resultado_cred = extraer_cred()
    # 2. VACUNAS
    resultado_vacunas = extraer_vacunas()