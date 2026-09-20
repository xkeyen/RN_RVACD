import os
import json
import gspread
import pandas as pd
from google.cloud import secretmanager
from google.oauth2.service_account import Credentials


PROJECT_ID = os.environ.get(
    "GOOGLE_CLOUD_PROJECT"
)
SECRET_ID = "ETL_RN_SHETS"

def obtener_credenciales():
    client = secretmanager.SecretManagerServiceClient()
    secret_name = (
        f"projects/{PROJECT_ID}"
        f"/secrets/{SECRET_ID}"
        f"/versions/latest"
    )
    response = client.access_secret_version(
        request={"name": secret_name}
    )
    contenido = response.payload.data.decode("UTF-8")
    datos_credenciales = json.loads(contenido)
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credenciales = Credentials.from_service_account_info(
        datos_credenciales,
        scopes=scope
    )
    return credenciales


def subir_a_google_sheets(data_final):
    try:
        credenciales = obtener_credenciales()
        cliente = gspread.authorize(credenciales)
        sheet_id = (
            "1yJI7Uf9qnRNxEKkpWyypa0h0VxfWC9n05CXrjLSPJZo"
        )
        sheet = cliente.open_by_key(sheet_id)
        worksheet = None

        for ws in sheet.worksheets():
            if ws.id == 1402527898:
                worksheet = ws
                break

        if worksheet is None:
            worksheet = sheet.sheet1
  
        data_final = data_final.copy()
        datos = []
        cabecera = [
            str(columna).lstrip("'")
            for columna in data_final.columns
        ]

        datos.append(cabecera)

        for fila in data_final.itertuples(
            index=False,
            name=None
        ):

            nueva_fila = []

            for i, valor in enumerate(fila):
                if pd.isna(valor):
                    nueva_fila.append("")
                    continue

                if i in (
                    0, 2, 4, 6,
                    8, 10, 12
                ):
                    if isinstance(valor, str):
                        valor = (
                            valor
                            .strip()
                            .lstrip("'")
                        )
                        if valor == "":
                            nueva_fila.append("")
                            continue
                        try:
                            valor = int(valor)
                        except ValueError:
                            pass
                    nueva_fila.append(valor)
                    continue

                if i in (
                    1, 3, 5,
                    7, 9, 11
                ):
                    if isinstance(valor, str):
                        valor = (
                            valor
                            .strip()
                            .lstrip("'")
                        )
                    nueva_fila.append(valor)
                    continue

                if isinstance(valor, str):
                    valor = (
                        valor
                        .strip()
                        .lstrip("'")
                    )
                nueva_fila.append(valor)
            datos.append(nueva_fila)

        worksheet.update(
            "A1",
            datos,
            value_input_option="USER_ENTERED"
        )

        print("✓ DATOS SUBIDOS CORRECTAMENTE")
        return True
    except Exception as e:
        print("ERROR AL SUBIR DATOS")
        print(str(e))
        raise