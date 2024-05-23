import requests
import datetime
from core.mongo import MongoDB
from core.wallet import Wallet
from core.swap_quotation import SwapQuotation
import json

class Swapper:
    def __init__(self):
        # Initialize the token URLs
        self.token_urls = {
            "TREMP" : "5o9kgvozarynwfbytzd1wdrkpkkdr6ldpqbuuqm57nfj",
            "BODEN" : "6UYbX1x8YUcFj8YstPYiZByG7uQzAq2s46ZWphUMkjg5",
            "BOME" : "DSUvc5qf5LJHHV5e2tD184ixotSnCnwj7i4jJa4Xsrmt",
            "WIF" : "CZrvf5cCAf7BoTqLkMEsT2czJobx4zfppHez2gaJwHaF",
            "TOOKER" : "3vGHsKVKNapB4hSapzKNwtiJ6DA8Ytd9SsMFSoAk154B",
            "GUMMY" : "FMiecMsYhPdBf94zZKa7i6inK1GX7aypLf7QewNz1i6w",
            "SLERF" : "AgFnRLUScRD2E4nWQxW73hdbSN7eKEUb2jHX7tx9YTYc",
            "HARAMBE" : "2BJKy9pnzTDvMPdHJhv8qbWejKiLzebD7i2taTyJxAze",
            "COST" : "GQdUPA8cUV8WsqEdCfDQtphvztocNCoSBGo1wARtaAXK",
            "POPCAT" : "FRhB8L7Y9Qq41qZXYLtC2nw8An1RJfLLxRF2x9RwLLMo"
        }
        self.solana_url = "https://api.dexscreener.com/latest/dex/pairs/bsc/0x1e4600929edf7f36b4a7eac4c7571057d82a246c"
        self.base_url = "https://api.dexscreener.com/latest/dex/pairs/solana/"
        self.counter = 1000

    def get_token_price(self, token_name):
        if token_name == 'SOL':
            response = requests.post(self.solana_url)
        else:
            token_url = self.token_urls[token_name]
            response = requests.post(self.base_url + token_url)
        response = response.json()

        price_usd = response['pair']['priceUsd']
        return float(price_usd)

    def swap_token_for_sol(self, wallet_id, token_name, token_amount):
        token_price = self.get_token_price(token_name)
        sol_price = self.get_token_price("SOL")
        sol_amount = (float(token_amount) * token_price) / sol_price

        wallet = MongoDB.get_wallet_from_db(wallet_id)

        wallet.subtract_token_balance(token_name, token_amount)
        wallet.add_sol_balance(sol_amount)

        reference = self.generate_reference(token_name, True)
        swap_quotation = SwapQuotation(wallet_id, reference, token_name, token_amount, sol_amount, True, datetime.datetime.now())
        MongoDB.add_wallet_to_db(wallet)
        MongoDB.add_swap_quotation_to_db(swap_quotation)

        return swap_quotation

    def swap_sol_for_token(self, wallet, token_name, sol_amount):
        token_price = self.get_token_price(token_name)
        sol_price = self.get_token_price("SOL")
        token_amount = (float(sol_amount) * sol_price) / token_price

        wallet.subtract_sol_balance(sol_amount)
        wallet.add_token_balance(token_name, token_amount)

        print(wallet.token_balances)
        reference = self.generate_reference(token_name, False)
        swap_quotation = SwapQuotation(wallet.wallet_address, reference, token_name, token_amount, sol_amount, True, datetime.datetime.now())
        MongoDB.add_wallet_to_db(wallet)
        MongoDB.add_swap_quotation_to_db(swap_quotation)
        MongoDB.display_fetched_wallet_info(wallet)

        return swap_quotation

    def generate_reference(self, token_name, token_swap):
        ref_prefix = token_name + "SOL" if token_swap else "SOL" + token_name
        ref_suffix = str(self.counter).zfill(4)
        self.counter += 1
        return ref_prefix + ref_suffix