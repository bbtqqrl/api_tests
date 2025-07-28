import requests
import pytest
@pytest.mark.parametrize("email, password", [
    ("eve.holt@reqres.in", "pistol"),
    ("eve.holt@reqres.in", "1")])
def test_register_user(base_url, headers, email, password):
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{base_url}/register", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert "token" in data

@pytest.mark.parametrize("key, value", [
    ("email", "eve.holt@reqres.in"),
    ("password", "1")])
def test_invalid_register_user(base_url, headers, key, value):
    payload = {
        key : value
    }
    response = requests.post(f"{base_url}/register", json=payload, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data

@pytest.mark.parametrize("email, password", [
    ("eve.holt@reqres.in", "cityslicka")])
def test_login_user(base_url, headers, email, password):
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{base_url}/login", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "token" in data

@pytest.mark.parametrize("key, value", [
    ("email", "eve.holt@reqres.in"),
    ("password", "1")])
def test_invalid_login_user(base_url, headers, key, value):
    payload = {
        key : value
    }
    response = requests.post(f"{base_url}/login", json=payload, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data

