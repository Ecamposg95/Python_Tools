
import requests

r = requests.get('https://jsonplaceholder.typicode.com/users')


if r.status_code == 200:
    data = r.json()
    print("Usuarios obtenidos")
else:
    print("no encontrados")
