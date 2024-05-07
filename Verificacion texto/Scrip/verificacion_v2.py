# -*- coding: utf-8 -*-
"""
Created on Thu May  2 03:47:08 2024

@author: ecamp
"""

import os
import PyPDF2
import difflib

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

def compare_pdfs(original_pdf, revised_pdf, diff_file):
    """Genera un reporte de diferencias entre dos PDFs."""
    original_text = extract_text_from_pdf(original_pdf).split()
    revised_text = extract_text_from_pdf(revised_pdf).split()

    # Usando difflib para encontrar diferencias
    d = difflib.Differ()
    diff = list(d.compare(original_text, revised_text))

    # Escribiendo las diferencias en un archivo
    with open(diff_file, 'w') as file:
        for line in diff:
            file.write(line + '\n')

    print("El reporte de diferencias ha sido generado en:", diff_file)

# Ajustando la ruta base al directorio superior al de 'Script'
base_dir = os.path.dirname(os.path.dirname(__file__))
input_dir = os.path.join(base_dir, 'Input')
output_dir = os.path.join(base_dir, 'Output')

# Rutas a los archivos PDF
original_pdf_path = os.path.join(input_dir, 'CPEUM.pdf')
revised_pdf_path = os.path.join(input_dir, 'Constitucion_bolsillo.pdf')

# Ruta al archivo de diferencias
diff_file_path = os.path.join(output_dir, 'diferencias.txt')

# Comparar los PDFs y generar reporte de diferencias
compare_pdfs(original_pdf_path, revised_pdf_path, diff_file_path)
