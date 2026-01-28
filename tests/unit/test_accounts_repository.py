import pytest
from src.accounts_repository import AccountsRepository


class ConcreteRepository(AccountsRepository):
    def save_all(self, accounts):
        return super().save_all(accounts)

    def load_all(self):
        return super().load_all()


def test_save_all_not_implemented():
    repo = ConcreteRepository()
    with pytest.raises(NotImplementedError):
        repo.save_all([])


def test_load_all_not_implemented():
    repo = ConcreteRepository()
    with pytest.raises(NotImplementedError):
        repo.load_all()
