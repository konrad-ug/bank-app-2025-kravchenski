from src.account import Account


class TestAccountTransfers:
    def make_account(self, balance=0.0):
        acc = Account("Jan", "Kowalski", "12345678901")
        acc.balance = balance
        return acc

    def test_receive_transfer_positive(self):
        acc = self.make_account()
        result = acc.receive_transfer(150)
        assert result == True
        assert acc.balance == 150.0

    def test_receive_transfer_float(self):
        acc = self.make_account()
        result = acc.receive_transfer(19.75)
        assert result == True
        assert acc.balance == 19.75

    def test_receive_transfer_zero(self):
        acc = self.make_account()
        result = acc.receive_transfer(0)
        assert result == False
        assert acc.balance == 0.0

    def test_receive_transfer_negative(self):
        acc = self.make_account()
        result = acc.receive_transfer(-10)
        assert result == False
        assert acc.balance == 0.0

    def test_receive_transfer_wrong_type(self):
        acc = self.make_account()
        result = acc.receive_transfer("100")
        assert result == False
        assert acc.balance == 0.0

    def test_send_transfer_success(self):
        acc = self.make_account(200)
        result = acc.send_transfer(120)
        assert result == True
        assert acc.balance == 80.0

    def test_send_transfer_exact_balance(self):
        acc = self.make_account(75.5)
        result = acc.send_transfer(65.2)
        assert result == True
        assert round(acc.balance, 9) == 10.3

    def test_send_transfer_insufficient_funds(self):
        acc = self.make_account(50)
        result = acc.send_transfer(60)
        assert result == False
        assert acc.balance == 50.0

    def test_send_transfer_invalid_amount(self):
        acc = self.make_account(100)
        assert acc.send_transfer(0) == False
        assert acc.send_transfer(-5) == False
        assert acc.balance == 100.0

    def test_send_transfer_wrong_type(self):
        acc = self.make_account(100)
        result = acc.send_transfer("25")
        assert result == False
        assert acc.balance == 100.0
