# -*- coding: utf-8 -*-
"""
Created on Wed May  8 16:15:54 2024

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

# Texto a ser hasheado
input_text = "Hola Mundo"
# Llamar a la función y imprimir el resultado
hash_result = generate_hash(input_text)
print(f"El hash SHA-256 de '{input_text}' es: {hash_result}")
