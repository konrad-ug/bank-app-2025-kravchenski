from src.accounts_registry import AccountsRegistry
from src.account import Account

def test_registry_add_and_find():
    reg = AccountsRegistry()
    acc1 = Account("Jan", "Kowalski", "12345678901")
    acc2 = Account("Anna", "Nowak", "12345678902")
    reg.add_account(acc1)
    reg.add_account(acc2)
    assert reg.count() == 2
    assert reg.find_by_pesel("12345678901") is acc1
    assert reg.find_by_pesel("12345678902") is acc2
    assert reg.find_by_pesel("00000000000") is None
    all_accs = reg.get_all_accounts()
    assert all_accs == [acc1, acc2]
    assert all_accs is not reg._accounts

def test_registry_duplicate_pesel():
    reg = AccountsRegistry()
    acc1 = Account("Jan", "Kowalski", "12345678901")
    acc2 = Account("Anna", "Nowak", "12345678901")
    reg.add_account(acc1)
    reg.add_account(acc2)
    assert reg.count() == 2

def test_registry_count_empty_and_after_add():
    reg = AccountsRegistry()
    assert reg.count() == 0
    acc1 = Account("Jan", "Kowalski", "12345678901")
    reg.add_account(acc1)
    assert reg.count() == 1
