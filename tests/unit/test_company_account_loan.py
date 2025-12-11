import pytest
from src.company_account import CompanyAccount

@pytest.fixture
def company_account():
    return CompanyAccount("Tech Corp", "1234567890")

@pytest.mark.parametrize(
    "balance,history,amount,expected_balance,expected_result",
    [
        (3000, [-1775], 2000, 3000, False),
        (5000, [], 2000, 5000, False),
        (5000, [-1775], 0, 5000, False),
        (5000, [-1775], -100, 5000, False),
        (5000, [-1775], 2000, 7000, True),
        (10000, [1000, -1775, -500], 4000, 14000, True),
        (8000, [-1775, -1775], 3000, 11000, True),
        (3550, [-1775, -100], 1775, 5325, True),
        (3550, [-100, -1775], 1775, 5325, True),
        (3550, [-100, -500], 1775, 3550, False),
        (4000, [-1775, -1775, -1775], 1500, 5500, True),
        (3550, [-1775], 1776, 3550, False),
        (10000, [-1775, -100, -200], 5000, 15000, True),
        (10000, [-1775, -100, -200], 4000, 14000, True),
        (10000, [-100, -200, -300], 4000, 10000, False),
        (10000, [-1775, -100, -200], 0.01, 10000.01, True),
    ]
)
def test_take_loan(company_account, balance, history, amount, expected_balance, expected_result):
    company_account.balance = balance
    company_account.history = history.copy()
    result = company_account.take_loan(amount)
    assert result == expected_result
    assert company_account.balance == expected_balance
