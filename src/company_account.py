import os
import requests
from datetime import datetime
from src.account import Account


class CompanyAccount(Account):
    def __init__(self, company_name, nip):
        self.company_name = company_name
        super().__init__(first_name="", last_name="", pesel=None, promo_code=None)
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        if self.is_nip_valid(nip) and os.environ.get("BANK_APP_SKIP_MF_CHECK", "").lower() not in ("1", "true", "yes"):
            mf_status = self.verify_nip_vat_status(nip)
            if mf_status is None or mf_status is False:
                raise ValueError("Company not registered!!")
    
    def is_nip_valid(self, nip):
        if isinstance(nip, str) and nip.isdigit() and len(nip) == 10:
            return True
        return False

    def verify_nip_vat_status(self, nip):
        base_url = os.environ.get("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl/")
        base_url = base_url.rstrip('/')
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"{base_url}/api/search/nip/{nip}?date={today}"
        try:
            response = requests.get(url)
            print(f"MF API response: {response.text}")
            if response.status_code == 200:
                data = response.json()
                subject = data.get("result", {}).get("subject")
                if subject and subject.get("statusVat") == "Czynny":
                    return True
                if subject is None:
                    return False
            return False
        except Exception as e:
            print(f"MF API error: {e}")
            return False

    def get_express_fee(self):
        return 5.0
    
    def submit_for_loan(self, amount):
        return False

    def take_loan(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False
        if self.balance < 2 * amount:
            return False
        if -1775 not in self.history:
            return False
        self.balance += float(amount)
        return True
