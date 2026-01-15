import requests

url = "https://httpbin.org/anything"

methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]

for method in methods:
    print("=" * 70)
    print(f"🔹 Probando método: {method}")
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json={"msg": "hola desde POST"}, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json={"msg": "actualizado con PUT"}, timeout=5)
        elif method == "PATCH":
            response = requests.patch(url, json={"msg": "cambio parcial con PATCH"}, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, timeout=5)
        elif method == "OPTIONS":
            response = requests.options(url, timeout=5)
        elif method == "HEAD":
            response = requests.head(url, timeout=5)

        print(f"➡️ Código de estado: {response.status_code}")
        print(f"➡️ Tipo de contenido: {response.headers.get('Content-Type')}")

        # Para métodos que devuelven JSON, imprimimos datos útiles
        if method not in ["HEAD"]:
            data = response.json()
            print("➡️ Método que el servidor detectó:", data.get("method"))
            print("➡️ URL:", data.get("url"))
            if "json" in data and data["json"]:
                print("➡️ Cuerpo JSON enviado:", data["json"])
        else:
            print("➡️ HEAD no tiene cuerpo de respuesta.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error con {method}: {e}")
