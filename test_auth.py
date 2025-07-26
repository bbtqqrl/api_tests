import requests
import utils
import pytest
from datetime import datetime
BASE_URL = "https://reqres.in/api"
headers = {'x-api-key': 'reqres-free-v1'}
@pytest.mark.parametrize("email, password", [
    ("eve.holt@reqres.in", "pistol"),
    ("eve.holt@reqres.in", "1")])
def test_register_user(email, password):
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/register", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert "token" in data

@pytest.mark.parametrize("key, value", [
    ("email", "eve.holt@reqres.in"),
    ("password", "1")])
def test_invalid_register_user(key, value):
    payload = {
        key : value
    }
    response = requests.post(f"{BASE_URL}/register", json=payload, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data

@pytest.mark.parametrize("email, password", [
    ("eve.holt@reqres.in", "cityslicka")])
def test_login_user(email, password):
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/login", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "token" in data

@pytest.mark.parametrize("key, value", [
    ("email", "eve.holt@reqres.in"),
    ("password", "1")])
def test_invalid_login_user(key, value):
    payload = {
        key : value
    }
    response = requests.post(f"{BASE_URL}/login", json=payload, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "error" in data

