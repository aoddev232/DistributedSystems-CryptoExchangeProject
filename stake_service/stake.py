from datetime import datetime, timedelta
import math
from core.mongo import MongoDB
from core.wallet import Wallet
from core.staking_info import StakingInfo

class Stake:
    interest_rate = 1.001  # 1% interest

    def stake_sol(self, wallet_address, amount):
        wallet = MongoDB.get_wallet_from_db(wallet_address)
        if float(wallet.sol_balance) < amount:
            print("Error! Insufficient sol balance!")
            return

        staked = MongoDB.get_staking_info_from_db(wallet.wallet_address)
        print(staked)
        if staked is None:
            print("Staking for the first time.")
            staked = StakingInfo(wallet.wallet_address, amount, datetime.now())
        else:
            updated_amount = self.get_staked_amount(wallet.wallet_address)
            staked.amount = updated_amount + amount
            staked.start_time = datetime.now()  # Reset the start time
        MongoDB.add_staking_info_to_db(staked)
        wallet.subtract_sol_balance(amount)
        MongoDB.add_wallet_to_db(wallet)
        return "Stake successful."

    @staticmethod
    def get_staked_amount(wallet_address):
        staked = MongoDB.get_staking_info_from_db(wallet_address)
        print(staked)
        if staked is None:
            return 0.0

        current_time = datetime.now()
        time_elapsed_in_seconds = (current_time - staked.start_time).total_seconds()
        intervals = float(time_elapsed_in_seconds / 600)
        total = staked.amount * math.pow(Stake.interest_rate, intervals)
        float_total = float(total)
        print(float_total)
        return float_total

    def unstake_sol(self, wallet_address, amount):
        wallet = MongoDB.get_wallet_from_db(wallet_address)
        staked = MongoDB.get_staking_info_from_db(wallet_address)
        if staked is None:
            print("Error! No staked sol to unstake.")
            return

        if amount > self.get_staked_amount(wallet.wallet_address):
            print("Error! Unstaking amount is more than staked.")
            return

        new_staked_amount = self.get_staked_amount(wallet.wallet_address) - amount
        staked.amount = new_staked_amount
        MongoDB.add_staking_info_to_db(staked)
        wallet.add_sol_balance(amount)
        MongoDB.add_wallet_to_db(wallet)