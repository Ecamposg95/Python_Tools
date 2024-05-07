# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 03:03:46 2024

@author: ecamp
"""

from fuzzywuzzy import fuzz, process
import pandas as pd
import os

# Define las rutas para los archivos de entrada y salida
input_file_path = os.path.join('..', 'output', 'autores_separados2.xlsx')
output_similares_file_path = os.path.join('..', 'output', 'autores_similares.xlsx')

# Asegúrate de que el directorio de salida exista
os.makedirs(os.path.dirname(output_similares_file_path), exist_ok=True)

# Cargar el archivo Excel con los nombres de autores individuales
df_autores_individuales = pd.read_excel(input_file_path)

# Filtrar los valores nulos antes de procesar
df_autores_individuales.dropna(subset=['Autor Individual'], inplace=True)

# Asegurar que todos los nombres son cadenas
df_autores_individuales['Autor Individual'] = df_autores_individuales['Autor Individual'].astype(str)

# Convertir todos los nombres a mayúsculas para estandarizar la comparación
df_autores_individuales['Autor Individual'] = df_autores_individuales['Autor Individual'].str.upper()

# Crear un conjunto único de nombres para reducir el número de comparaciones necesarias
nombres_unicos = df_autores_individuales['Autor Individual'].unique()

# Utilizar fuzzywuzzy para encontrar coincidencias que no sean perfectas dentro de la lista
similares = {}
for nombre in nombres_unicos:
    # Obtener coincidencias con un umbral de similitud, por ejemplo, 90
    coincidencias = process.extract(nombre, nombres_unicos, limit=None, scorer=fuzz.WRatio)
    similares[nombre] = [coincidencia for coincidencia in coincidencias if coincidencia[1] > 90 and coincidencia[0] != nombre]

# Convertir el diccionario de nombres similares en un DataFrame para una mejor visualización y exportación
df_similares = pd.DataFrame([(nombre, sim[0], sim[1]) for nombre, sims in similares.items() for sim in sims], columns=['Nombre Original', 'Nombre Similar', 'Grado de Similitud'])

# Guardar el DataFrame de nombres similares en un nuevo archivo Excel
df_similares.to_excel(output_similares_file_path, index=False)

print(f'El archivo con autores similares se ha guardado en: {output_similares_file_path}')
