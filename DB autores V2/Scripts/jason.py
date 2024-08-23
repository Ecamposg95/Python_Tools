import pandas as pd
import json
import os

# Ruta del archivo Excel
input_file_path = r'C:\Users\ECG\Devs\Python_Tools\DB autores V2\Input\2_Autor.xlsx'

# Cargar el archivo Excel
df = pd.read_excel(input_file_path)

# Supongamos que la columna con los autores concatenados se llama "Autor"
# Si tiene otro nombre, ajústalo aquí
autores_concatenados = df['Autor (por punto y coma ;)'].dropna()

# Separar los autores que están concatenados por ';'
autores = []
for autores_grupo in autores_concatenados:
    autores.extend(autores_grupo.split(';'))

# Limpiar espacios en blanco y remover duplicados
autores = list(set(autor.strip() for autor in autores if autor.strip()))

# Ruta para guardar el archivo JSON
output_json_path = r'C:\Users\ECG\Devs\Python_Tools\DB autores V2\Output\autores.json'

# Guardar la lista de autores como un archivo JSON
os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(autores, f, ensure_ascii=False, indent=4)

print(f'Archivo JSON guardado en: {output_json_path}')
