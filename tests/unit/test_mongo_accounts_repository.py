from unittest.mock import Mock

from src.account import Account
from src.mongo_accounts_repository import MongoAccountsRepository


def test_save_all_clears_and_upserts_accounts():
    account1 = Account("Jan", "Kowalski", "12345678901")
    account1.receive_transfer(100)
    account2 = Account("Anna", "Nowak", "98765432109")
    account2.receive_transfer(50)

    mock_collection = Mock()
    repo = MongoAccountsRepository(collection=mock_collection)

    repo.save_all([account1, account2])

    mock_collection.delete_many.assert_called_once_with({})
    assert mock_collection.update_one.call_count == 2

    first_call = mock_collection.update_one.call_args_list[0]
    assert first_call.args == ({"pesel": account1.pesel}, {"$set": account1.to_dict()})
    assert first_call.kwargs == {"upsert": True}

    second_call = mock_collection.update_one.call_args_list[1]
    assert second_call.args == ({"pesel": account2.pesel}, {"$set": account2.to_dict()})
    assert second_call.kwargs == {"upsert": True}


def test_load_all_returns_accounts_from_collection():
    account1 = Account("Jan", "Kowalski", "12345678901")
    account1.receive_transfer(100)
    account2 = Account("Anna", "Nowak", "98765432109")
    account2.receive_transfer(50)

    mock_collection = Mock()
    mock_collection.find.return_value = [
        {"_id": "mongo1", **account1.to_dict()},
        {"_id": "mongo2", **account2.to_dict()},
    ]
    repo = MongoAccountsRepository(collection=mock_collection)

    accounts = repo.load_all()

    assert len(accounts) == 2
    assert accounts[0].pesel == account1.pesel
    assert accounts[0].balance == account1.balance
    assert accounts[0].history == account1.history
    assert accounts[1].pesel == account2.pesel
    assert accounts[1].balance == account2.balance
    assert accounts[1].history == account2.history
