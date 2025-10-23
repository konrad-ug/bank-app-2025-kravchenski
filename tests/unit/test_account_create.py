from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678901"

    def test_pesel_too_short(self):
        account = Account("John", "Doe", "12345")
        assert account.pesel == "Invalid"

    def test_pesel_too_long(self):
        account = Account("John", "Doe", "2342342341532525235235")
        assert account.pesel == "Invalid"

    def test_pesel_no_digit(self):
        account = Account("John", "Doe", None)
        assert account.pesel == "Invalid"

    def test_apply_valid_promo_code_to_account_without_initial_promo(self):
        account = Account("John", "Doe", "12345678901")
        initial_balance = account.balance

        result = account.apply_promo_code("PROM_XYZ")

        assert result == True
        assert account.balance == initial_balance + 50.0

    def test_apply_invalid_promo_code(self):
        account = Account("John", "Doe", "12345678901")
        initial_balance = account.balance
        result = account.apply_promo_code("INVALID_CODE")

        assert result == False
        assert account.balance == initial_balance

    def test_apply_promo_code_multiple_times(self):
        account = Account("John", "Doe", "12345678901")

        result1 = account.apply_promo_code("PROM_ABC")
        assert result1 == True
        assert account.balance == 50.0

        result2 = account.apply_promo_code("PROM_123")
        assert result2 == True
        assert account.balance == 100.0

        result3 = account.apply_promo_code("WRONG_CODE")
        assert result3 == False
        assert account.balance == 100.0
