# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:25:16 2024

@author: ecamp
"""
import pandas as pd
import os

# Define las rutas para los archivos de entrada y salida
input_file_path = os.path.join('..', 'input', 'autor.xlsx')
output_file_path = os.path.join('..', 'output', 'autores_separados2.xlsx')

# Asegúrate de que el directorio de salida exista
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Cargar el archivo Excel original desde la hoja 'Sheet1'
df_autores = pd.read_excel(input_file_path, sheet_name='Sheet1')

# Antes de eliminar, contar las filas con valores nulos
filas_con_nulos = df_autores.isnull().any(axis=1).sum()
print(f'Se encontraron {filas_con_nulos} filas con valores nulos.')

# Eliminar cualquier fila que contenga un valor nulo en la columna de autores
df_autores.dropna(inplace=True)

# Después de eliminar, contar las filas restantes
filas_restantes = df_autores.shape[0]
print(f'Después de eliminar, quedan {filas_restantes} filas sin valores nulos.')

# Separar los autores en la primera columna, utilizando ';' como delimitador y eliminando nulos
autores_separados = df_autores.iloc[:,0].str.split(';').dropna()

# Aplanar la lista para tener todos los autores individualmente, eliminando espacios en blanco y omitiendo cadenas vacías
autores_individuales = [autor.strip() for sublist in autores_separados for autor in sublist if autor.strip()]

# Convertir la lista de autores individuales en un DataFrame
df_autores_individuales = pd.DataFrame(autores_individuales, columns=['Autor Individual'])

# Guardar el DataFrame en un nuevo archivo Excel
df_autores_individuales.to_excel(output_file_path, index=False)

print(f'El archivo se ha guardado en: {output_file_path}')