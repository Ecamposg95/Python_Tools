# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:34:41 2024

@author: ecamp
"""

import PyPDF2
import pandas as pd
import os

# Rutas a las carpetas de entrada y salida
carpeta_entrada = 'input'
carpeta_salida = 'output'

# Asegurarse de que la carpeta de salida existe
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

# Rutas completas a los archivos
ruta_archivo_excel = os.path.join(carpeta_entrada, 'NOMBRES.xlsx')  # Actualizado al nombre real de tu archivo Excel
nombre_columna_nombres = 'NombreColumna'  # Asegúrate de que esto coincide con el nombre de la columna en tu archivo Excel
ruta_archivo_pdf = os.path.join(carpeta_entrada, 'TODOS.pdf')  # Actualizado al nombre real de tu archivo PDF

# Leer los nombres desde el archivo Excel
df = pd.read_excel(ruta_archivo_excel)
nombres = df[nombre_columna_nombres].tolist()

# Leer y dividir el archivo PDF
with open(ruta_archivo_pdf, 'rb') as archivo_pdf:
    lector_pdf = PyPDF2.PdfReader(archivo_pdf)
    numero_paginas = len(lector_pdf.pages)

    if numero_paginas != len(nombres):
        print("Error: El número de nombres en el archivo Excel no coincide con el número de páginas en el PDF.")
    else:
        for i in range(numero_paginas):
            escritor_pdf = PyPDF2.PdfWriter()
            escritor_pdf.add_page(lector_pdf.pages[i])

            nombre_archivo_salida = f'{nombres[i]}.pdf'
            ruta_completa_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
            with open(ruta_completa_salida, 'wb') as archivo_salida:
                escritor_pdf.write(archivo_salida)
            print(f'Archivo guardado: {ruta_completa_salida}')

print("Proceso completado.")
