from src.account import Account


class TestSubmitForLoan:
    
    def test_loan_denied_empty_history(self):
        account = Account("John", "Doe", "12345678901")
        result = account.submit_for_loan(1000.0)
        assert result == False
        assert account.balance == 0.0
    
    def test_loan_denied_one_transaction(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(500.0)
        result = account.submit_for_loan(1000.0)
        assert result == False
        assert account.balance == 500.0
    
    def test_loan_approved_last_three_are_deposits(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        account.receive_transfer(200.0)
        account.receive_transfer(300.0)
        result = account.submit_for_loan(500.0)
        assert result == True
        assert account.balance == 1100.0
    
    def test_loan_denied_last_three_not_all_deposits(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        account.receive_transfer(200.0)
        account.receive_transfer(300.0)
        account.send_transfer(50.0)
        result = account.submit_for_loan(500.0)
        assert result == False
        assert account.balance == 550.0
    def test_loan_approved_sum_of_five_transactions_greater(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        account.receive_transfer(200.0)
        account.receive_transfer(300.0)
        account.send_transfer(50.0)
        account.receive_transfer(150.0)
        result = account.submit_for_loan(699.0)
        assert result == True
        assert account.balance == 1399.0
    
    def test_loan_denied_sum_of_five_transactions_less(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        account.receive_transfer(200.0)
        account.receive_transfer(300.0)
        account.send_transfer(50.0)
        account.receive_transfer(150.0)
        result = account.submit_for_loan(800.0)
        assert result == False
        assert account.balance == 700.0
    
    def test_loan_denied_sum_of_five_transactions_equal(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        account.receive_transfer(200.0)
        account.receive_transfer(300.0)
        account.send_transfer(50.0)
        account.receive_transfer(150.0)
        result = account.submit_for_loan(700.0)
        assert result == False
        assert account.balance == 700.0

    def test_loan_approved_last_three_deposits_with_express_fee(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(500.0)
        account.send_express_transfer(100.0)
        account.receive_transfer(300.0)
        account.receive_transfer(200.0)
        account.receive_transfer(100.0)
        result = account.submit_for_loan(500.0)
        assert result == True
        assert account.balance == 1499.0
    
    def test_loan_denied_last_three_not_all_deposits_with_express(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(500.0)
        account.receive_transfer(300.0)
        account.send_express_transfer(100.0)
        result = account.submit_for_loan(1000.0)
        assert result == False
        assert account.balance == 699.0
    
    def test_loan_four_transactions_last_three_deposits(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(50.0)
        account.receive_transfer(100.0)
        account.receive_transfer(200.0)
        account.receive_transfer(300.0)
        result = account.submit_for_loan(500.0)
        assert result == True
        assert account.balance == 1150.0
    
    def test_loan_exactly_five_transactions_sum_greater_than_amount(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        account.receive_transfer(200.0)
        account.receive_transfer(300.0)
        account.send_transfer(50.0)
        account.receive_transfer(150.0)
        result = account.submit_for_loan(699.0)
        assert result == True
        assert account.balance == 1399.0
    
    def test_loan_more_than_five_transactions_uses_last_five(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(50.0)
        account.receive_transfer(100.0)
        account.receive_transfer(200.0)
        account.receive_transfer(300.0)
        account.send_transfer(50.0)
        account.receive_transfer(150.0)
        result = account.submit_for_loan(699.0)
        assert result == True
        assert account.balance == 1449.0
    
    def test_loan_denied_negative_amount(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        account.receive_transfer(200.0)
        account.receive_transfer(300.0)
        result = account.submit_for_loan(-500.0)
        assert result == False
        assert account.balance == 600.0
    
    def test_loan_denied_zero_amount(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(100.0)
        account.receive_transfer(200.0)
        account.receive_transfer(300.0)
        result = account.submit_for_loan(0)
        assert result == False
        assert account.balance == 600.0
    def test_loan_last_three_include_express_fee(self):
        account = Account("John", "Doe", "12345678901")
        account.receive_transfer(1000.0)
        account.send_express_transfer(100.0)
        account.receive_transfer(200.0)
        account.receive_transfer(300.0)
        account.receive_transfer(400.0)
        result = account.submit_for_loan(100.0)
        assert result == True
        assert account.balance == 1899.0


class TestCompanyAccountLoan:
    
    def test_company_account_cannot_submit_for_loan(self):
        from src.company_account import CompanyAccount
        account = CompanyAccount("Tech Corp", "1234567890")
        account.receive_transfer(1000.0)
        account.receive_transfer(1000.0)
        account.receive_transfer(1000.0)
        result = account.submit_for_loan(500.0)
        assert result == False
        assert account.balance == 3000.0
