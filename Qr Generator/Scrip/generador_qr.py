# -*- coding: utf-8 -*-
"""
Created on Tue May  7 13:24:10 2024

@author: ecamp
"""

import qrcode
import os
from qrcode.image.svg import SvgImage

def generar_codigo_qr(data, nombre_archivo):
    # Configurar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Crear una imagen del código QR en formato SVG
    img = qr.make_image(fill_color="black", back_color="white", image_factory=SvgImage)

    # Ruta del archivo donde se guardará el código QR en formato SVG
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'Output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, f'{nombre_archivo}.svg')

    # Guardar la imagen en formato SVG
    img.save(file_path)
    print(f'Código QR guardado en formato SVG en {file_path}')

if __name__ == "__main__":
    # Solicitar al usuario la URL y el nombre del archivo
    url = input("Introduce la URL para el código QR: ")
    nombre_archivo = input("Introduce el nombre del archivo para guardar el código QR: ")
    generar_codigo_qr(url, nombre_archivo)
