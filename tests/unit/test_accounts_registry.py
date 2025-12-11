import pytest
from src.account import Account
from src.accounts_registry import AccountsRegistry

@pytest.fixture
def registry():
    return AccountsRegistry()

@pytest.fixture
def sample_accounts():
    return [
        Account("Jan", "Kowalski", "12345678901"),
        Account("Anna", "Nowak", "98765432109"),
        Account("Piotr", "Zielinski", "11122233344"),
    ]

def test_add_and_count_accounts(registry, sample_accounts):
    for acc in sample_accounts:
        registry.add_account(acc)
    assert registry.count() == 3

def test_find_by_pesel(registry, sample_accounts):
    for acc in sample_accounts:
        registry.add_account(acc)
    found = registry.find_by_pesel("98765432109")
    assert found is sample_accounts[1]
    not_found = registry.find_by_pesel("00000000000")
    assert not_found is None

def test_get_all_accounts(registry, sample_accounts):
    for acc in sample_accounts:
        registry.add_account(acc)
    all_accs = registry.get_all_accounts()
    assert all_accs == sample_accounts
    assert all_accs is not sample_accounts  # copy, not ref
