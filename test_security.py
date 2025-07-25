import pytest
import requests
from confest import base_url, headers


def test_sql_injection_email(base_url, headers):
    payload = {"email": "test' OR 1=1 --", "password": "password123"}

    try:
        response = requests.post(f"{base_url}/login", json=payload, headers=headers)
        assert response.status_code in [400, 401, 403], f"Unexpected status: {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.skip(f"Request was blocked by security service (Cloudflare): {e}")

@pytest.mark.xfail(reason="Reqres.in does not sanitize XSS")
def test_xss_injection_name(base_url, headers):
    payload = {"name": "<script>alert(1)</script>", "job": "hacker"}
    response = requests.post(f"{base_url}/users", json=payload, headers=headers)
    data = response.json()
    print(response.text)  

    assert "<script>" not in data.get("name", ""), "XSS not sanitized"

@pytest.mark.xfail(reason="Reqres.in does not sanitize validation errors")
@pytest.mark.parametrize("name, job", [
    ("", ""),  # empty
    ("a"*1000, "b"*1000)  # long
])
def test_extreme_input_lengths(base_url, headers, name, job):
    payload = {"name": name, "job": job}
    response = requests.post(f"{base_url}/users", json=payload, headers=headers)
    print(response.text)  
    assert response.status_code in [201, 400]

@pytest.mark.xfail(reason="Reqres.in does not sanitize invalid data types")
@pytest.mark.parametrize("name, job", [
    (123, True),
    ([], {}),
])
def test_invalid_data_types(base_url, headers, name, job):
    payload = {"name": name, "job": job}
    response = requests.post(f"{base_url}/users", json=payload, headers=headers)
    print(response.text)  

    assert response.status_code in [400, 422]
