# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 21:54:49 2024

@author: ecamp
"""
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os

# Ruta del archivo de salida PDF
output_pdf_path = "Resultados_Completos_Interes_Simple_Compuesto.pdf"

# Función para generar la imagen de la fórmula usando matplotlib
def create_formula_image(formula, filename):
    plt.figure(figsize=(5, 0.5), dpi=200)
    plt.text(0.5, 0.5, f"${formula}$", fontsize=14, ha='center', va='center')
    plt.axis('off')
    plt.savefig(filename, format='png', bbox_inches='tight', pad_inches=0.1)
    plt.close()

# Función para añadir un ejercicio al PDF
def add_exercise(canvas, title, description, formula_image_path, explanation, calculation_image_path, x=50, y=750):
    # Título del ejercicio
    canvas.setFont("Helvetica-Bold", 14)
    canvas.setFillColor(colors.black)
    canvas.drawString(x, y, title)
    
    # Descripción del ejercicio
    canvas.setFont("Helvetica", 12)
    canvas.drawString(x, y - 20, description)

    # Insertar imagen de la fórmula
    canvas.drawImage(formula_image_path, x, y - 90, width=200, height=40)

    # Explicación de cada valor
    y_position = y - 140
    for line in explanation:
        canvas.setFont("Helvetica", 12)
        canvas.drawString(x, y_position, line)
        y_position -= 15

    # Cálculo final
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(x, y_position - 20, "Cálculo:")
    canvas.drawImage(calculation_image_path, x, y_position - 70, width=250, height=40)

# Crear el PDF
c = canvas.Canvas(output_pdf_path, pagesize=A4)
width, height = A4

# Información de cada ejercicio
exercises = [
    {
        "title": "Ejercicio 1",
        "description": "Interés simple sobre $1,250 para dos años al 5%",
        "formula": r"Interes = Capital \times Tasa \times Tiempo",
        "explanation": [
            "Capital: $1,250",
            "Tasa: 5%",
            "Tiempo: 2 años"
        ],
        "calculation": r"Interes = 1250 \times 0.05 \times 2 = 125.00"
    },
    {
        "title": "Ejercicio 2",
        "description": "Tasa para que $1,250 se acumulen a $1,362.50 en dos años",
        "formula": r"Tasa = \frac{Monto \ final - Capital}{Capital \times Tiempo}",
        "explanation": [
            "Monto final: $1,362.50",
            "Capital: $1,250",
            "Tiempo: 2 años"
        ],
        "calculation": r"Tasa = \frac{1362.5 - 1250}{1250 \times 2} = 0.045 \ o \ 4.5\%"
    },
    {
        "title": "Ejercicio 3",
        "description": "Tiempo para que $500 se acumulen a $525 al 4% de interés simple",
        "formula": r"Tiempo = \frac{Monto \ final - Capital}{Capital \times Tasa}",
        "explanation": [
            "Monto final: $525",
            "Capital: $500",
            "Tasa: 4%"
        ],
        "calculation": r"Tiempo = \frac{525 - 500}{500 \times 0.04} = 1.25 \ años"
    },
    {
        "title": "Ejercicio 4",
        "description": "Interés simple sobre $285 para 1 ½ años al 4.75%",
        "formula": r"Interes = Capital \times Tasa \times Tiempo",
        "explanation": [
            "Capital: $285",
            "Tasa: 4.75%",
            "Tiempo: 1.5 años"
        ],
        "calculation": r"Interes = 285 \times 0.0475 \times 1.5 = 20.31"
    },
    {
        "title": "Ejercicio 5",
        "description": "Interés simple sobre $530 para 4 meses al 4.5%",
        "formula": r"Interes = Capital \times Tasa \times Tiempo",
        "explanation": [
            "Capital: $530",
            "Tasa: 4.5%",
            "Tiempo: 4/12 años"
        ],
        "calculation": r"Interes = 530 \times 0.045 \times 0.333 = 7.95"
    },
    {
        "title": "Ejercicio 6",
        "description": "Monto acumulado para $8,000 a una tasa del 36% anual, capitalizable mensualmente durante cuatro años",
        "formula": r"Monto = Capital \times \left(1 + \frac{Tasa}{Frecuencia}\right)^{Frecuencia \times Tiempo}",
        "explanation": [
            "Capital: $8,000",
            "Tasa: 36%",
            "Tiempo: 4 años",
            "Frecuencia de capitalización: 12"
        ],
        "calculation": r"Monto = 8000 \times \left(1 + \frac{0.36}{12}\right)^{12 \times 4} = 33058.02"
    },
    {
       "title": "Ejercicio 7a",
       "description": "Valor final a tasa de interés simple para $50,000 al 30% anual durante tres meses",
       "formula": r"Monto = Capital + (Capital \times Tasa \times Tiempo)",
       "explanation": ["Capital: $50,000", "Tasa: 30%", "Tiempo: 0.25 años"],
       "calculation": r"Monto = 50000 + (50000 \times 0.30 \times 0.25) = 53750.00"
   },
   {
       "title": "Ejercicio 7b",
       "description": "Valor final a interés compuesto al 30% anual capitalizable mensualmente",
       "formula": r"Monto = Capital \times \left(1 + \frac{Tasa}{Frecuencia}\right)^{Frecuencia \times Tiempo}",
       "explanation": ["Capital: $50,000", "Tasa: 30%", "Tiempo: 0.25 años", "Frecuencia de capitalización: 12"],
       "calculation": r"Monto = 50000 \times \left(1 + \frac{0.30}{12}\right)^{12 \times 0.25} = 53844.53"
   },
   {
       "title": "Ejercicio 8",
       "description": "Valor final de $20,000 a un interés compuesto durante 15 meses y 15 días, al 24% capitalizable mensualmente",
       "formula": r"Monto = Capital \times \left(1 + \frac{Tasa}{Frecuencia}\right)^{Frecuencia \times Tiempo}",
       "explanation": ["Capital: $20,000", "Tasa: 24%", "Tiempo: 15.5 meses (1.29 años)", "Frecuencia de capitalización: 12"],
       "calculation": r"Monto = 20000 \times \left(1 + \frac{0.24}{12}\right)^{12 \times 1.29} = 27185.21"
   },
   {
       "title": "Ejercicio 9",
       "description": "Monto final de $8,000 invertidos por un año con 12% capitalizable mensualmente los primeros tres meses y 18% para el resto del año",
       "formula": r"Monto = Monto_{3 \ meses} \times \left(1 + \frac{Tasa_{posterior}}{Frecuencia}\right)^{Frecuencia \times Tiempo}",
       "explanation": ["Capital: $8,000", "Tasa inicial: 12%", "Tasa posterior: 18%", "Tiempo total: 1 año"],
       "calculation": r"Monto = 8242.88 \times \left(1 + \frac{0.18}{12}\right)^{12 \times 0.75} = 9424.29"
   },
   {
       "title": "Ejercicio 10",
       "description": "Monto final de $10,000 a 18% capitalizable mensualmente, con retiro de $4,000 después de cuatro meses",
       "formula": r"Monto \ final = (Monto_{4 \ meses} - Retiro) \times \left(1 + \frac{Tasa}{Frecuencia}\right)^{Frecuencia \times Tiempo \ restante}",
       "explanation": ["Capital: $10,000", "Tasa: 18%", "Tiempo total: 1 año", "Retiro: $4,000 después de 4 meses"],
        "calculation": r"Monto \ final = (10394.21 - 4000) \times \left(1 + \frac{0.18}{12}\right)^{12 \times 0.67} = 7450.21"
    }
]
    # Agrega más ejercicios aquí siguiendo el mismo formato


# Generar contenido para cada ejercicio
for exercise in exercises:
    # Crear imagen de la fórmula y del cálculo
    formula_image_path = "formula_image.png"
    calculation_image_path = "calculation_image.png"
    create_formula_image(exercise["formula"], formula_image_path)
    create_formula_image(exercise["calculation"], calculation_image_path)

    # Agregar el ejercicio al PDF
    add_exercise(
        c, 
        exercise["title"], 
        exercise["description"], 
        formula_image_path, 
        exercise["explanation"], 
        calculation_image_path, 
        x=50, 
        y=750
    )
    c.showPage()  # Nueva página para cada ejercicio

# Guardar el PDF
c.save()

# Limpiar imágenes temporales
os.remove("formula_image.png")
os.remove("calculation_image.png")

print(f"PDF generado en: {output_pdf_path}")
