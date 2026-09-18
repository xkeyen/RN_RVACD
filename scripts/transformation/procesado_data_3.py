import pandas as pd
from datetime import datetime, timedelta
from Agregar_Fechas_nac import proceso_fechanac

def data_procesada():
 def cargar_datos():
     df = proceso_fechanac()

     df['CODIGO CIE'] = (
         df['CODIGO CIE']
         .astype(str)
         .str.strip()
         .str.rstrip('.0')
     )

     df['NUMERO DOCUMENTO'] = (
         df['NUMERO DOCUMENTO']
         .astype(str)
         .str.strip()
     )

     df['FECHA ATENCION'] = pd.to_datetime(
         df['FECHA ATENCION'],
         dayfirst=True,
         errors='coerce'
     )

     df['FECHA DE NACIMIENTO'] = pd.to_datetime(
         df['FECHA DE NACIMIENTO'],
         dayfirst=True,
         errors='coerce'
     )

     df['VALOR LAB'] = pd.to_numeric(
         df['VALOR LAB'],
         errors='coerce'
     )

     return df

 def dias_desde(fecha, nacimiento):
     return (fecha.date() - nacimiento).days

 def obtener_primera_fecha(grupo, codigo):
     datos = grupo[
         grupo['CODIGO CIE'] == codigo
     ].sort_values('FECHA ATENCION')
 
     if len(datos):
         return datos.iloc[0]['FECHA ATENCION']

     return None


 def obtener_controles_rn(grupo):
     controles = {}

     rn = grupo[
         grupo['CODIGO CIE'] == '99381.01'
     ]

     for i in [1, 2, 3]:
         datos = rn[
             rn['VALOR LAB'] == i
         ].sort_values('FECHA ATENCION')

         controles[i] = (
             datos.iloc[0]['FECHA ATENCION']
             if len(datos)
             else None
         )

     return controles


 def tiene_huecos(controles):
     encontrado_none = False
 
     for i in [1, 2, 3]:
 
         if controles[i] is None:
             encontrado_none = True
 
         elif encontrado_none:
             return True

     return False


 def validar_intervalos_rn(controles, fecha_nac):

     reglas = {
         1: (3, 6),
         2: (7, 14),
         3: (15, 21)
     }

     for i, (min_d, max_d) in reglas.items():
 
         if controles[i] is None:
             return False

         dias = dias_desde(
             controles[i],
             fecha_nac
         )

         if not (min_d <= dias <= max_d):
             return False

         if i > 1:

             diferencia = (
                 controles[i] -
                 controles[i - 1]
             ).days

             if diferencia < 7:
                 return False

     return True


 def proyecta_intervalos_rn(
     controles,
     fecha_nac,
     hoy
 ):

     reglas = {
         1: (3, 6),
         2: (7, 14),
         3: (15, 21)
     }

     for i, (min_d, max_d) in reglas.items():
 
         if controles[i] is None:
 
             if hoy > fecha_nac + timedelta(days=max_d):
                 return False
 
             return True
 
         dias = dias_desde(
             controles[i],
             fecha_nac
         )

         if not (min_d <= dias <= max_d):
             return False

         if i > 1 and controles[i - 1] is not None:
 
             diferencia = (
                 controles[i] -
                 controles[i - 1]
             ).days

             if diferencia < 7:
                 return False

     return True

 def validar_evento(
     fecha_evento,
     fecha_nac,
     rango,
     hoy,
     proyectar=False
 ):

     min_d, max_d = rango
     if fecha_evento is None:
         return (
             proyectar and
             hoy <= fecha_nac + timedelta(days=max_d)
         )
     dias = dias_desde(
         fecha_evento,
         fecha_nac
     )

     return min_d <= dias <= max_d


 def validar_vacunas_y_tamizaje(
     controles,
     fecha_nac,
     hoy,
     proyectar=False
 ):
 
     reglas = {
         'BCG': (0, 1),
         'HVB': (0, 1),
         'TAMIZAJE': (2, 6)
     }

     for nombre, rango in reglas.items():
         if not validar_evento(
             controles.get(nombre),
             fecha_nac,
             rango,
             hoy,
             proyectar
         ):
             return False
     return True


 def procesar_datos(df):

     resultados = []
     hoy = datetime.now().date()
     grupos = df.groupby(
         [
             'NUMERO DOCUMENTO',
             'FECHA DE NACIMIENTO'
         ]
     )

     for (dni, fecha_nac_ts), grupo in grupos:

         if pd.isna(fecha_nac_ts):
             continue

         fecha_nac = fecha_nac_ts.date()

         controles_rn = obtener_controles_rn(grupo)

         controles = {
             'BCG': obtener_primera_fecha(
                 grupo,
                 '90585'
             ),

             'HVB': obtener_primera_fecha(
                 grupo,
                 '90744'
             ),

             'TAMIZAJE': obtener_primera_fecha(
                 grupo,
                 '36416'
             )
         }

         huecos = tiene_huecos(controles_rn)

         cumple_rn = validar_intervalos_rn(controles_rn,fecha_nac)

         cumple_vac = validar_vacunas_y_tamizaje(
             controles,
             fecha_nac,
             hoy
         )

        # CUMPLE
         cumple = int(
             cumple_rn and
             cumple_vac and
             not huecos
         )

        # SIGUE CUMPLIENDO
         sigue_cumpliendo = int(
             proyecta_intervalos_rn(
                 controles_rn,
                 fecha_nac,
                 hoy
             )
             and
             validar_vacunas_y_tamizaje(
                 controles,
                 fecha_nac,
                 hoy,
                 proyectar=True
             )
             and
             not huecos
         )

         if cumple == 1:
             denominacion = 'CUMPLE'

         elif (
             cumple == 0 and
             sigue_cumpliendo == 1
         ):

             denominacion = 'PROCESO'

         else:
             continue

         resultados.append({
             'DNI': dni,
             'DENOMINACION': denominacion
         })

     return resultados


 def main():
     df = cargar_datos()
     resultados = procesar_datos(df)
     df_resultado = pd.DataFrame(resultados,columns=['DNI','DENOMINACION'])

     return df_resultado

 return main()