import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api/accounts"

@pytest.fixture(autouse=True)
def clear_registry():
    r = requests.get(BASE_URL)
    if r.status_code == 200:
        for acc in r.json():
            pesel = acc["pesel"]
            requests.delete(f"{BASE_URL}/{pesel}")

@pytest.fixture
def create_account():
    def _create(pesel, name="Jan", surname="Kowalski"):
        data = {"name": name, "surname": surname, "pesel": pesel}
        r = requests.post(BASE_URL, json=data)
        return r
    return _create

def test_create_account_unique(create_account):
    pesel = "12345678901"
    r = create_account(pesel)
    assert r.status_code == 201

def test_create_account_duplicate(create_account):
    pesel = "12345678901"
    create_account(pesel)
    r = create_account(pesel)
    assert r.status_code == 409
    assert "Account with this pesel already exists" in r.json()["error"]

def test_create_account_multiple_unique(create_account):
    pesel1 = "12345678901"
    pesel2 = "12345678902"
    r1 = create_account(pesel1)
    r2 = create_account(pesel2)
    assert r1.status_code == 201
    assert r2.status_code == 201

def test_create_account_missing_name(create_account):
    data = {"surname": "Kowalski", "pesel": "12345678903"}
    r = requests.post(BASE_URL, json=data)
    assert r.status_code == 400

def test_create_account_missing_surname(create_account):
    data = {"name": "Jan", "pesel": "12345678904"}
    r = requests.post(BASE_URL, json=data)
    assert r.status_code == 400

def test_create_account_missing_pesel(create_account):
    data = {"name": "Jan", "surname": "Kowalski"}
    r = requests.post(BASE_URL, json=data)
    assert r.status_code == 400

def test_create_account_empty_body():
    r = requests.post(BASE_URL, json={})
    assert r.status_code == 400

def test_create_account_invalid_method():
    r = requests.get(BASE_URL, json={"name": "Jan", "surname": "Kowalski", "pesel": "12345678905"})
    assert r.status_code == 200

def test_create_account_long_pesel(create_account):
    pesel = "123456789012345"
    r = create_account(pesel)
    assert r.status_code == 201

def test_create_account_short_pesel(create_account):
    pesel = "12345"
    r = create_account(pesel)
    assert r.status_code == 201
