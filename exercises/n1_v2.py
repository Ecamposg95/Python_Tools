import requests

# Defino el endpoint (la URI completa de la API)
url = "https://jsonplaceholder.typicode.com/users"

try:
    # Hago la solicitud con un tiempo máximo de espera de 5 segundos
    response = requests.get(url, timeout=5)

    # Si hubo un error HTTP (por ejemplo, 404 o 500), lanza una excepción
    response.raise_for_status()

    # Si llegamos hasta aquí, la respuesta fue exitosa (status 200)
    data = response.json()
    print("Usuarios obtenidos correctamente:")

    for user in data[:6]:  # Muestro solo los primeros 3 usuarios
        print(f"- {user['name']} ({user['email']})")

# Si la API tarda demasiado
except requests.exceptions.Timeout:
    print("⚠️ La solicitud tardó demasiado en responder (timeout).")

# Si ocurre cualquier otro error (conexión, formato, etc.)
except requests.exceptions.RequestException as e:
    print("❌ Error en la solicitud:", e)
