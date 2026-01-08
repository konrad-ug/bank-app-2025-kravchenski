from flask import Flask, request, jsonify, abort
from src.accounts_registry import AccountsRegistry
from src.account import Account

app = Flask(__name__)
registry = AccountsRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "surname", "pesel")):
        return jsonify({"error": "Missing data"}), 400
    if registry.find_by_pesel(data["pesel"]):
        return jsonify({"error": "Account with this pesel already exists"}), 409
    account = Account(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.get_all_accounts()
    accounts_data = [{
        "name": acc.first_name,
        "surname": acc.last_name,
        "pesel": acc.pesel,
        "balance": acc.balance
    } for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    return jsonify({"count": registry.count()}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    acc = registry.find_by_pesel(pesel)
    if not acc:
        abort(404)
    return jsonify({
        "name": acc.first_name,
        "surname": acc.last_name,
        "pesel": acc.pesel,
        "balance": acc.balance
    }), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    acc = registry.find_by_pesel(pesel)
    if not acc:
        abort(404)
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    if "name" in data:
        acc.first_name = data["name"]
    if "surname" in data:
        acc.last_name = data["surname"]
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    acc = registry.find_by_pesel(pesel)
    if not acc:
        abort(404)
    registry._accounts.remove(acc)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def receive_transfer(pesel):
    acc = registry.find_by_pesel(pesel)
    if not acc:
        abort(404)
    data = request.get_json()
    if not data or "amount" not in data:
        return jsonify({"error": "Missing amount"}), 400
    amount = data["amount"]
    if acc.receive_transfer(amount):
        return jsonify({"message": "Transfer received", "balance": acc.balance}), 200
    return jsonify({"error": "Invalid transfer"}), 400

if __name__ == "__main__":
    app.run(debug=True)
