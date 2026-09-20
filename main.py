from scripts.transformation.CRED99381_01 import data_99381_01
from scripts.transformation.Vacunas_2 import data_vacunas
from scripts.transformation.Unir_resultados import unir_datos
from scripts.transformation.procesado_data_3 import data_procesada
from scripts.loading.load_datos_shets import subir_a_google_sheets
from scripts.extract.Extraccion import ejecutar_extract
from scripts.extract.cloudStorage import descargar_archivos_external

def main():
 print("=== INICIO ETL ===")
 # 1. EXTRACT
 descargar_archivos_external()
 ejecutar_extract()
 # 2. TRANSFORM
 data_99381 = data_99381_01()
 data_vacuna = data_vacunas()
 data_procesado = data_procesada()
  # 3. UNIÓN
 data_final = unir_datos(data_99381,data_vacuna,data_procesado)
 # 4. LOAD
 subir_a_google_sheets(data_final)
 print("=== ETL FINALIZADO ===")


if __name__ == "__main__":
    main()