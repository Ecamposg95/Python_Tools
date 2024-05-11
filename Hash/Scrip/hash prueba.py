# -*- coding: utf-8 -*-
"""
Created on Wed May  8 16:21:13 2024

@author: ecamp
"""

import hashlib

def generate_hash(input_string):
    # Crear un objeto hash SHA-256
    hasher = hashlib.sha256()
    # Codificar la entrada y pasarla al objeto hash
    hasher.update(input_string.encode('utf-8'))
    # Obtener el hash en formato hexadecimal
    return hasher.hexdigest()

def verify_hash(input_string, given_hash):
    # Generar el hash del texto ingresado
    new_hash = generate_hash(input_string)
    # Comparar el nuevo hash con el hash dado
    if new_hash == given_hash:
        return True
    else:
        return False

# Texto original y el hash que queremos verificar
input_text = "Hola Mundo"
known_hash = "c3a4a2e49d91f2177113a9adfcb9ef9af9679dc4557a0a3a4602e1bd39a6f481"

# Verificar si el hash conocido corresponde al texto
if verify_hash(input_text, known_hash):
    print("El hash coincide con el texto.")
else:
    print("El hash no coincide con el texto.")
