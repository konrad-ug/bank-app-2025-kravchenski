class AccountsRegistry:
    def __init__(self):
        self._accounts = []

    def add_account(self, account):
        self._accounts.append(account)

    def find_by_pesel(self, pesel):
        for acc in self._accounts:
            if hasattr(acc, 'pesel') and acc.pesel == pesel:
                return acc
        return None

    @property
    def accounts(self):
        return self._accounts.copy()

    @property
    def count(self):
        return len(self._accounts)
