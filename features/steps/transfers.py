from behave import *
import requests

URL = "http://localhost:5000"

@when('I send transfer of amount "{amount}" to account with pesel: "{pesel}"')
def send_transfer_to_account(context, amount, pesel):
    json_body = {"amount": float(amount)}
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    context.last_transfer_response = response

@then('Account with pesel "{pesel}" has balance equal to "{balance}"')
def check_account_balance(context, pesel, balance):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    account = response.json()
    assert float(account["balance"]) == float(balance), f"Expected balance {balance}, but got {account['balance']}"

@then('Transfer to account with pesel "{pesel}" is rejected')
def check_transfer_rejected(context, pesel):
    assert hasattr(context, 'last_transfer_response'), "No transfer was attempted"
    assert context.last_transfer_response.status_code == 400, f"Expected status 400, but got {context.last_transfer_response.status_code}"

@then('Transfer to account with pesel "{pesel}" fails with not found error')
def check_transfer_not_found(context, pesel):
    assert hasattr(context, 'last_transfer_response'), "No transfer was attempted"
    assert context.last_transfer_response.status_code == 404, f"Expected status 404, but got {context.last_transfer_response.status_code}"
