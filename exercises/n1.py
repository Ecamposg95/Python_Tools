import requests

# Defino el endpoint (la URI completa de la API)
url = "https://jsonplaceholder.typicode.com/users"

# Hago una solicitud GET
response = requests.get(url)

# Verifico que la respuesta fue exitosa (status code 200)
if response.status_code == 200:
    data = response.json()
    print("Usuarios obtenidos correctamente:")
    for user in data[:5]:  # Muestro solo los primeros 3
        print(f"- {user['name']} ({user['email']})")
        
else:
    print(f"Error al consultar la API: {response.status_code}")
