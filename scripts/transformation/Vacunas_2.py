import pandas as pd
 
def data_vacunas(): 
 archivo_original = 'data/external/Libro2.xlsx'
 archivo_vacuna_1 = 'data/raw/2026_vacuna_1.xlsx' 
 archivo_vacuna_2 = 'data/raw/2026_vacuna_2.xlsx'
 df_vacuna_1 = pd.read_excel( archivo_vacuna_1, skiprows=6, skipfooter=2 ) 
 df_vacuna_2 = pd.read_excel( archivo_vacuna_2, skiprows=6, skipfooter=2 )
 df1 = pd.read_excel(archivo_original)
 df_vacunas = pd.concat( [df_vacuna_1, df_vacuna_2], ignore_index=True )
 df = pd.concat( [df_vacunas, df1], ignore_index=True )
 def filtrar_y_formatear(df, codigo_cie, nombre_fecha):
     filtro = df['CODIGO CIE'] == codigo_cie
     df_filtrado = df.loc[ filtro, ['NUMERO DOCUMENTO', 'FECHA ATENCION'] ].copy()
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

 return df_final

