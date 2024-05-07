# -*- coding: utf-8 -*-
"""
Created on Thu May  2 03:24:16 2024

@author: ecamp
"""
import os
import PyPDF2

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

def compare_pdfs(original_pdf, revised_pdf):
    """Verifica que todo el texto del PDF original esté en el PDF revisado."""
    original_text = extract_text_from_pdf(original_pdf)
    revised_text = extract_text_from_pdf(revised_pdf)

    if all(word in revised_text for word in original_text.split()):
        print("Todo el texto del documento original está en el documento revisado.")
    else:
        print("Algunos elementos del texto original no están en el documento revisado.")

# Ajustando la ruta base al directorio superior al de 'Script'
base_dir = os.path.dirname(os.path.dirname(__file__))

# Definiendo la ruta de entrada
input_dir = os.path.join(base_dir, 'Input')

# Rutas a los archivos PDF
original_pdf_path = os.path.join(input_dir, 'CPEUM.pdf')
revised_pdf_path = os.path.join(input_dir, 'Constitucion_bolsillo.pdf')

# Comparar los PDFs
compare_pdfs(original_pdf_path, revised_pdf_path)
