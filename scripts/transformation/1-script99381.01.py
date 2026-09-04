import pandas as pd
import numpy as np
from DNIS import miprincipal
from pathlib import Path

def procesar_documento_vectorizado(df_grupo, fecha_nacimiento):
    fechas_ordenadas = np.sort(df_grupo['FECHA ATENCION'].values)
    dias_nacido = (fechas_ordenadas - np.datetime64(fecha_nacimiento)).astype('timedelta64[D]').astype(int)
    resultado = [None, None, None]  
    mascara_1 = (dias_nacido >= 3) & (dias_nacido <= 6)
    if mascara_1.any():
        idx_1 = np.where(mascara_1)[0][0]
        resultado[0] = pd.Timestamp(fechas_ordenadas[idx_1])
        dias_desde_primera = (fechas_ordenadas - fechas_ordenadas[idx_1]).astype('timedelta64[D]').astype(int)
        mascara_2 = (dias_nacido >= 7) & (dias_nacido <= 14) & (dias_desde_primera >= 7)
        if mascara_2.any():
            idx_2 = np.where(mascara_2)[0][0]
            resultado[1] = pd.Timestamp(fechas_ordenadas[idx_2])
            dias_desde_segunda = (fechas_ordenadas - fechas_ordenadas[idx_2]).astype('timedelta64[D]').astype(int)
            mascara_3 = (dias_nacido >= 15) & (dias_nacido <= 21) & (dias_desde_segunda >= 7)
            if mascara_3.any():
                idx_3 = np.where(mascara_3)[0][0]
                resultado[2] = pd.Timestamp(fechas_ordenadas[idx_3])
    return resultado
archivo_original = 'datos/Libro1.xlsx'
archivo2 = 'datos/2026_99381_1.xlsx'
#archivo_fechas_nac = 'fechasNa.xlsx'

df2 = pd.read_excel(
    archivo2,
    skiprows=6, 
    skipfooter=2,
    usecols=['NUMERO DOCUMENTO', 'FECHA ATENCION'],
    dtype={'NUMERO DOCUMENTO': str}
)
df3 = pd.read_excel(
    archivo_original, 
    usecols=['NUMERO DOCUMENTO', 'FECHA ATENCION'],
    dtype={'NUMERO DOCUMENTO': str}
)
df = pd.concat([df3, df2], ignore_index=True)
df['NUMERO DOCUMENTO'] = df['NUMERO DOCUMENTO'].str[6:]
df['FECHA ATENCION'] = pd.to_datetime(df['FECHA ATENCION'])

df_nacimientos = miprincipal()
#df_nacimientos = pd.read_excel(
#    archivo_fechas_nac,
#    usecols=['NUMERO DOCUMENTO', 'FECHA DE NACIMIENTO'],
#    dtype={'NUMERO DOCUMENTO': str}
#)
df_nacimientos['FECHA DE NACIMIENTO'] = pd.to_datetime(df_nacimientos['FECHA DE NACIMIENTO'])
df = df.merge(df_nacimientos, on='NUMERO DOCUMENTO', how='inner') 
resultados_por_doc = {}
for doc, grupo in df.groupby('NUMERO DOCUMENTO', sort=False):
    fecha_nac = grupo['FECHA DE NACIMIENTO'].iloc[0]
    resultados_por_doc[doc] = procesar_documento_vectorizado(grupo, fecha_nac)

documentos = list(resultados_por_doc.keys())
atenciones = list(zip(*resultados_por_doc.values()))
data_final = {}
for i in range(3):
    data_final[f'NUMERO DOCUMENTO_{i+1}'] = [
        doc if atenciones[i][j] is not None else None 
        for j, doc in enumerate(documentos)
    ]
    data_final[f'FECHA ATENCION_{i+1}'] = list(atenciones[i])

df_final = pd.DataFrame(data_final)
df_final = df_final.dropna(how='all', subset=[f'FECHA ATENCION_{i+1}' for i in range(3)])

for i in range(3):
    col_fecha = f'FECHA ATENCION_{i+1}'
    if col_fecha in df_final.columns:
        df_final[col_fecha] = df_final[col_fecha].dt.strftime('%d/%m/%Y')

archivo_filtrado = '1_archivo99381.xlsx'
with pd.ExcelWriter(archivo_filtrado, engine='openpyxl', datetime_format='DD/MM/YYYY') as writer:
    df_final.to_excel(writer, index=False, sheet_name='Datos Filtrados')

print(f"Los datos filtrados han sido guardados en '{archivo_filtrado}'.")
print(f"Total de filas: {len(df_final)}")
print(f"Columnas: {list(df_final.columns)}")