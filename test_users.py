import requests
import utils
import pytest
from confest import base_url, headers
def test_existing_list_users(base_url, headers):
    page = 2
    data = requests.get(f"{base_url}/users?page={page}", headers=headers)
    utils.assert_status_ok(data)
    assert data.json()["page"] == page
    if page < len(data.json()["data"]):
        assert len(data.json()["data"]) == data.json()["per_page"]
    else:
        assert len(data.json()["data"]) <= data.json()["per_page"]

def test_non_existing_list_users(base_url, headers):
    page = 999
    data = requests.get(f"{base_url}/users?page={page}", headers=headers)
    assert data.status_code == 200
    json_data = data.json()
    assert json_data["data"] == []

def test_existing_user(base_url, headers):
    user = 2
    data = requests.get(f"{base_url}/users/{user}", headers=headers)
    utils.assert_status_ok(data)
    users = data.json()["data"]
    required_keys = {"id", "email", "first_name", "last_name", "avatar"}
    utils.assert_has_keys(users, required_keys)
    utils.is_valid_email(users["email"])
    
def test_non_existing_user(base_url, headers):
    user = 999
    data = requests.get(f"{base_url}/users/{user}", headers=headers)
    assert data.status_code == 404

def test_existing_list_unknown(base_url, headers):
    data = requests.get(f"{base_url}/unknown", headers=headers)
    utils.assert_status_ok(data)
    users = data.json()["data"]
    required_keys = {"id", "name", "year", "color", "pantone_value"}
    for user in users:
        utils.assert_has_keys(user, required_keys)

def test_existing_unknown(base_url, headers):
    data = requests.get(f"{base_url}/unknown/1", headers=headers)

    utils.assert_status_ok(data)
    users = data.json()["data"]

    required_keys = {"id", "name", "year", "color", "pantone_value"}
    utils.assert_has_keys(users, required_keys)

def test_non_existing_unknown(base_url, headers):
    data = requests.get(f"{base_url}/unknown/23", headers=headers)
    assert data.status_code == 404

@pytest.mark.parametrize("name, job", [
    ("Neo", "The One"),
    ("Trinity", "Hacker"),
    ("Morpheus", "Leader")])
def test_create_user_parametrized(base_url, headers, name, job):
    payload = {
        "name": name,
        "job": job
    }
    response = requests.post(f"{base_url}/users", json=payload, headers=headers)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == name
    assert data["job"] == job
    assert "id" in data
    assert "createdAt" in data
    utils.assert_datetime_format(data["createdAt"])

def test_update_user(base_url, headers):
    user_id = 2
    payload = {
        "name": "Neo",
        "job": "The One"
    }
    response = requests.put(f"{base_url}/users/{user_id}", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["job"] == payload["job"]
    assert "updatedAt" in data

    utils.assert_datetime_format(data["updatedAt"])

def test_patch_user(base_url, headers):
    user_id = 2
    payload = {
        "name": "Neo",
        "job": "The One"
    }
    response = requests.patch(f"{base_url}/users/{user_id}", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["job"] == payload["job"]
    assert "updatedAt" in data

    utils.assert_datetime_format(data["updatedAt"])

def test_delete_user(base_url, headers):
    user = 2
    data = requests.delete(f"{base_url}/users/{user}", headers=headers)
    assert data.status_code == 204


@pytest.mark.parametrize("number", [0, 1, 100])
def test_delay_list_users(base_url, headers, number):
    data = requests.get(f"{base_url}/users?delay={number}", headers=headers)
    utils.assert_status_ok(data)
    users = data.json()
    required_keys = {"page", "per_page", "total", "total_pages", "data"}
    utils.assert_has_keys(users, required_keys)