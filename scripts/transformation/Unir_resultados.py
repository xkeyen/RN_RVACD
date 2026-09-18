import pandas as pd

def unir_datos(primero,segundo, tercero):
 primero = primero.reset_index(drop=True)
 segundo = segundo.reset_index(drop=True)
 tercero = tercero.reset_index(drop=True)
 data_final = pd.concat([primero, segundo,tercero], axis=1)
 data_final = data_final.fillna('') 
 return data_final


