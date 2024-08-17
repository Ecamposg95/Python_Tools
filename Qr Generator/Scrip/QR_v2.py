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

# Crear el directorio Output si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Datos que deseas incluir en el código QR
data = "https://forms.gle/6at3toYjjTZ9goJH7"

# Generar el código QR
qr = qrcode.QRCode(
    version=10,  # Versión más alta para mayor densidad (versión va de 1 a 40)
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Mayor corrección de errores (hasta un 30% puede estar dañado)
    box_size=10,  # Tamaño de cada cuadro en píxeles
    border=4,  # Tamaño del borde
)
qr.add_data(data)
qr.make(fit=True)

# Crear una imagen del código QR en formato SVG
img = qr.make_image(image_factory=SvgImage)

# Ruta del archivo donde se guardará el código QR en formato SVG
file_path = os.path.join(output_dir, 'DINAMICA.svg')

# Guardar la imagen en formato SVG
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(img.to_string().decode('utf-8'))

print(f'Código QR con alta densidad guardado en formato SVG en {file_path}')

