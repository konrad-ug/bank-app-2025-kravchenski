import pytest

from src.account import Account
from src.accounts_registry import AccountsRegistry
from src.company_account import CompanyAccount


@pytest.mark.parametrize(
    "pesel, expected",
    [
        ("12345678901", True),
        ("00000000000", True),
        ("ABCDEFGHIJK", True),
        ("1234567890a", True),
        ("1234567890 ", True),
        (" 1234567890", True),
        ("1234567890-", True),
        ("XXXXXXXXXXX", True),
        ("1234567890", False),
        ("123456789012", False),
        ("", False),
        (None, False),
        (12345678901, False),
        ("12345", False),
        ("123456789", False),
        ("123456789011", False),
        (["12345678901"], False),
        ({"pesel": "12345678901"}, False),
    ],
)
def test_is_pesel_valid_cases(pesel, expected):
    account = Account("A", "B", "12345678901")
    assert account.is_pesel_valid(pesel) is expected


@pytest.mark.parametrize(
    "promo_code, expected",
    [
        ("PROM_1", True),
        ("PROM_ABC", True),
        ("PROM_ ", True),
        ("PROM_12345", True),
        ("PROM_", False),
        ("PROM", False),
        ("PRO_M123", False),
        ("", False),
        (None, False),
        (123, False),
        ("XPROM_1", False),
        ("prom_1", False),
    ],
)
def test_is_promocode_valid_cases(promo_code, expected):
    account = Account("A", "B", "12345678901")
    assert account.is_promocode_valid(promo_code) is expected


@pytest.mark.parametrize(
    "pesel, expected_year",
    [
        ("02222912345", 2002),
        ("61010112345", 1961),
        ("05223912345", 2005),
        ("99123112345", 1999),
        ("00222912345", 2000),
        ("83222912345", 2083),
        ("81923112345", 1881),
        ("12345678901", None),
        ("99139912345", None),
        ("9913991234A", None),
        ("invalidpesel", None),
        (None, None),
    ],
)
def test_extract_birth_year_cases(pesel, expected_year):
    account = Account("A", "B", "12345678901")
    account.pesel = pesel
    assert account.extract_birth_year() == expected_year


@pytest.mark.parametrize(
    "amount, expected_result, expected_balance, expected_history",
    [
        (100, True, 100.0, [100.0]),
        (0, False, 0.0, []),
        (-50, False, 0.0, []),
        (99.99, True, 99.99, [99.99]),
        ("100", False, 0.0, []),
        (None, False, 0.0, []),
        (True, True, 1.0, [1.0]),
        (0.25, True, 0.25, [0.25]),
        (1, True, 1.0, [1.0]),
        (-0.01, False, 0.0, []),
    ],
)
def test_receive_transfer_cases(amount, expected_result, expected_balance, expected_history):
    account = Account("A", "B", "12345678901")
    result = account.receive_transfer(amount)
    assert result is expected_result
    assert account.balance == expected_balance
    assert account.history == expected_history


@pytest.mark.parametrize(
    "start_balance, amount, expected_result, expected_balance, expected_history",
    [
        (100, 50, True, 50.0, [-50.0]),
        (100, 100, True, 0.0, [-100.0]),
        (100, 0, False, 100.0, []),
        (100, -1, False, 100.0, []),
        (100, 150, False, 100.0, []),
        (0, 1, False, 0.0, []),
        (10.5, 5.25, True, 5.25, [-5.25]),
        (1, True, True, 0.0, [-1.0]),
    ],
)
def test_send_transfer_cases(start_balance, amount, expected_result, expected_balance, expected_history):
    account = Account("A", "B", "12345678901")
    account.balance = start_balance
    result = account.send_transfer(amount)
    assert result is expected_result
    assert account.balance == expected_balance
    assert account.history == expected_history


@pytest.mark.parametrize(
    "start_balance, amount, expected_result, expected_balance, expected_history",
    [
        (100, 50, True, 49.0, [-50.0, -1.0]),
        (50, 49, True, 0.0, [-49.0, -1.0]),
        (10, 10, True, -1.0, [-10.0, -1.0]),
        (9, 10, True, -2.0, [-10.0, -1.0]),
        (8.9, 10, False, 8.9, []),
        (0, 1, True, -2.0, [-1.0, -1.0]),
        (100, 0, False, 100.0, []),
        (100, -5, False, 100.0, []),
    ],
)
def test_send_express_transfer_cases(start_balance, amount, expected_result, expected_balance, expected_history):
    account = Account("A", "B", "12345678901")
    account.balance = start_balance
    result = account.send_express_transfer(amount)
    assert result is expected_result
    assert account.balance == expected_balance
    assert account.history == expected_history


@pytest.mark.parametrize(
    "data, expected_name, expected_surname, expected_pesel, expected_balance, expected_history, expect_exception",
    [
        (
            {"name": "A", "surname": "B", "pesel": "12345678901", "balance": 100, "history": [1, 2, -3]},
            "A",
            "B",
            "12345678901",
            100.0,
            [1.0, 2.0, -3.0],
            False,
        ),
        (
            {"first_name": "A", "last_name": "B", "pesel": "12345678901", "balance": "200.5", "history": ["1.5", "-2"]},
            "A",
            "B",
            "12345678901",
            200.5,
            [1.5, -2.0],
            False,
        ),
        (
            {"name": "A", "surname": "B", "pesel": "12345678901", "balance": "bad", "history": [1]},
            "A",
            "B",
            "12345678901",
            0.0,
            [1.0],
            False,
        ),
        (
            {"name": "A", "surname": "B", "pesel": "12345678901", "history": None},
            "A",
            "B",
            "12345678901",
            0.0,
            [],
            False,
        ),
        (
            {"name": "A", "surname": "B", "pesel": "12345678901"},
            "A",
            "B",
            "12345678901",
            0.0,
            [],
            False,
        ),
        (
            {"name": None, "surname": None, "pesel": "12345678901", "balance": 50},
            "",
            "",
            "12345678901",
            50.0,
            [],
            False,
        ),
        (
            {"name": "A", "surname": "B", "pesel": None, "balance": 10, "history": [0]},
            "A",
            "B",
            "Invalid",
            10.0,
            [0.0],
            False,
        ),
        (
            None,
            None,
            None,
            None,
            None,
            None,
            True,
        ),
    ],
)
def test_from_dict_cases(
    data,
    expected_name,
    expected_surname,
    expected_pesel,
    expected_balance,
    expected_history,
    expect_exception,
):
    if expect_exception:
        with pytest.raises(ValueError):
            Account.from_dict(data)
        return
    account = Account.from_dict(data)
    assert account.first_name == expected_name
    assert account.last_name == expected_surname
    assert account.pesel == expected_pesel
    assert account.balance == expected_balance
    assert account.history == expected_history


@pytest.mark.parametrize(
    "nip, expected",
    [
        ("1234567890", True),
        ("0000000000", True),
        ("123456789", False),
        ("12345678901", False),
        ("12345abcde", False),
        (None, False),
        (1234567890, False),
        ("123456789O", False),
    ],
)
def test_company_is_nip_valid_cases(nip, expected):
    company = CompanyAccount("Test Company", "1234567890")
    assert company.is_nip_valid(nip) is expected


@pytest.mark.parametrize(
    "pesels, search_pesel, expected_found, expected_count",
    [
        (["11111111111"], "11111111111", True, 1),
        (["11111111111", "22222222222"], "33333333333", False, 2),
        ([], "11111111111", False, 0),
        (["11111111111", "22222222222", "33333333333"], "22222222222", True, 3),
        (["11111111111"], None, False, 1),
        (["11111111111"], "", False, 1),
    ],
)
def test_registry_find_and_count_cases(pesels, search_pesel, expected_found, expected_count):
    registry = AccountsRegistry()
    for idx, pesel in enumerate(pesels):
        registry.add_account(Account(f"Name{idx}", f"Surname{idx}", pesel))
    found = registry.find_by_pesel(search_pesel)
    assert (found is not None) is expected_found
    assert registry.count() == expected_count
