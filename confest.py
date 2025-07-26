import pytest

@pytest.fixture
def base_url():
    return "https://reqres.in/api"

@pytest.fixture
def headers():
    return {"x-api-key": "reqres-free-v1"}