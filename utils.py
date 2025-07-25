from datetime import datetime
import re
import pytest

def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # Basic email pattern
    return bool(re.fullmatch(pattern, email))

def assert_datetime_format(dt: str):
    try:
        datetime.fromisoformat(dt.replace("Z", "+00:00"))
    except ValueError:
        pytest.fail("Invalid ISO datetime format")

def assert_has_keys(obj: dict, keys: set):
    assert keys.issubset(obj.keys()), f"Missing keys: {keys - set(obj.keys())}"

def assert_status_ok(data):
    assert data.status_code == 200
    assert "data" in data.json()