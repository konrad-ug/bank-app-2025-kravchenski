from datetime import datetime
from smtp.smtp import SMTPClient

class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.promo_code = promo_code
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.history = []
        self.apply_promo_code(promo_code)

    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11:
            return True
        return False

    def is_promocode_valid(self, promo_code):
        if isinstance(promo_code, str) and promo_code.startswith("PROM_"):
            suffix = promo_code[5:]
            if len(suffix) >= 1:
                return True

        return False

    def extract_birth_year(self):
        try:
            year_part = int(self.pesel[0:2])
            month_part = int(self.pesel[2:4])
            if 1 <= month_part <= 12:
                century = 1900
            elif 21 <= month_part <= 32:
                century = 2000
            elif 41 <= month_part <= 52:
                century = 2100
            elif 61 <= month_part <= 72:
                century = 2200
            elif 81 <= month_part <= 92:
                century = 1800
            else:
                return None
            return century + year_part
        except (ValueError, TypeError):
            return None

    def apply_age_bonus(self):
        year = self.extract_birth_year()
        if year is not None and year > 1960:
            self.balance += 50.0
            return True
        return False

    def apply_promo_code(self, promo_code):
        if self.is_promocode_valid(promo_code):
            self.balance += 50.0
            return True
        return False
    
    def receive_transfer(self, amount):
        if isinstance(amount, (int, float)) and amount > 0:
            self.balance += float(amount)
            self.history.append(float(amount))
            return True
        return False

    def send_transfer(self, amount):
        if isinstance(amount, (int, float)) and 0 < amount <= self.balance:
            self.balance -= float(amount)
            self.history.append(-float(amount))
            return True
        return False
    
    def get_express_fee(self):
        return 1.0
    
    def send_express_transfer(self, amount):
        if isinstance(amount, (int, float)) and amount > 0:
            express_fee = self.get_express_fee()
            total_cost = float(amount) + express_fee
            if self.balance >= amount - express_fee:
                self.balance -= total_cost
                self.history.append(-float(amount))
                self.history.append(-express_fee)
                return True
        return False

    def submit_for_loan(self, amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False
        
        if len(self.history) < 3:
            return False
        
        last_three = self.history[-3:]
        if all(transaction > 0 for transaction in last_three):
            self.balance += float(amount)
            return True
        if len(self.history) >= 5:
            last_five = self.history[-5:]
            sum_last_five = sum(last_five)
            if sum_last_five > amount:
                self.balance += float(amount)
                return True
        
        return False

    def send_history_via_email(self, email_address):
        today = datetime.now().strftime("%Y-%m-%d")
        subject = f"Account Transfer History {today}"
        text = f"Personal account history: {self.history}"
        
        smtp_client = SMTPClient()
        return smtp_client.send(subject, text, email_address)
