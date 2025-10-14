import re
import pandas as pd
from pathlib import Path

# =========================================
#  CONFIGURACIÓN DE RUTAS (ROBUSTA)
# =========================================
BASE_DIR = Path(r"C:\Users\ecamp\Devs\Python_Tools\Normalizacion DB  data X POS")

# intenta primero la versión limpia; si no, usa la original
CANDIDATES = ["db_general_limpio.xlsx", "db_general.xlsx"]

INPUT_FILE = None
for name in CANDIDATES:
    p = BASE_DIR / name
    if p.exists():
        INPUT_FILE = str(p)
        break

if INPUT_FILE is None:
    files = "\n  - " + "\n  - ".join(sorted(f.name for f in BASE_DIR.glob("*.xlsx")))
    raise FileNotFoundError(
        f"No encontré ninguno de: {CANDIDATES} en:\n{BASE_DIR}\n"
        f"Archivos .xlsx disponibles:{files if files.strip() else ' (ninguno)'}"
    )

SHEET_WANTED = "h1"  # nombre esperado de hoja (case-insensitive)
OUTPUT_FILE = BASE_DIR / "coincidencias_humanas.xlsx"

# Nombres de columnas en tu Excel
COL_CODIGO = "Código"
COL_DESC   = "Descripción"

print(f"Usando archivo: {INPUT_FILE}")

# =========================================
#  UTILIDADES
# =========================================
def elegir_hoja_case_insensitive(xlsx_path: str, wanted: str) -> str:
    xl = pd.ExcelFile(xlsx_path)
    wanted_norm = wanted.strip().lower()
    for s in xl.sheet_names:
        if s.strip().lower() == wanted_norm:
            return s
    raise ValueError(f"No encontré la hoja '{wanted}'. Hojas disponibles: {', '.join(xl.sheet_names)}")

def normaliza_codigo(s: str) -> str:
    """Mayúsculas + elimina todo lo que no sea A-Z o 0-9."""
    if not isinstance(s, str):
        s = "" if pd.isna(s) else str(s)
    s = s.upper().strip()
    return re.sub(r"[^A-Z0-9]", "", s)

def extrae_codigo_inicio_desc(desc: str) -> str:
    """Extrae el primer token tipo código al INICIO de la descripción y lo normaliza."""
    if not isinstance(desc, str):
        desc = "" if pd.isna(desc) else str(desc)
    m = re.match(r"^([A-Z0-9][A-Z0-9\-/_.]*)", desc.strip().upper())
    return normaliza_codigo(m.group(1)) if m else ""

def partes_codigo(code_norm: str):
    """
    Divide un código normalizado en (prefijo letras, número, sufijo letras).
    Ej.: 'JL1004' -> ('JL', '1004', '')
          '1004'   -> ('', '1004', '')
          'JL1004A'-> ('JL','1004','A')
    """
    if not code_norm:
        return ("", "", "")
    m = re.match(r"^([A-Z]*)(\d+)([A-Z]*)$", code_norm)
    if m:
        return m.group(1), m.group(2), m.group(3)
    # fallback: primera racha de dígitos
    m2 = re.search(r"(\d+)", code_norm)
    if not m2:
        return ("", "", "")
    num = m2.group(1)
    start, end = m2.span()
    pref = re.sub(r"[^A-Z]", "", code_norm[:start])
    suf  = re.sub(r"[^A-Z]", "", code_norm[end:])
    return (pref, num, suf)

# =========================================
#  CARGA DE DATOS
# =========================================
SHEET_NAME = elegir_hoja_case_insensitive(INPUT_FILE, SHEET_WANTED)
df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME, dtype=str)

# Validación de columnas
missing = [c for c in (COL_CODIGO, COL_DESC) if c not in df.columns]
if missing:
    raise ValueError(f"Faltan columnas: {missing}. Encontradas: {list(df.columns)}")

df = df.copy()
df["codigo_raw"] = df[COL_CODIGO].fillna("").astype(str).str.strip()
df["descripcion_raw"] = df[COL_DESC].fillna("").astype(str).str.strip()

# Normalización y elección del mejor código
df["codigo_norm"]      = df["codigo_raw"].apply(normaliza_codigo)
df["codigo_desc_norm"] = df["descripcion_raw"].apply(extrae_codigo_inicio_desc)

df["codigo_mejor"] = df["codigo_norm"]
df.loc[df["codigo_mejor"] == "", "codigo_mejor"] = df["codigo_desc_norm"]

# Partes del código
df[["prefijo","numero","sufijo"]] = df["codigo_mejor"].apply(
    lambda c: pd.Series(partes_codigo(c))
)

# Filtra filas con número válido
base = df[df["numero"] != ""].copy()

# =========================================
#  COINCIDENCIAS “HUMANAS”
#  - mismo número
#  - mismo sufijo (o ambos vacíos)
#  - prefijo distinto (incluye vacío vs letras)
#  => NO mezcla sufijos (A, B, OC, etc.)
# =========================================
pairs = []
grp = base.groupby(["numero", "sufijo"], dropna=False, as_index=False)

for (numero, sufijo), g in grp:
    if len(g) < 2:
        continue
    g = g.reset_index(drop=False)  # conserva índice original
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            a = g.loc[i]
            b = g.loc[j]
            if a["codigo_mejor"] == b["codigo_mejor"]:
                continue
            if a["prefijo"] != b["prefijo"]:
                pairs.append({
                    "numero": numero,
                    "sufijo": sufijo,
                    "codigo_a": a["codigo_mejor"],
                    "codigo_b": b["codigo_mejor"],
                    "prefijo_a": a["prefijo"],
                    "prefijo_b": b["prefijo"],
                    "desc_a": a["descripcion_raw"],
                    "desc_b": b["descripcion_raw"],
                    "motivo": "mismo número + mismo sufijo; prefijo diferente",
                    "Elegir_codigo_final": ""  # para tu selección manual
                    
                    
                })

coinc = pd.DataFrame(pairs, columns=[
    "numero","sufijo","codigo_a","codigo_b","prefijo_a","prefijo_b",
    "desc_a","desc_b","motivo","Elegir_codigo_final"
])

# Orden agradable
if not coinc.empty:
    coinc = coinc.sort_values(["numero","sufijo","codigo_a","codigo_b"]).reset_index(drop=True)

# Tabla de control con normalización
codigos_normalizados = base[[
    "codigo_raw","descripcion_raw","codigo_mejor","prefijo","numero","sufijo"
]].drop_duplicates().sort_values(["numero","sufijo","codigo_mejor"])

# =========================================
#  EXPORTAR
# =========================================
with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as xw:
    codigos_normalizados.to_excel(xw, sheet_name="codigos_normalizados", index=False)
    coinc.to_excel(xw, sheet_name="posibles_coincidencias", index=False)

print(f"Listo.\n- Archivo de salida: {OUTPUT_FILE}")
print("Abre la hoja 'posibles_coincidencias' para revisar (ej. 1004 ↔ JL1004).")
print("Completa 'Elegir_codigo_final' si quieres estandarizar manualmente.")
