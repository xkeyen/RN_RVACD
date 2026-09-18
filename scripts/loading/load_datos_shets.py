import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def subir_a_google_sheets(data_final):
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        credenciales = ServiceAccountCredentials.from_json_keyfile_name(
            'clave/keyen10-a2b364de4493.json',
            scope
        )
        cliente = gspread.authorize(credenciales)
        sheet_id = '1yJI7Uf9qnRNxEKkpWyypa0h0VxfWC9n05CXrjLSPJZo'
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
                # VACÍOS
                if pd.isna(valor):
                    nueva_fila.append('')
                    continue

                if i in (0, 2, 4, 6, 8, 10, 12):
                    if isinstance(valor, str):
                        valor = valor.strip().lstrip("'")
                        if valor == '':
                            nueva_fila.append('')
                            continue
                        try:
                            valor = int(valor)
                        except ValueError:
                            pass
                    nueva_fila.append(valor)
                    continue


                if i in (1, 3, 5, 7, 9, 11):

                    if isinstance(valor, str):

                        valor = valor.strip().lstrip("'")
                        nueva_fila.append(valor)
                    else:
                        nueva_fila.append(valor)
                    continue
                if isinstance(valor, str):
                    valor = valor.strip().lstrip("'")
                nueva_fila.append(valor)
            datos.append(nueva_fila)
        worksheet.update(
            'A1',
            datos,
            value_input_option='USER_ENTERED'
        )
        print("DATOS SUBIDOS CORRECTAMENTE")
        print(f"Filas: {len(data_final)}")
        print(f"Columnas: {len(data_final.columns)}")
        print("Rango actualizado: A:N")
        return True

    except Exception as e:
        print("ERROR AL SUBIR DATOS")
        print(str(e))
        return False