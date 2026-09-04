import pandas as pd
from openpyxl.styles import numbers
import time
tiempo_inicio = time.time()
# DATAFRAMES
archivo_original = 'datos/Libro2.xlsx'
archivo2 = 'datos/2026_vacuna_1.xlsx'
df2 = pd.read_excel(archivo2,
                   skiprows=6, 
                   skipfooter=2)
df1 = pd.read_excel(archivo_original)
df = pd.concat([df2, df1], ignore_index=True)

def filtrar_y_formatear(df, codigo_cie, nombre_fecha):
    filtro = df['CODIGO CIE'] == codigo_cie
    df_filtrado = df[filtro]
    df_filtrado = df_filtrado[['NUMERO DOCUMENTO', 'FECHA ATENCION']]
    df_filtrado = df_filtrado.rename(columns={
        'NUMERO DOCUMENTO': 'DNI',
        'FECHA ATENCION': nombre_fecha
    })
    df_filtrado['DNI'] = df_filtrado['DNI'].astype(str).str.slice(start=6)
    df_filtrado[nombre_fecha] = pd.to_datetime(df_filtrado[nombre_fecha]).dt.strftime('%d/%m/%Y')
    return df_filtrado

df_cie_90585 = filtrar_y_formatear(df, 90585, 'FECHA BCG')
df_cie_90744 = filtrar_y_formatear(df, 90744, 'FECHA HVB')
df_cie_36416 = filtrar_y_formatear(df, 36416, 'FECHA TAMZ')
df_final = pd.concat([df_cie_90585.reset_index(drop=True), 
                      df_cie_90744.reset_index(drop=True), 
                      df_cie_36416.reset_index(drop=True)], axis=1)

archivo_filtrado = '2_vacunas.xlsx'
with pd.ExcelWriter(archivo_filtrado, engine='openpyxl') as writer:
    df_final.to_excel(writer, index=False, sheet_name='Datos Filtrados')
    worksheet = writer.sheets['Datos Filtrados']
    for col in ['B', 'D', 'F']:  
        for cell in worksheet[col]:
            if cell.row != 1:  
                cell.number_format = 'dd/mm/yyyy'  

print(f"Los datos filtrados han sido guardados en '{archivo_filtrado}'.")
tiempo_final = time.time()
tiempo_ejecucion = tiempo_final - tiempo_inicio
print(f"Tiempo de ejecución: {tiempo_ejecucion} segundos")