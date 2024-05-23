from datetime import datetime

class SwapQuotation:
    def __init__(self, wallet_address=None, reference=None, token_name=None, token_amount=None, sol_amount=None, swap_occurred=None, timestamp=None):
        self._wallet_address = wallet_address
        self._reference = reference
        self._token_name = token_name
        self._token_amount = token_amount
        self._sol_amount = sol_amount
        self._swap_occurred = swap_occurred
        self._timestamp = timestamp if timestamp is not None else datetime.now()

    @property
    def wallet_address(self):
        return self._wallet_address

    @wallet_address.setter
    def wallet_address(self, value):
        if not isinstance(value, str):
            raise ValueError("Invalid wallet address format")
        self._wallet_address = value

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, value):
        if not isinstance(value, str):
            raise ValueError("Reference must be a string")
        self._reference = value

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

    @property
    def swap_occurred(self):
        return self._swap_occurred

    @swap_occurred.setter
    def swap_occurred(self, value):
        if not isinstance(value, bool):
            raise ValueError("Swap occurred must be a boolean")
        self._swap_occurred = value

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        if not isinstance(value, datetime):
            raise ValueError("Invalid timestamp")
        self._timestamp = value
