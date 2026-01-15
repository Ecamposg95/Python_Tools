import requests

def test_get_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Error: código {response.status_code}")
    else:
        print("✅ API disponible y respondiendo correctamente")

    assert response.status_code == 200
