import requests

url = "https://api.agify.io?name=emmanuel"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"Nombre: {data['name']}, Edad estimada: {data['age']}")
else:
    print("Error al consultar la API:", response.status_code)
