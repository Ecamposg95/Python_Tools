import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Definir rutas
directorio_trabajo = r"C:\Users\ecamp\Devs\Python_Tools\dc3"
ruta_registros = os.path.join(directorio_trabajo, "DC3_resgistro.xlsx")
ruta_formato = os.path.join(directorio_trabajo, "DC-3-Formato.xlsx")
carpeta_salida = os.path.join(directorio_trabajo, "Formatos_Generados")

# Crear la carpeta de salida si no existe
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

# Verificar si los archivos de entrada existen
if not os.path.exists(ruta_registros):
    raise FileNotFoundError(f"El archivo de registros no existe: {ruta_registros}")
if not os.path.exists(ruta_formato):
    raise FileNotFoundError(f"El archivo de formato no existe: {ruta_formato}")

# Cargar base de datos de inscritos
try:
    df = pd.read_excel(ruta_registros, sheet_name="Hoja1")
except Exception as e:
    raise Exception(f"Error al leer el archivo de registros: {e}")

# Función para extraer cada dígito de una fecha en una lista
def descomponer_fecha(fecha):
    fecha_str = fecha.strftime("%Y%m%d")  # Convertir a string en formato YYYYMMDD
    return [int(digito) for digito in fecha_str]  # Retornar los dígitos separados en una lista

# Iterar sobre cada inscrito
for index, row in df.iterrows():
    try:
        # Validar que los campos requeridos no estén vacíos
        required_fields = ["Nombre", "CURP", "RFC_SHCP", "Ocupacion", "Duración del curso", "F_inicial", "F_final", 
                           "Puesto", "Empresa", "N_Curso", "Tematica", "Capacitador", "Instructor", "patron", "Representante"]
        for field in required_fields:
            if pd.isna(row[field]):
                raise ValueError(f"El campo {field} está vacío en el registro {index + 1}")

        # Cargar la plantilla del Formato DC-3
        wb = load_workbook(ruta_formato)
        ws = wb.active

        # 🔹 Descombinar celdas si están combinadas
        for merged_range in ws.merged_cells.ranges:
            if "E17" in merged_range.coord:
                ws.unmerge_cells(merged_range.coord)
            if "E29" in merged_range.coord:
                ws.unmerge_cells(merged_range.coord)
            if "E38" in merged_range.coord:
                ws.unmerge_cells(merged_range.coord)
            if "Z17" in merged_range.coord:  # Ocupación
                ws.unmerge_cells(merged_range.coord)

        # 🔹 Escribir la CURP carácter por carácter en la fila 17
        for i, char in enumerate(row["CURP"]):
            ws.cell(row=17, column=5 + i, value=char)  # E17 en adelante

        # 🔹 Escribir el RFC carácter por carácter en la fila 29
        for i, char in enumerate(row["RFC_SHCP"]):
            ws.cell(row=29, column=5 + i, value=char)  # E29 en adelante

        # 🔹 Escribir la Ocupación en Z17 con alineación a la izquierda
        ws["Z17"] = row["Ocupacion"]
        ws["Z17"].alignment = Alignment(horizontal="left", vertical="center")  # Alineado a la izquierda

        # 🔹 Fusionar celdas para "Duración en Horas" (de E38 a G38)
        ws.merge_cells("E38:G38")
        ws["E38"] = row["Duración del curso"]
        ws["E38"].alignment = Alignment(horizontal="center", vertical="center")  # Alineado al centro

        # 🔹 Escribir Año, Mes y Día (Inicio y Fin)
        digitos_inicio = descomponer_fecha(row["F_inicial"])
        digitos_fin = descomponer_fecha(row["F_final"])

        posiciones = {
            "año_inicio": [22, 23, 24, 25], "mes_inicio": [26, 27], "día_inicio": [30, 31],
            "año_fin": [36, 37, 38, 39], "mes_fin": [40, 41], "día_fin": [44, 45]
        }

        for i, col in enumerate(posiciones["año_inicio"]):
            ws.cell(row=38, column=col, value=digitos_inicio[i])
        for i, col in enumerate(posiciones["mes_inicio"]):
            ws.cell(row=38, column=col, value=digitos_inicio[4 + i])
        for i, col in enumerate(posiciones["día_inicio"]):
            ws.cell(row=38, column=col, value=digitos_inicio[6 + i])
        for i, col in enumerate(posiciones["año_fin"]):
            ws.cell(row=38, column=col, value=digitos_fin[i])
        for i, col in enumerate(posiciones["mes_fin"]):
            ws.cell(row=38, column=col, value=digitos_fin[4 + i])
        for i, col in enumerate(posiciones["día_fin"]):
            ws.cell(row=38, column=col, value=digitos_fin[6 + i])

        # 🔹 Escribir otros campos en el formato DC-3
        ws.cell(row=14, column=5, value=row["Nombre"])  # E14 -> Nombre
        ws.cell(row=20, column=5, value=row["Puesto"])  # E20 -> Puesto
        ws.cell(row=26, column=5, value=row["Empresa"])  # E26 -> Empresa
        ws.cell(row=35, column=5, value=row["N_Curso"])  # E35 -> Nombre del Curso

        ws.cell(row=41, column=5, value=row["Tematica"])  # E41 -> Área Temática
        ws.cell(row=44, column=5, value=row["Capacitador"])  # E44 -> Agente Capacitador
        ws.cell(row=53, column=8, value=row["Instructor"])  # H53 -> Instructor
        ws.cell(row=53, column=21, value=row["patron"])  # U53 -> Patrón o Representante Legal
        ws.cell(row=53, column=34, value=row["Representante"])  # AH53 -> Representante de Trabajadores

        # Guardar con un nuevo nombre basado en el nombre del inscrito
        nombre_archivo = f"DC3_{row['Nombre'].replace(' ', '_')}.xlsx"
        ruta_guardado = os.path.join(carpeta_salida, nombre_archivo)
        wb.save(ruta_guardado)

        logging.info(f"✅ Formato generado: {ruta_guardado}")
    except Exception as e:
        logging.error(f"❌ Error al procesar el registro {index + 1}: {e}")

logging.info("🎉 Proceso finalizado. Todos los formatos han sido generados correctamente.")

