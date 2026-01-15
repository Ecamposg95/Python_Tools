# -*- coding: utf-8 -*-
"""
Created on Tue May  7 13:11:07 2024

@author: ecamp
"""
import qrcode
import os
from qrcode.image.svg import SvgImage

# Ubicación del directorio Output
output_dir = os.path.join(os.path.dirname(__file__), '..', 'Output')

# Datos que deseas incluir en el código QR
data = "https://maps.app.goo.gl/CwgmUt593fPKSKM1A"

# Generar el código QR
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
file_path = os.path.join(output_dir, 'maps.svg')

# Guardar la imagen en formato SVG
img.save(file_path)

print(f'Código QR guardado en formato SVG en {file_path}')
