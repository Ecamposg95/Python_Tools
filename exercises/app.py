from flask import Flask, jsonify, request
import requests
from collections import defaultdict

app = Flask(__name__)

SOURCE_URL_DEFAULT = "https://jsonplaceholder.typicode.com/users"

# ----------------------------
# Utilidades
# ----------------------------
def fetch_users(source_url: str, timeout: int = 5):
    resp = requests.get(source_url, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        raise ValueError("La fuente no devolvió una lista de usuarios.")
    return data

def extract_fields(users: list[dict]) -> list[str]:
    keys = set()
    for u in users:
        if isinstance(u, dict):
            keys.update(u.keys())
    return sorted(keys)

def pytype_name(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int) and not isinstance(value, bool):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, dict):
        return "dict"
    if isinstance(value, list):
        return "list"
    return type(value).__name__

def walk_schema(obj, prefix, types_map, presence_map, example_map):
    """
    Recorre dicts/listas y:
      - registra tipos por clave (con notación a.b.c)
      - cuenta presencia (veces que aparece la clave)
      - guarda un ejemplo (primera muestra no vacía)
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            tname = pytype_name(v)
            types_map[key].add(tname)
            presence_map[key] += 1
            if key not in example_map and v is not None:
                example_map[key] = v if not isinstance(v, (dict, list)) else None
            # Descenso
            if isinstance(v, dict):
                walk_schema(v, key, types_map, presence_map, example_map)
            elif isinstance(v, list):
                # Registramos tipo list y, si hay dicts dentro, descendemos con sufijo []
                for item in v:
                    if isinstance(item, dict):
                        walk_schema(item, key + "[]", types_map, presence_map, example_map)
    # Si fuera lista raíz, también la procesamos
    elif isinstance(obj, list):
        for item in obj:
            walk_schema(item, prefix + "[]", types_map, presence_map, example_map)

def build_schema(users: list[dict]):
    """
    Devuelve:
      - schema: { campo: {types: [...], presence: 0..1, example: ...} }
      - flat_fields: lista de campos
    """
    types_map = defaultdict(set)
    presence_map = defaultdict(int)
    example_map = {}

    total = len(users)
    for u in users:
        if isinstance(u, dict):
            walk_schema(u, "", types_map, presence_map, example_map)

    schema = {}
    for key in sorted(types_map.keys()):
        types_list = sorted(types_map[key])
        presence = presence_map[key] / total if total else 0.0
        item = {
            "types": types_list,
            "presence": round(presence, 3)
        }
        if key in example_map and example_map[key] is not None:
            item["example"] = example_map[key]
        schema[key] = item

    return schema, list(schema.keys())

# ----------------------------
# Endpoints
# ----------------------------
@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.get("/meta/users")
def users_meta():
    source_url = request.args.get("source_url", SOURCE_URL_DEFAULT)
    try:
        users = fetch_users(source_url)
        fields = extract_fields(users)
        sample_fields = sorted(users[0].keys()) if users and isinstance(users[0], dict) else []
        return jsonify({
            "source_url": source_url,
            "count": len(users),
            "fields": fields,
            "sample_fields": sample_fields
        }), 200
    except requests.exceptions.Timeout:
        return jsonify({"error": "Timeout consultando la fuente"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error HTTP al consultar la fuente: {str(e)}"}), 502
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

@app.get("/meta/users/schema")
def users_schema():
    """
    Devuelve un esquema inferido:
      - count: número de usuarios
      - fields: lista de campos (incluye anidados: address.city, company.name)
      - schema: dict con types, presence (0..1) y example (cuando aplica)
    Notación:
      - a.b.c  => claves anidadas en dict
      - a[]    => elementos de lista (y a[].b para claves dentro de dicts en listas)
    """
    source_url = request.args.get("source_url", SOURCE_URL_DEFAULT)
    try:
        users = fetch_users(source_url)
        schema, flat_fields = build_schema(users)
        return jsonify({
            "source_url": source_url,
            "count": len(users),
            "fields": flat_fields,
            "schema": schema
        }), 200
    except requests.exceptions.Timeout:
        return jsonify({"error": "Timeout consultando la fuente"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error HTTP al consultar la fuente: {str(e)}"}), 502
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 500
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
