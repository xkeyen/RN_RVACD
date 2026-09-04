import pandas as pd 

def miprincipal():
 sheet_id_1 = "1yJI7Uf9qnRNxEKkpWyypa0h0VxfWC9n05CXrjLSPJZo"
 gid_1 = "1402527898"  
 url_1 = f"https://docs.google.com/spreadsheets/d/{sheet_id_1}/export?format=csv&gid={gid_1}"
 sheet_id_2 = "1yJI7Uf9qnRNxEKkpWyypa0h0VxfWC9n05CXrjLSPJZo"
 gid_2 = "455335311"  
 url_2 = f"https://docs.google.com/spreadsheets/d/{sheet_id_2}/export?format=csv&gid={gid_2}"
 df_dnis_1 = pd.read_csv(
     url_1,
     usecols=[12, 13],  
     dtype=str          
 )
 df_dnis_2 = pd.read_csv(
     url_2,
     skiprows=1,
     usecols=[2, 3],  
     dtype=str       
 )
 df_dnis_1 = df_dnis_1.dropna(how="all").reset_index(drop=True)
 df_dnis_2 = df_dnis_2.dropna(how="all").reset_index(drop=True)
 df_dnis_2 = df_dnis_2.rename(columns={
    "FN": "FECHA DE NACIMIENTO",
    "DNI /CNV": "NUMERO DOCUMENTO"
 })
 df_dnis_2 = df_dnis_2.drop_duplicates(
    subset=["NUMERO DOCUMENTO"],
    keep="first"
 ).reset_index(drop=True)
 df_dnis_final = pd.concat([df_dnis_1,df_dnis_2[~df_dnis_2["NUMERO DOCUMENTO"].isin(df_dnis_1["NUMERO DOCUMENTO"])]], ignore_index=True)
 
 df_dnis_final["FECHA DE NACIMIENTO"] = pd.to_datetime(
        df_dnis_final["FECHA DE NACIMIENTO"],
        format="%d/%m/%Y",
        errors="coerce"
    )
 return(df_dnis_final)


#df_dnis_final = miprincipal()
#nombre_archivo = "resultado_dnis.xlsx"
#df_dnis_final.to_excel(nombre_archivo, index=False, engine="openpyxl")
#print(f"Archivo guardado exitosamente como: {nombre_archivo}")