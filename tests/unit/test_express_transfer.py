from src.account import Account
from src.company_account import CompanyAccount


class TestExpressTransferPersonalAccount:
    
    def test_express_transfer_with_sufficient_balance(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        result = account.send_express_transfer(50.0)
        assert result == True
        assert account.balance == 49.0
    
    def test_express_transfer_fee_is_1_pln(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        account.send_express_transfer(50.0)
        assert account.balance == 49.0
    
    def test_express_transfer_balance_can_go_negative_by_fee(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(10.0)
        result = account.send_express_transfer(10.0)
        assert result == True
        assert account.balance == -1.0
    
    def test_express_transfer_fails_when_balance_too_low(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(5.0)
        result = account.send_express_transfer(10.0)
        assert result == False
        assert account.balance == 5.0
    
    def test_express_transfer_with_zero_balance(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(1.0)
        result = account.send_express_transfer(1.0)
        assert result == True
        assert account.balance == -1.0
    
    def test_express_transfer_invalid_amount_negative(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        result = account.send_express_transfer(-10.0)
        assert result == False
        assert account.balance == 100.0
    
    def test_express_transfer_invalid_amount_zero(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        result = account.send_express_transfer(0)
        assert result == False
        assert account.balance == 100.0


class TestExpressTransferCompanyAccount:
    def test_express_transfer_with_sufficient_balance(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.receive_transfer(100.0)
        result = account.send_express_transfer(50.0)
        assert result == True
        assert account.balance == 45.0
    
    def test_express_transfer_fee_is_5_pln(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.receive_transfer(100.0)
        account.send_express_transfer(50.0)
        assert account.balance == 45.0
    
    def test_express_transfer_balance_can_go_negative_by_fee(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.receive_transfer(10.0)
        result = account.send_express_transfer(10.0)
        assert result == True
        assert account.balance == -5.0
    
    def test_express_transfer_fails_when_balance_too_low(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.receive_transfer(3.0)
        result = account.send_express_transfer(10.0)
        assert result == False
        assert account.balance == 3.0
    
    def test_express_transfer_with_zero_balance(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.receive_transfer(5.0)
        result = account.send_express_transfer(5.0)
        assert result == True
        assert account.balance == -5.0
    
    def test_express_transfer_invalid_amount_negative(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.receive_transfer(100.0)
        result = account.send_express_transfer(-10.0)
        assert result == False
        assert account.balance == 100.0
    
    def test_express_transfer_invalid_amount_zero(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.receive_transfer(100.0)
        result = account.send_express_transfer(0)
        assert result == False
        assert account.balance == 100.0
