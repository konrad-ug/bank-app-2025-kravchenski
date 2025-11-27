from src.account import Account
from src.company_account import CompanyAccount


class TestAccountHistory:
    
    def test_account_has_empty_history_on_creation(self):
        account = Account("John", "Doe", "12345678901")
        assert account.history == []
    
    def test_history_records_incoming_transfer(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(500.0)
        assert account.history == [500.0]
    
    def test_history_records_outgoing_transfer(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(1000.0)
        account.send_transfer(300.0)
        assert account.history == [1000.0, -300.0]
    
    def test_history_records_multiple_transfers(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(500.0)
        account.receive_transfer(200.0)
        account.send_transfer(100.0)
        assert account.history == [500.0, 200.0, -100.0]
    
    def test_history_records_express_transfer_with_fee(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(500.0)
        account.send_express_transfer(300.0)
        assert account.history == [500.0, -300.0, -1.0]
    
    def test_history_records_only_successful_transfers(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        account.send_transfer(500.0)
        assert account.history == [100.0]
    
    def test_history_records_failed_express_transfer_not_added(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        account.send_express_transfer(500.0)
        assert account.history == [100.0]
    
    def test_history_complex_scenario(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(500.0)
        account.send_express_transfer(300.0)
        account.receive_transfer(200.0)
        account.send_transfer(100.0)
        assert account.history == [500.0, -300.0, -1.0, 200.0, -100.0]


class TestCompanyAccountHistory:
    
    def test_company_account_has_empty_history_on_creation(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        assert account.history == []
    
    def test_company_account_history_records_incoming_transfer(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.receive_transfer(1000.0)
        assert account.history == [1000.0]
    
    def test_company_account_history_records_outgoing_transfer(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.receive_transfer(1000.0)
        account.send_transfer(500.0)
        assert account.history == [1000.0, -500.0]
    
    def test_company_account_history_express_transfer_with_higher_fee(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.receive_transfer(1000.0)
        account.send_express_transfer(300.0)
        assert account.history == [1000.0, -300.0, -5.0]
    
    def test_company_account_history_multiple_operations(self):
        account = CompanyAccount("Tech Corp", "1234567890")
        account.receive_transfer(500.0)
        account.send_transfer(100.0)
        account.receive_transfer(200.0)
        account.send_express_transfer(150.0)
        assert account.history == [500.0, -100.0, 200.0, -150.0, -5.0]
