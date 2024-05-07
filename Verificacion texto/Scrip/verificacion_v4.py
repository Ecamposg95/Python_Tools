# -*- coding: utf-8 -*-
"""
Created on Thu May  2 04:45:11 2024

@author: ecamp
"""

import os
import PyPDF2
import difflib
import pandas as pd

def extract_text_from_pdf(pdf_path, start_page=None, end_page=None):
    """Extrae texto de un rango específico de páginas de un archivo PDF."""
    text = ''
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        # Si no se especifica end_page, leer hasta la última página
        if end_page is None:
            end_page = len(pdf_reader.pages)
        # Asegurarse de que el rango de páginas es válido
        for page_num in range(max(start_page - 1, 0), min(end_page, len(pdf_reader.pages))):
            page_text = pdf_reader.pages[page_num].extract_text()
            if page_text:
                text += page_text
    return text

def compare_pdfs_to_excel(original_pdf, revised_pdf, excel_path, original_start_page=None, original_end_page=None):
    """Genera un archivo Excel con las diferencias entre dos PDFs."""
    # Aplica el rango solo al documento original
    original_text = extract_text_from_pdf(original_pdf, original_start_page, original_end_page).split()
    # Extrae el texto completo del documento revisado
    revised_text = extract_text_from_pdf(revised_pdf).split()

    d = difflib.Differ()
    diff = list(d.compare(original_text, revised_text))

    added = [line[2:] for line in diff if line.startswith('+ ')]
    deleted = [line[2:] for line in diff if line.startswith('- ')]
    unchanged = [line[2:] for line in diff if line.startswith('  ')]

    df = pd.DataFrame({
        'Added': pd.Series(added),
        'Deleted': pd.Series(deleted),
        'Unchanged': pd.Series(unchanged)
    })

    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Differences')

    print("El reporte de diferencias ha sido generado en:", excel_path)
    print("El proceso ha terminado.")

# Configuración de rutas y parámetros
base_dir = os.path.dirname(os.path.dirname(__file__))
input_dir = os.path.join(base_dir, 'Input')
output_dir = os.path.join(base_dir, 'Output')
original_pdf_path = os.path.join(input_dir, 'CPEUM.pdf')
revised_pdf_path = os.path.join(input_dir, 'Constitucion_bolsillo.pdf')
excel_file_path = os.path.join(output_dir, 'Differences5.xlsx')

# Parámetros para rango de páginas del documento original
original_start_page = 1  # página inicial
original_end_page = 150 # página final

# Ejecutar la comparación con rango específico solo para el documento original
compare_pdfs_to_excel(original_pdf_path, revised_pdf_path, excel_file_path, original_start_page, original_end_page)
