import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from src.account import Account
from src.company_account import CompanyAccount
from smtp.smtp import SMTPClient


class TestPersonalAccountEmailHistory:
    
    def test_send_email_called_with_correct_parameters(self, monkeypatch):
        account = Account("John", "Doe", "12345678901", None)
        account.receive_transfer(100)
        account.send_transfer(1)
        account.receive_transfer(500)
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=True)
        
        with patch('src.account.SMTPClient', return_value=mock_smtp):
            with patch('src.account.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "2025-12-10"
                result = account.send_history_via_email("test@example.com")
        
        mock_smtp.send.assert_called_once()
        
        call_args = mock_smtp.send.call_args
        subject = call_args[0][0]
        text = call_args[0][1]
        email = call_args[0][2]
        
        assert subject == "Account Transfer History 2025-12-10"
        assert text == "Personal account history: [100.0, -1.0, 500.0]"
        assert email == "test@example.com"
        assert result == True
    
    def test_send_email_returns_true_on_success(self, monkeypatch):
        account = Account("Jane", "Smith", "98765432109", None)
        account.history = [100, -50, 200]
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=True)
        
        with patch('src.account.SMTPClient', return_value=mock_smtp):
            result = account.send_history_via_email("success@example.com")
        
        assert result == True
        mock_smtp.send.assert_called_once()
    
    def test_send_email_returns_false_on_failure(self, monkeypatch):
        account = Account("Bob", "Johnson", "11223344556", None)
        account.history = [1000, -200]
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=False)
        
        with patch('src.account.SMTPClient', return_value=mock_smtp):
            result = account.send_history_via_email("failure@example.com")
        
        assert result == False
        mock_smtp.send.assert_called_once()
    
    def test_send_email_with_empty_history(self, monkeypatch):
        account = Account("Alice", "Brown", "55667788990", None)
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=True)
        with patch('src.account.SMTPClient', return_value=mock_smtp):
            with patch('src.account.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "2025-12-10"
                
                result = account.send_history_via_email("empty@example.com")
        
        call_args = mock_smtp.send.call_args
        text = call_args[0][1]
        
        assert text == "Personal account history: []"
        assert result == True
    
    def test_send_email_with_complex_history(self, monkeypatch):
        account = Account("Charlie", "Davis", "12312312312", None)
        account.receive_transfer(5000)
        account.send_transfer(1000)
        account.receive_transfer(2500)
        account.send_express_transfer(500)
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=True)
        
        with patch('src.account.SMTPClient', return_value=mock_smtp):
            result = account.send_history_via_email("complex@example.com")
        
        call_args = mock_smtp.send.call_args
        text = call_args[0][1]
        
        assert "5000.0" in text
        assert "-1000.0" in text
        assert "2500.0" in text
        assert "-500.0" in text
        assert "-1.0" in text
        assert result == True


class TestCompanyAccountEmailHistory:
    
    def test_company_send_email_called_with_correct_parameters(self, monkeypatch):
        monkeypatch.setenv("BANK_APP_SKIP_MF_CHECK", "1")
        
        account = CompanyAccount("Test Company Sp. z o.o.", "1234567890")
        account.receive_transfer(5000)
        account.send_transfer(1000)
        account.receive_transfer(500)
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=True)
        
        with patch('src.company_account.SMTPClient', return_value=mock_smtp):
            with patch('src.company_account.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "2025-12-10"
                
                result = account.send_history_via_email("company@example.com")
        
        mock_smtp.send.assert_called_once()
        
        call_args = mock_smtp.send.call_args
        subject = call_args[0][0]
        text = call_args[0][1]
        email = call_args[0][2]
        
        assert subject == "Account Transfer History 2025-12-10"
        assert text == "Company account history: [5000.0, -1000.0, 500.0]"
        assert email == "company@example.com"
        assert result == True
    
    def test_company_send_email_returns_true_on_success(self, monkeypatch):
        monkeypatch.setenv("BANK_APP_SKIP_MF_CHECK", "1")
        
        account = CompanyAccount("Success Corp", "9876543210")
        account.history = [10000, -2000, 5000]
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=True)
        
        with patch('src.company_account.SMTPClient', return_value=mock_smtp):
            result = account.send_history_via_email("success@company.com")
        assert result == True
        mock_smtp.send.assert_called_once()
    
    def test_company_send_email_returns_false_on_failure(self, monkeypatch):
        monkeypatch.setenv("BANK_APP_SKIP_MF_CHECK", "1")
        
        account = CompanyAccount("Failure LLC", "1122334455")
        account.history = [20000, -5000]
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=False)
        
        with patch('src.company_account.SMTPClient', return_value=mock_smtp):
            result = account.send_history_via_email("failure@company.com")
        
        assert result == False
        mock_smtp.send.assert_called_once()
    
    def test_company_send_email_with_empty_history(self, monkeypatch):
        monkeypatch.setenv("BANK_APP_SKIP_MF_CHECK", "1")
        
        account = CompanyAccount("Empty History Inc", "5566778899")
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=True)
        
        with patch('src.company_account.SMTPClient', return_value=mock_smtp):
            with patch('src.company_account.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "2025-12-10"
                
                result = account.send_history_via_email("empty@company.com")
        
        call_args = mock_smtp.send.call_args
        text = call_args[0][1]
        assert text == "Company account history: []"
        assert result == True
    
    def test_company_send_email_with_express_transfers(self, monkeypatch):
        monkeypatch.setenv("BANK_APP_SKIP_MF_CHECK", "1")
        
        account = CompanyAccount("Express Co", "9988776655")
        account.receive_transfer(50000)
        account.send_express_transfer(10000)
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=True)
        
        with patch('src.company_account.SMTPClient', return_value=mock_smtp):
            result = account.send_history_via_email("express@company.com")
        
        call_args = mock_smtp.send.call_args
        text = call_args[0][1]
        
        assert "50000.0" in text
        assert "-10000.0" in text
        assert "-5.0" in text
        assert result == True
    
    def test_company_account_creation_with_valid_nip_mock(self, monkeypatch):
        class DummyResponse:
            status_code = 200
            text = '{"result": {"subject": {"statusVat": "Czynny"}}}'
            def json(self):
                return {"result": {"subject": {"statusVat": "Czynny"}}}
        
        import requests
        monkeypatch.setattr(requests, "get", lambda url: DummyResponse())
        monkeypatch.delenv("BANK_APP_SKIP_MF_CHECK", raising=False)
        
        account = CompanyAccount("Valid NIP Company", "8461627563")
        account.receive_transfer(1000)
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=True)
        
        with patch('src.company_account.SMTPClient', return_value=mock_smtp):
            result = account.send_history_via_email("valid@nip.com")
        
        assert result == True
        mock_smtp.send.assert_called_once()
        call_args = mock_smtp.send.call_args
        text = call_args[0][1]
        assert "1000.0" in text


class TestEmailHistoryDateFormat:
    
    def test_date_format_is_correct(self, monkeypatch):
        monkeypatch.setenv("BANK_APP_SKIP_MF_CHECK", "1")
        
        account = Account("Test", "User", "12345678901", None)
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=True)
        
        with patch('src.account.SMTPClient', return_value=mock_smtp):
            with patch('src.account.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "2025-12-13"
                
                account.send_history_via_email("date@test.com")
        call_args = mock_smtp.send.call_args
        subject = call_args[0][0]
        
        assert subject == "Account Transfer History 2025-12-13"
    
    def test_different_date_format(self, monkeypatch):
        account = Account("Another", "User", "98765432109", None)
        
        mock_smtp = Mock(spec=SMTPClient)
        mock_smtp.send = Mock(return_value=True)
        
        with patch('src.account.SMTPClient', return_value=mock_smtp):
            with patch('src.account.datetime') as mock_datetime:
                mock_datetime.now.return_value.strftime.return_value = "2026-01-08"
                
                account.send_history_via_email("another@test.com")
        
        call_args = mock_smtp.send.call_args
        subject = call_args[0][0]
        
        assert subject == "Account Transfer History 2026-01-08"
