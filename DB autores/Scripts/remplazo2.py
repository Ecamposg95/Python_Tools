# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 18:45:01 2024

@author: ecamp
"""

import pandas as pd
from fuzzywuzzy import process
import os

# Definir las rutas de los archivos
input_file_path = os.path.join('..', 'input', 'comp2.xlsx')
output_file_path = os.path.join('..', 'output', 'nombres_corregidos5.xlsx')

# Cargar las hojas de Excel
df_nombres_correctos = pd.read_excel(input_file_path, sheet_name='Sheet1')
df_nombres_por_corregir = pd.read_excel(input_file_path, sheet_name='Sheet2')

# Convertir los nombres a cadena y manejar posibles valores nulos
df_nombres_correctos['Nombre bueno'] = df_nombres_correctos['Nombre bueno'].astype(str)
df_nombres_por_corregir['Nombre autor mal'] = df_nombres_por_corregir['Nombre autor mal'].apply(lambda x: x if isinstance(x, str) else "")

# Función para encontrar la mejor coincidencia
def encontrar_coincidencia(nombre, lista_nombres, threshold=90):
    if nombre:  # Solo procesar si la cadena no está vacía
        mejor_coincidencia, puntaje = process.extractOne(nombre, lista_nombres)
        if puntaje >= threshold:
            return mejor_coincidencia
    return nombre  # Devolver el nombre original si está vacío o no hay coincidencia suficientemente buena

# Aplicar la función para corregir los nombres
df_nombres_por_corregir['Nombre Corregido'] = df_nombres_por_corregir['Nombre autor mal'].apply(
    encontrar_coincidencia, args=(df_nombres_correctos['Nombre bueno'].tolist(),))

# Agregar columna para identificar si un nombre fue corregido
df_nombres_por_corregir['Corregido'] = df_nombres_por_corregir['Nombre autor mal'] != df_nombres_por_corregir['Nombre Corregido']

# Agregar columna para nombres no corregidos basados en la columna 'Corregido'
df_nombres_por_corregir['No Corregidos'] = df_nombres_por_corregir.apply(
    lambda row: row['Nombre autor mal'] if not row['Corregido'] else '', axis=1)

# Guardar en un nuevo archivo Excel
df_nombres_por_corregir.to_excel(output_file_path, index=False)

print(f'Archivo guardado en: {output_file_path}')
