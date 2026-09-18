import pandas as pd
from datetime import datetime
from extract.DNIS import miprincipal

def proceso_fechanac():
 usecols = ['FECHA ATENCION', 'NUMERO DOCUMENTO','CODIGO CIE','VALOR LAB']
 primero =pd.read_excel('data/external/Libro1.xlsx',usecols=usecols)
 segundo = pd.read_excel('data/external/Libro2.xlsx',usecols=usecols)
 #DATOS ETL
 archivo_vac_1 = 'data/raw/2026_vacuna_1.xlsx'
 archivo_vac_2 = 'data/raw/2026_vacuna_2.xlsx'
 df_vac_1 = pd.read_excel(archivo_vac_1,
                   skiprows=6, 
                   skipfooter=2)
 df_vac_2 = pd.read_excel(archivo_vac_2,
                    skiprows=6, 
                    skipfooter=2)
 archivo2 = 'data/raw/2026_99381_1.xlsx'
 df2 = pd.read_excel(archivo2,
                   skiprows=6, 
                   skipfooter=2, 
                   dtype={'NUMERO DOCUMENTO': str})

 padron_df = miprincipal() 
 #UNIR DATOS
 df = pd.concat([primero, segundo,df_vac_1,df_vac_2,df2], ignore_index=True)

 def extraer_numero(documento):
     if pd.notna(documento):
         documento = str(documento) 
         if "DNI |" in documento:
             return documento.split("|")[1].strip()
         elif "CNV |" in documento:
             return documento.split("|")[1].strip()
     return documento

 def formatear_fecha(fecha):
     if pd.notna(fecha):
         if isinstance(fecha, str):
             try:
                 fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
             except:
                 try:
                     fecha = datetime.strptime(fecha, '%Y-%m-%d')
                 except:
                     return fecha  
         return fecha.strftime('%d/%m/%Y')
     return fecha
 
 df['NUMERO DOCUMENTO'] = df['NUMERO DOCUMENTO'].apply(extraer_numero)
 df['FECHA ATENCION'] = df['FECHA ATENCION'].apply(formatear_fecha)

 padron_df = padron_df.drop_duplicates(subset=['NUMERO DOCUMENTO'])
 resultado_df = df.merge(
     padron_df[['NUMERO DOCUMENTO', 'FECHA DE NACIMIENTO']],
     on='NUMERO DOCUMENTO',
     how="left"
 )

 resultado_df = resultado_df.dropna(subset=["FECHA DE NACIMIENTO"])

 for col in ["FECHA DE NACIMIENTO", "FECHA ATENCION"]:
     if col in resultado_df.columns:
         resultado_df[col] = pd.to_datetime(resultado_df[col], format='mixed', dayfirst=True).dt.strftime('%d/%m/%Y')

 return resultado_df