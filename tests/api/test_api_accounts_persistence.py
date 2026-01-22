import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api/accounts"


@pytest.fixture(autouse=True)
def clear_registry_and_db():
    r = requests.get(BASE_URL)
    if r.status_code == 200:
        for acc in r.json():
            requests.delete(f"{BASE_URL}/{acc['pesel']}")
    requests.post(f"{BASE_URL}/save")


def test_save_accounts_returns_saved_count():
    data1 = {"name": "anna", "surname": "kowalska", "pesel": "85010112345"}
    data2 = {"name": "piotr", "surname": "nowak", "pesel": "86010112345"}
    requests.post(BASE_URL, json=data1)
    requests.post(BASE_URL, json=data2)

    r = requests.post(f"{BASE_URL}/save")

    assert r.status_code == 200
    assert r.json()["saved"] == 2


def test_load_accounts_overwrites_registry():
    data1 = {"name": "ewa", "surname": "zielinska", "pesel": "87010112345"}
    requests.post(BASE_URL, json=data1)
    requests.post(f"{BASE_URL}/87010112345/transfer", json={"amount": 100})
    requests.post(f"{BASE_URL}/save")

    data2 = {"name": "adam", "surname": "kowal", "pesel": "88010112345"}
    requests.post(BASE_URL, json=data2)

    r = requests.post(f"{BASE_URL}/load")
    assert r.status_code == 200
    assert r.json()["loaded"] == 1

    accounts = requests.get(BASE_URL).json()
    assert len(accounts) == 1
    assert accounts[0]["pesel"] == "87010112345"
    assert accounts[0]["balance"] == 100.0
