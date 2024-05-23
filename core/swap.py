from core.wallet import Wallet

class Swap:
    def __init__(self, wallet=None, token_name=None, token_amount=None, sol_amount=None):
        self._wallet = wallet
        self._token_name = token_name
        self._token_amount = token_amount
        self._sol_amount = sol_amount

    @property
    def wallet(self):
        return self._wallet

    @wallet.setter
    def wallet(self, value):
        if not isinstance(value, Wallet):
            raise ValueError("Invalid wallet type provided")
        self._wallet = value

    @property
    def token_name(self):
        return self._token_name

    @token_name.setter
    def token_name(self, value):
        if not isinstance(value, str):
            raise ValueError("Token name must be a string")
        self._token_name = value

    @property
    def token_amount(self):
        return self._token_amount

    @token_amount.setter
    def token_amount(self, value):
        if value < 0:
            raise ValueError("Token amount cannot be negative")
        self._token_amount = value

    @property
    def sol_amount(self):
        return self._sol_amount

    @sol_amount.setter
    def sol_amount(self, value):
        if value < 0:
            raise ValueError("SOL amount cannot be negative")
        self._sol_amount = value
