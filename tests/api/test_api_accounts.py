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

def test_create_account():
    data = {"name": "james", "surname": "hetfield", "pesel": "89092909825"}
    r = requests.post(BASE_URL, json=data)
    assert r.status_code == 201
    assert r.json()["message"] == "Account created"

def test_get_all_accounts():
    data = {"name": "lars", "surname": "ulrich", "pesel": "80010112345"}
    requests.post(BASE_URL, json=data)
    r = requests.get(BASE_URL)
    assert r.status_code == 200
    accounts = r.json()
    assert any(acc["pesel"] == "80010112345" for acc in accounts)

def test_get_account_count():
    r = requests.get(BASE_URL + "/count")
    assert r.status_code == 200
    assert "count" in r.json()

def test_get_account_by_pesel():
    pesel = "90010111111"
    data = {"name": "kirk", "surname": "hammett", "pesel": pesel}
    requests.post(BASE_URL, json=data)
    r = requests.get(f"{BASE_URL}/{pesel}")
    assert r.status_code == 200
    assert r.json()["pesel"] == pesel

def test_get_account_by_pesel_404():
    r = requests.get(f"{BASE_URL}/00000000000")
    assert r.status_code == 404

def test_update_account():
    pesel = "91010122222"
    data = {"name": "robert", "surname": "trujillo", "pesel": pesel}
    requests.post(BASE_URL, json=data)
    patch = {"name": "rob"}
    r = requests.patch(f"{BASE_URL}/{pesel}", json=patch)
    assert r.status_code == 200
    r2 = requests.get(f"{BASE_URL}/{pesel}")
    assert r2.json()["name"] == "rob"

def test_delete_account():
    pesel = "92010133333"
    data = {"name": "jason", "surname": "newsted", "pesel": pesel}
    requests.post(BASE_URL, json=data)
    r = requests.delete(f"{BASE_URL}/{pesel}")
    assert r.status_code == 200
    r2 = requests.get(f"{BASE_URL}/{pesel}")
    assert r2.status_code == 404

def test_create_account_duplicate_pesel():
    data = {"name": "james", "surname": "hetfield", "pesel": "89092909825"}
    r1 = requests.post(BASE_URL, json=data)
    r2 = requests.post(BASE_URL, json=data)
    assert r1.status_code == 201
    assert r2.status_code in (400, 409)

def test_update_account_only_surname():
    pesel = "93010144444"
    data = {"name": "anna", "surname": "kowalska", "pesel": pesel}
    requests.post(BASE_URL, json=data)
    patch = {"surname": "nowak"}
    r = requests.patch(f"{BASE_URL}/{pesel}", json=patch)
    assert r.status_code == 200
    r2 = requests.get(f"{BASE_URL}/{pesel}")
    assert r2.json()["surname"] == "nowak"
    assert r2.json()["name"] == "anna"

def test_update_account_not_found():
    pesel = "00000000001"
    patch = {"name": "ghost"}
    r = requests.patch(f"{BASE_URL}/{pesel}", json=patch)
    assert r.status_code == 404

def test_delete_account_not_found():
    pesel = "00000000002"
    r = requests.delete(f"{BASE_URL}/{pesel}")
    assert r.status_code == 404

def test_create_account_missing_field():
    data = {"name": "jan", "pesel": "95010155555"}
    r = requests.post(BASE_URL, json=data)
    assert r.status_code == 400
