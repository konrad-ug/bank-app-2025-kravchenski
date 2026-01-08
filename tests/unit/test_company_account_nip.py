import pytest
from src.company_account import CompanyAccount
import requests


def test_valid_nip_with_czynny_status(monkeypatch):
    class DummyResponse:
        status_code = 200
        text = '{"result": {"subject": {"statusVat": "Czynny"}}}'
        def json(self):
            return {"result": {"subject": {"statusVat": "Czynny"}}}
    monkeypatch.setattr(requests, "get", lambda url: DummyResponse())
    acc = CompanyAccount("Test Sp. z o.o.", "8461627563")
    assert acc.nip == "8461627563"
    assert acc.company_name == "Test Sp. z o.o."


def test_invalid_nip_not_found_raises_error(monkeypatch):
    class DummyResponse:
        status_code = 200
        text = '{"result": {"subject": null}}'
        def json(self):
            return {"result": {"subject": None}}
    monkeypatch.setattr(requests, "get", lambda url: DummyResponse())
    monkeypatch.delenv("BANK_APP_SKIP_MF_CHECK", raising=False)
    with pytest.raises(ValueError, match="Company not registered!!"):
        CompanyAccount("Test Sp. z o.o.", "1234567890")


def test_nip_with_non_czynny_status_raises_error(monkeypatch):
    class DummyResponse:
        status_code = 200
        text = '{"result": {"subject": {"statusVat": "Zwolniony"}}}'
        def json(self):
            return {"result": {"subject": {"statusVat": "Zwolniony"}}}
    monkeypatch.setattr(requests, "get", lambda url: DummyResponse())
    monkeypatch.delenv("BANK_APP_SKIP_MF_CHECK", raising=False)
    with pytest.raises(ValueError, match="Company not registered!!"):
        CompanyAccount("Test Sp. z o.o.", "1234567891")


def test_nip_too_short_no_api_call(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url: pytest.fail("Should not call API"))
    acc = CompanyAccount("Test Sp. z o.o.", "12345")
    assert acc.nip == "Invalid"


def test_nip_too_long_no_api_call(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url: pytest.fail("Should not call API"))
    acc = CompanyAccount("Test Sp. z o.o.", "12345678901234")
    assert acc.nip == "Invalid"


def test_nip_with_letters_no_api_call(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url: pytest.fail("Should not call API"))
    acc = CompanyAccount("Test Sp. z o.o.", "123ABC7890")
    assert acc.nip == "Invalid"


def test_skip_mf_check_env_variable_set_to_1(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url: pytest.fail("Should not call API"))
    monkeypatch.setenv("BANK_APP_SKIP_MF_CHECK", "1")
    acc = CompanyAccount("Test Sp. z o.o.", "1234567890")
    assert acc.nip == "1234567890"


def test_skip_mf_check_env_variable_set_to_true(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url: pytest.fail("Should not call API"))
    monkeypatch.setenv("BANK_APP_SKIP_MF_CHECK", "true")
    acc = CompanyAccount("Test Sp. z o.o.", "1234567890")
    assert acc.nip == "1234567890"


def test_skip_mf_check_env_variable_set_to_yes(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url: pytest.fail("Should not call API"))
    monkeypatch.setenv("BANK_APP_SKIP_MF_CHECK", "yes")
    acc = CompanyAccount("Test Sp. z o.o.", "1234567890")
    assert acc.nip == "1234567890"


def test_api_returns_non_200_status(monkeypatch):
    class DummyResponse:
        status_code = 500
        text = '{"error": "Internal server error"}'
        def json(self):
            return {"error": "Internal server error"}
    monkeypatch.setattr(requests, "get", lambda url: DummyResponse())
    monkeypatch.delenv("BANK_APP_SKIP_MF_CHECK", raising=False)
    with pytest.raises(ValueError, match="Company not registered!!"):
        CompanyAccount("Test Sp. z o.o.", "1234567892")


def test_api_request_exception_handling(monkeypatch):
    def raise_exception(url):
        raise Exception("Network error")
    monkeypatch.setattr(requests, "get", raise_exception)
    monkeypatch.delenv("BANK_APP_SKIP_MF_CHECK", raising=False)
    with pytest.raises(ValueError, match="Company not registered!!"):
        CompanyAccount("Test Sp. z o.o.", "1234567893")


def test_custom_mf_url_env_variable(monkeypatch):
    call_count = {"count": 0}
    
    def mock_get(url):
        call_count["count"] += 1
        assert url.startswith("https://custom-api.example.com")
        class DummyResponse:
            status_code = 200
            text = '{"result": {"subject": {"statusVat": "Czynny"}}}'
            def json(self):
                return {"result": {"subject": {"statusVat": "Czynny"}}}
        return DummyResponse()
    
    monkeypatch.setattr(requests, "get", mock_get)
    monkeypatch.delenv("BANK_APP_SKIP_MF_CHECK", raising=False)
    monkeypatch.setenv("BANK_APP_MF_URL", "https://custom-api.example.com/")
    acc = CompanyAccount("Test Sp. z o.o.", "1234567890")
    assert acc.nip == "1234567890"
    assert call_count["count"] == 1


def test_verify_nip_vat_status_method_returns_true(monkeypatch):
    class DummyResponse:
        status_code = 200
        text = '{"result": {"subject": {"statusVat": "Czynny"}}}'
        def json(self):
            return {"result": {"subject": {"statusVat": "Czynny"}}}
    monkeypatch.setattr(requests, "get", lambda url: DummyResponse())
    monkeypatch.setenv("BANK_APP_SKIP_MF_CHECK", "1")
    acc = CompanyAccount("Test Sp. z o.o.", "1234567890")
    monkeypatch.setenv("BANK_APP_SKIP_MF_CHECK", "0")
    result = acc.verify_nip_vat_status("8461627563")
    assert result == True


def test_verify_nip_vat_status_method_returns_false_for_null(monkeypatch):
    class DummyResponse:
        status_code = 200
        text = '{"result": {"subject": null}}'
        def json(self):
            return {"result": {"subject": None}}
    monkeypatch.setattr(requests, "get", lambda url: DummyResponse())
    monkeypatch.setenv("BANK_APP_SKIP_MF_CHECK", "1")
    acc = CompanyAccount("Test Sp. z o.o.", "1234567890")
    result = acc.verify_nip_vat_status("9999999999")
    assert result == False


def test_nip_none_value_no_api_call(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url: pytest.fail("Should not call API"))
    acc = CompanyAccount("Test Sp. z o.o.", None)
    assert acc.nip == "Invalid"
