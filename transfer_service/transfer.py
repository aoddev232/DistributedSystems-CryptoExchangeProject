from pymongo import MongoClient
from core.wallet import Wallet
from core.mongo import MongoDB

class TransferService:
    def transfer_money(self, sender_wallet, receiver_wallet, amount):
        if sender_wallet is None or receiver_wallet is None:
            raise ValueError("Sender or receiver wallet not found.")

        if amount < 0:
            raise ValueError("Transfer amount must be positive.")

        sender_balance = sender_wallet.sol_balance
        if int(sender_balance) < amount:
            raise ValueError("Insufficient balance in sender's wallet.")
        
        # Perform the transfer
        sender_wallet.subtract_sol_balance(amount)
        receiver_wallet.add_sol_balance(amount)

        # Persist changes to the database
        MongoDB.add_wallet_to_db(sender_wallet)
        MongoDB.add_wallet_to_db(receiver_wallet)

        return "Transfer successful."
