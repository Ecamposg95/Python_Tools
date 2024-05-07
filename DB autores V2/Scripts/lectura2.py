# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 03:03:46 2024

@author: ecamp
"""

import pandas as pd
import os

# Define las rutas para los archivos de entrada y salida
input_file_path = os.path.join('..', 'input', '2_Autor.xlsx')
output_file_path = os.path.join('..', 'output', '2_autores_separados.xlsx')
output_nulos_file_path = os.path.join('..', 'output', '2_1 autores_nulos.xlsx')

# Asegúrate de que el directorio de salida exista
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Cargar el archivo Excel original desde la hoja 'Sheet1'
df_autores = pd.read_excel(input_file_path, sheet_name='Sheet1')

# Identificar las filas con valores nulos
df_autores_nulos = df_autores[df_autores.isnull().any(axis=1)].copy()

# Si hay filas con valores nulos, agregar una columna con el número de la fila original
if not df_autores_nulos.empty:
    df_autores_nulos['Número de Fila Original'] = df_autores_nulos.index + 2  # +2 para compensar el encabezado y el índice base 0
    df_autores_nulos.to_excel(output_nulos_file_path, index=False)
    print(f'Se guardaron {len(df_autores_nulos)} filas con valores nulos en: {output_nulos_file_path}')

# Eliminar cualquier fila que contenga un valor nulo en la columna de autores
df_autores.dropna(inplace=True)

# Separar los autores en la primera columna, utilizando ';' como delimitador y eliminando nulos
autores_separados = df_autores.iloc[:,0].str.split(';').dropna()

# Aplanar la lista para tener todos los autores individualmente, eliminando espacios en blanco y omitiendo cadenas vacías
autores_individuales = [autor.strip() for sublist in autores_separados for autor in sublist if autor.strip()]

# Convertir la lista de autores individuales en un DataFrame
df_autores_individuales = pd.DataFrame(autores_individuales, columns=['Autor Individual'])

# Guardar el DataFrame en un nuevo archivo Excel
df_autores_individuales.to_excel(output_file_path, index=False)

print(f'El archivo con autores separados se ha guardado en: {output_file_path}')
