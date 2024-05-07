# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:46:14 2024

@author: ecamp
"""

import os
import pandas as pd
from fuzzywuzzy import process

# Define las rutas para los archivos de entrada y salida
input_file_path = os.path.join('..', 'input', 'concatenar.xlsx')
output_file_path = os.path.join('..', 'output', 'autores_corregidos3.xlsx')

# Asegurarse de que el directorio de salida exista
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Cargar el archivo Excel
df = pd.read_excel(input_file_path)

def reemplazar_nombres_concatenados(nombres_concatenados, lista_nombres_correctos):
    if pd.isnull(nombres_concatenados):
        return ""  # Devolver una cadena vacía si el valor es NaN

    # Eliminar delimitadores sobrantes al final de la cadena
    nombres_concatenados = nombres_concatenados.rstrip(';')
    
    # Separar los nombres por el delimitador ';'
    nombres = nombres_concatenados.split(';')
    
    # Inicializar una lista para guardar los nombres corregidos
    nombres_corregidos = []
    
    for nombre in nombres:
        if nombre:  # Asegurarse de que el nombre no esté vacío antes de procesarlo
            nombre_corregido, _ = process.extractOne(str(nombre), lista_nombres_correctos)
            nombres_corregidos.append(nombre_corregido)
    
    # Reconstruir la cadena de nombres concatenados, separados por ';'
    # Se agrega el delimitador al final para mantener el formato original
    return ';'.join(nombres_corregidos) + ';'

# Asegúrate de aplicar esta función corregida al DataFrame como antes.


# Asumiendo que 'Autor_concatenados' es la columna con los nombres concatenados
# y que 'correctos' contiene los nombres correctos (asegurarse de que sean solo cadenas)
lista_nombres_correctos = df['correctos'].astype(str).unique()

# Aplicar la función a la columna de nombres concatenados
df['Autor_concatenados_corregidos'] = df['Autor_concatenados'].apply(reemplazar_nombres_concatenados, lista_nombres_correctos=lista_nombres_correctos)

# Guardar el resultado en un nuevo archivo Excel
df.to_excel(output_file_path, index=False)

print(f"Proceso completado. Los autores han sido corregidos y guardados en '{output_file_path}'")
