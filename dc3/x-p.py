import os
import win32com.client

# Definir rutas
directorio_trabajo = r"C:\Users\ecamp\Devs\Python_Tools\dc3"
carpeta_entrada = os.path.join(directorio_trabajo, "Formatos_Generados")
carpeta_salida = os.path.join(directorio_trabajo, "PDF_Generados")

# Crear carpeta de salida si no existe
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

# Inicializar la aplicación de Excel
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False  # Mantener Excel en segundo plano

# Iterar sobre cada archivo Excel en la carpeta de entrada
for archivo in os.listdir(carpeta_entrada):
    if archivo.endswith(".xlsx"):  # Filtrar solo archivos de Excel
        ruta_excel = os.path.join(carpeta_entrada, archivo)
        ruta_pdf = os.path.join(carpeta_salida, archivo.replace(".xlsx", ".pdf"))

        try:
            # Abrir el archivo de Excel
            wb = excel.Workbooks.Open(ruta_excel)
            hoja = wb.Sheets(1)  # Seleccionar solo la primera hoja
            
            # Configurar el área de impresión para solo el rango deseado
            hoja.PageSetup.PrintArea = "$E$1:$AU$60"
            
            # Desactivar la impresión de cuadrículas
            hoja.PageSetup.PrintGridlines = False

            # Exportar solo la primera hoja a PDF
            hoja.ExportAsFixedFormat(0, ruta_pdf)

            # Cerrar el archivo sin guardar cambios
            wb.Close(SaveChanges=False)

            print(f"✅ PDF generado: {ruta_pdf}")

        except Exception as e:
            print(f"❌ Error al convertir {archivo}: {e}")

# Cerrar la aplicación de Excel
excel.Quit()

print("🎉 Todos los archivos han sido convertidos a PDF exitosamente (solo la primera hoja y sin cuadrícula).")
