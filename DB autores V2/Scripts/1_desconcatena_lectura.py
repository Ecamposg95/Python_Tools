# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 03:03:46 2024

@author: ecamp

SEPARA LOS NOMBRES CONCATENADOS DEL ARCHIVO ORIGINAL "2_Autor.xlsx"


"""
import pandas as pd
import os

# Define las rutas para los archivos de entrada y salida
input_file_path = os.path.join('..', 'input', '2_Autor.xlsx')
output_file_path = os.path.join('..', 'output', '2_2_autores_separados.xlsx')

# Asegúrate de que el directorio de salida exista
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Cargar el archivo Excel original desde la hoja 'Sheet1'
df_autores = pd.read_excel(input_file_path, sheet_name='Sheet1')

# Eliminar cualquier fila que contenga un valor nulo en la columna de autores
df_autores.dropna(inplace=True)

# Separar los autores en la primera columna, utilizando ';' como delimitador
autores_separados = df_autores.iloc[:, 0].str.split(';')

# Aplanar la lista para tener todos los autores individualmente, eliminando espacios en blanco y omitiendo cadenas vacías
autores_individuales = [autor.strip() for sublist in autores_separados for autor in sublist if autor.strip()]

# Convertir la lista de autores individuales en un DataFrame
df_autores_individuales = pd.DataFrame(autores_individuales, columns=['Autor Individual'])

# Guardar el DataFrame en un nuevo archivo Excel
df_autores_individuales.to_excel(output_file_path, index=False)

print(f'El archivo con autores separados se ha guardado en: {output_file_path}')
