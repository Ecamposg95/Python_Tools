# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:12:27 2024

@author: ecamp
"""

from fuzzywuzzy import fuzz, process
import pandas as pd
import os

# Define las rutas para los archivos de entrada y salida
input_file_path = os.path.join('..', 'output', '2_autores_separados.xlsx')
output_similares_file_path = os.path.join('..', 'output', 'autores_similares_87.xlsx')

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
    coincidencias = process.extract(nombre, nombres_unicos, limit=None, scorer=fuzz.WRatio)
    lista_similares = [coincidencia[0] for coincidencia in coincidencias if coincidencia[1] > 87 and coincidencia[0] != nombre]
    if lista_similares:
        similares[nombre] = lista_similares

# Convertir el diccionario de nombres similares en un DataFrame organizando los nombres hacia la derecha
max_len = max(len(v) for v in similares.values())  # Encuentra la lista más larga de nombres similares
columnas = ['Nombre Original'] + [f'Nombre Similar {i+1}' for i in range(max_len)]
data = []
for nombre, lista_nombres in similares.items():
    fila = [nombre] + lista_nombres + [''] * (max_len - len(lista_nombres))  # Ajusta la longitud de cada fila
    data.append(fila)

df_similares = pd.DataFrame(data, columns=columnas)

# Guardar el DataFrame de nombres similares en un nuevo archivo Excel
df_similares.to_excel(output_similares_file_path, index=False)

print(f'El archivo con autores similares se ha guardado en: {output_similares_file_path}')
