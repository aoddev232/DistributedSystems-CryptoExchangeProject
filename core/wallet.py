class Wallet:
    def __init__(self, wallet_address=None, wallet_tag=None, password=None, sol=None, tokens=None):
        self._wallet_address = wallet_address
        self._wallet_tag = wallet_tag
        self._password = password
        self._sol = sol
        self._tokens = tokens if tokens is not None else {}

    @property
    def wallet_address(self):
        return self._wallet_address

    @property
    def wallet_tag(self):
        return self._wallet_tag

    @wallet_tag.setter
    def wallet_tag(self, value):
        if isinstance(value, str):
            self._wallet_tag = value
        else:
            raise ValueError("Wallet tag must be a string")

    @property
    def sol_balance(self):
        return self._sol

    @property
    def password(self):
        return self._password

    def get_token_balance(self, token):
        return self._tokens.get(token, 0)

    @property
    def token_balances(self):
        return self._tokens

    def add_sol_balance(self, amount):
        balance = float(self._sol)
        amount = float(amount)
        if amount < 0:
            raise ValueError("Cannot add a negative amount")
        self._sol = (balance + amount)

    def subtract_sol_balance(self, amount):
        balance = float(self._sol)
        amount = float(amount)
        if float(self._sol) < amount:
            raise ValueError("Insufficient SOL balance")
        self._sol = (balance - amount)

    def add_token_balance(self, token, amount):
        amount = float(amount)
        if amount < 0:
            raise ValueError("Cannot add a negative amount")
        self._tokens[token] = self._tokens.get(token, 0) + amount

    def subtract_token_balance(self, token, amount):
        amount = float(amount)
        current_value = float(self._tokens.get(token, 0))
        if current_value < amount:
            raise ValueError("Removing more than current balance")
        self._tokens[token] = current_value - amount

    def __str__(self):
        return f"Wallet({self._wallet_address}, Tag: {self._wallet_tag}, Sol: {self._sol}, Tokens: {self._tokens})"
