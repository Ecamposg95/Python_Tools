# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 12:58:57 2024

@author: ecamp
"""

import pandas as pd
import os

# Rutas a los archivos
input_file_path = os.path.join('..', 'input', 'db_autores.xlsx')
output_file_path = os.path.join('..', 'output', 'db_autores_normalizados.xlsx')

# Cargar el archivo Excel
df = pd.read_excel(input_file_path, sheet_name='Sheet1')

# Asegúrate de que el directorio de salida exista
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Crear un mapeo basado en la columna 'BUENO' que ya contiene el nombre normalizado seleccionado
mapeo_nombres = {row['Nombre Original']: row['BUENO'] for _, row in df.iterrows() if pd.notna(row['BUENO'])}

# Actualizar los nombres en la base de datos original
df['Nombre Normalizado'] = df['Nombre Original'].apply(lambda x: mapeo_nombres.get(x, x))

# Guardar el resultado en un nuevo archivo Excel
df.to_excel(output_file_path, index=False)

print(f'Archivo guardado en {output_file_path}')
