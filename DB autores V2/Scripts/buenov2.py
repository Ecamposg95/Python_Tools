# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 13:19:41 2024

@author: ecamp
"""

import pandas as pd
import os

# Rutas a los archivos
input_file_path = os.path.join('..', 'input', 'db_autores.xlsx')
output_file_path = os.path.join('..', 'output', 'db_autores_normalizados_con_longitud.xlsx')

# Cargar el archivo Excel
df = pd.read_excel(input_file_path, sheet_name='Sheet1')

# Asegúrate de que el directorio de salida exista
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Crear un mapeo de nombres que prefiera el nombre más largo
mapeo_nombres = {}
for _, row in df.iterrows():
    if pd.notna(row['BUENO']):
        nombre_original = row['Nombre Original']
        buen_nombre = row['BUENO']
        # Si el nombre original ya está en el mapeo, elegir el más largo
        if nombre_original in mapeo_nombres:
            if len(buen_nombre) > len(mapeo_nombres[nombre_original]):
                mapeo_nombres[nombre_original] = buen_nombre
        else:
            mapeo_nombres[nombre_original] = buen_nombre

# Actualizar los nombres en la base de datos original
df['Nombre Normalizado'] = df['Nombre Original'].apply(lambda x: mapeo_nombres.get(x, x))

# Guardar el resultado en un nuevo archivo Excel
df.to_excel(output_file_path, index=False)

print(f'Archivo guardado en {output_file_path}')
