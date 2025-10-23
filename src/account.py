class Account:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0.0
        self.promo_code = promo_code
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
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

    def apply_promo_code(self, promo_code):
        if self.is_promocode_valid(promo_code):
            self.balance += 50.0
            return True
        return False
