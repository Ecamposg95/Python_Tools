# -*- coding: utf-8 -*-
"""
Created on Thu May  2 04:07:02 2024

@author: ecamp
"""

import os
import PyPDF2
import difflib
import pandas as pd

def extract_text_from_pdf(pdf_path):
    """Extrae todo el texto de un archivo PDF."""
    text = ''
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def compare_pdfs_to_excel(original_pdf, revised_pdf, excel_path):
    """Genera un archivo Excel con las diferencias entre dos PDFs."""
    original_text = extract_text_from_pdf(original_pdf).split()
    revised_text = extract_text_from_pdf(revised_pdf).split()

    # Usando difflib para encontrar diferencias
    d = difflib.Differ()
    diff = list(d.compare(original_text, revised_text))

    # Preparando los datos para el DataFrame
    maqueta = [line[2:] for line in diff if line.startswith('+ ')]
    falta = [line[2:] for line in diff if line.startswith('- ')]
    unchanged = [line[2:] for line in diff if line.startswith('  ')]

    # Creando DataFrame
    df = pd.DataFrame({
        'Maqueta': pd.Series(maqueta),
        'Falta': pd.Series(falta),
        'Unchanged': pd.Series(unchanged)
    })

    # Escribiendo el DataFrame a un archivo Excel
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Differences')

    print("El reporte generado en:", excel_path)
    print("El proceso ha terminado.")

# Ajustando la ruta base al directorio superior al de 'Script'
base_dir = os.path.dirname(os.path.dirname(__file__))
input_dir = os.path.join(base_dir, 'Input')
output_dir = os.path.join(base_dir, 'Output')

# Rutas a los archivos PDF
original_pdf_path = os.path.join(input_dir, 'CPEUM.pdf')
revised_pdf_path = os.path.join(input_dir, 'Constitucion_bolsillo.pdf')

# Ruta al archivo Excel de diferencias
excel_file_path = os.path.join(output_dir, 'Differences2.xlsx')

# Comparar los PDFs y generar reporte de diferencias en Excel
compare_pdfs_to_excel(original_pdf_path, revised_pdf_path, excel_file_path)
