import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:5000/api/accounts"
TIMEOUT_LIMIT = 0.5


@pytest.fixture(autouse=True)
def clear_registry():
    r = requests.get(BASE_URL)
    if r.status_code == 200:
        for acc in r.json():
            pesel = acc["pesel"]
            requests.delete(f"{BASE_URL}/{pesel}")


def test_create_and_delete_account_100_times():
    for i in range(100):
        pesel = f"{90000000000 + i}"
        data = {"name": "Test", "surname": "User", "pesel": pesel}
        
        start_time = time.time()
        r = requests.post(BASE_URL, json=data, timeout=TIMEOUT_LIMIT)
        elapsed_time = time.time() - start_time
        
        assert r.status_code == 201, f"Create failed for iteration {i}"
        assert elapsed_time < TIMEOUT_LIMIT, f"Create took {elapsed_time}s, exceeded {TIMEOUT_LIMIT}s limit"
        
        start_time = time.time()
        r = requests.delete(f"{BASE_URL}/{pesel}", timeout=TIMEOUT_LIMIT)
        elapsed_time = time.time() - start_time
        
        assert r.status_code == 200, f"Delete failed for iteration {i}"
        assert elapsed_time < TIMEOUT_LIMIT, f"Delete took {elapsed_time}s, exceeded {TIMEOUT_LIMIT}s limit"


def test_create_account_and_100_transfers():
    pesel = "85010198765"
    data = {"name": "Transfer", "surname": "Test", "pesel": pesel}
    
    start_time = time.time()
    r = requests.post(BASE_URL, json=data, timeout=TIMEOUT_LIMIT)
    elapsed_time = time.time() - start_time
    
    assert r.status_code == 201, "Account creation failed"
    assert elapsed_time < TIMEOUT_LIMIT, f"Account creation took {elapsed_time}s"
    
    expected_balance = 0.0
    for i in range(100):
        amount = 100.0 + i
        expected_balance += amount
        
        start_time = time.time()
        r = requests.post(f"{BASE_URL}/{pesel}/transfer", json={"amount": amount}, timeout=TIMEOUT_LIMIT)
        elapsed_time = time.time() - start_time
        
        assert r.status_code == 200, f"Transfer {i} failed"
        assert elapsed_time < TIMEOUT_LIMIT, f"Transfer {i} took {elapsed_time}s, exceeded {TIMEOUT_LIMIT}s limit"
    
    r = requests.get(f"{BASE_URL}/{pesel}")
    assert r.status_code == 200
    assert r.json()["balance"] == expected_balance, f"Expected balance {expected_balance}, got {r.json()['balance']}"
    
    requests.delete(f"{BASE_URL}/{pesel}")


def test_create_1000_accounts_then_delete_all():
    pesel_list = []
    
    for i in range(1000):
        pesel = f"{80000000000 + i}"
        pesel_list.append(pesel)
        data = {"name": "Bulk", "surname": f"User{i}", "pesel": pesel}
        
        start_time = time.time()
        r = requests.post(BASE_URL, json=data, timeout=TIMEOUT_LIMIT)
        elapsed_time = time.time() - start_time
        
        assert r.status_code == 201, f"Create failed for account {i}"
        assert elapsed_time < TIMEOUT_LIMIT, f"Create account {i} took {elapsed_time}s"
    
    for i, pesel in enumerate(pesel_list):
        start_time = time.time()
        r = requests.delete(f"{BASE_URL}/{pesel}", timeout=TIMEOUT_LIMIT)
        elapsed_time = time.time() - start_time
        
        assert r.status_code == 200, f"Delete failed for account {i}"
        assert elapsed_time < TIMEOUT_LIMIT, f"Delete account {i} took {elapsed_time}s"
