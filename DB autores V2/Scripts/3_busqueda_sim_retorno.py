# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 12:06:20 2024

@author: ecamp
"""

from fuzzywuzzy import fuzz, process
import pandas as pd
import os
import unicodedata

# Define las rutas para los archivos de entrada y salida
input_file_path = os.path.join('..', 'input', '3_db_autores.xlsx')
output_similares_file_path = os.path.join('..', 'output', '3_autores_similares_88.xlsx')
output_no_similares_file_path = os.path.join('..', 'output', '3_autores_no_similares88.xlsx')

# Asegúrate de que el directorio de salida exista
os.makedirs(os.path.dirname(output_similares_file_path), exist_ok=True)

# Función para normalizar nombres eliminando acentos
def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

# Cargar el archivo Excel con los nombres de autores individuales
df_autores_individuales = pd.read_excel(input_file_path)

# Filtrar los valores nulos antes de procesar
df_autores_individuales.dropna(subset=['Autor Individual'], inplace=True)

# Asegurar que todos los nombres son cadenas y convertirlos a mayúsculas
df_autores_individuales['Autor Individual'] = df_autores_individuales['Autor Individual'].apply(lambda x: normalize(x.upper()))

# Crear un conjunto único de nombres para reducir el número de comparaciones necesarias
nombres_unicos = df_autores_individuales['Autor Individual'].unique()

# Utilizar fuzzywuzzy para encontrar coincidencias que no sean perfectas dentro de la lista
similares = {}
nombres_sin_similares = []
for nombre in nombres_unicos:
    coincidencias = process.extract(nombre, nombres_unicos, limit=None, scorer=fuzz.WRatio)
    lista_similares = [coincidencia[0] for coincidencia in coincidencias if coincidencia[1] > 88 and coincidencia[0] != nombre]
    if lista_similares:
        similares[nombre] = lista_similares
    else:
        nombres_sin_similares.append(nombre)  # Agregar el nombre a la lista de no similares

# Procesar nombres similares para el primer archivo Excel
max_len = max((len(v) for v in similares.values()), default=0)  # Ajuste para cuando no hay similares
columnas = ['Nombre Original'] + [f'Nombre Similar {i+1}' for i in range(max_len)]
data = []
for nombre, lista_nombres in similares.items():
    fila = [nombre] + lista_nombres + [''] * (max_len - len(lista_nombres))
    data.append(fila)

df_similares = pd.DataFrame(data, columns=columnas)
df_similares.to_excel(output_similares_file_path, index=False)

# Procesar nombres no similares para el segundo archivo Excel
df_no_similares = pd.DataFrame(nombres_sin_similares, columns=['Nombres sin coincidencias similares'])
df_no_similares.to_excel(output_no_similares_file_path, index=False)

print(f'El archivo con autores similares se ha guardado en: {output_similares_file_path}')
print(f'El archivo con autores que no tienen similares se ha guardado en: {output_no_similares_file_path}')
