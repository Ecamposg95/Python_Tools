import requests

def test_users_have_expected_fields():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url, timeout=5)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    expected_fields = {"id", "name", "email"}  # OJO: 'name' (no 'names')
    for user in data:
        # Verifica que al menos estén estos campos base
        assert expected_fields.issubset(user.keys()), f"Faltan campos en: {user}"
        assert isinstance(user["id"], int)
        assert isinstance(user["name"], str)
        assert isinstance(user["email"], str)
