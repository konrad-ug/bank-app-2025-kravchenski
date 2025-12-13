import pytest
import os

@pytest.fixture(scope="session", autouse=True)
def set_skip_mf_check():
    os.environ["BANK_APP_SKIP_MF_CHECK"] = "1"
    yield
    if "BANK_APP_SKIP_MF_CHECK" in os.environ:
        del os.environ["BANK_APP_SKIP_MF_CHECK"]
