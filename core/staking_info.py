from datetime import datetime

class StakingInfo:
    def __init__(self, wallet_address=None, amount=None, start_time=None):
        self._wallet_address = wallet_address
        self._amount = amount
        self._start_time = start_time if start_time is not None else datetime.now()

    @property
    def wallet_address(self):
        return self._wallet_address

    @wallet_address.setter
    def wallet_address(self, value):
        self._wallet_address = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    def __str__(self):
        return f"Staking Info: Wallet Address: {self._wallet_address}, Amount: {self._amount}, Start Time: {self._start_time.strftime('%Y-%m-%d %H:%M:%S')}"