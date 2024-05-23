from pymongo import MongoClient
from datetime import datetime
from core.wallet import Wallet
from core.swap_quotation import SwapQuotation
from core.staking_info import StakingInfo

class MongoDB:
    wallet_collection_name = "wallets_collection"
    swap_quotation_collection_name = "swap_quotation_collection"
    staking_info_collection_name = "staking_info_collection"

    @staticmethod
    def get_database():
        client = MongoClient("mongodb://host.docker.internal:27017")
        return client["mydatabase"]

    @staticmethod
    def add_wallet_to_db(wallet):
        db = MongoDB.get_database()
        collection = db[MongoDB.wallet_collection_name]
        wallet_doc = {
            "walletAddress": wallet.wallet_address,
            "walletTag": wallet.wallet_tag,
            "walletSol": wallet.sol_balance,
            "walletPassword": wallet.password,
            "walletTokens": wallet.token_balances
        }
        filter = {"walletAddress": wallet.wallet_address}
        result = collection.replace_one(filter, wallet_doc, upsert=True)
        print("Inserted or Updated Wallet:", wallet.wallet_address)

    @staticmethod
    def get_wallet_from_db(wallet_address):
        db = MongoDB.get_database()
        collection = db[MongoDB.wallet_collection_name]
        wallet_doc = collection.find_one({"walletAddress": wallet_address})
        if wallet_doc:
            wallet_doc.pop('_id', None)  # Remove the MongoDB-specific '_id' field
            # Manually create a new Wallet object using the specific fields
            # Adjust the parameter names to match the Wallet class constructor
            wallet = Wallet(
                wallet_address=wallet_doc["walletAddress"], 
                wallet_tag=wallet_doc["walletTag"],
                password=wallet_doc["walletPassword"], 
                sol=wallet_doc["walletSol"],
                tokens=wallet_doc.get("walletTokens", {})  # Use 'tokens' as per the Wallet class definition
            )
            #print("Retrieved the following wallet from the database:")
            MongoDB.display_fetched_wallet_info(wallet)
            return wallet
        print("No wallet associated with the Wallet Address:", wallet_address)
        return None


    @staticmethod
    def add_swap_quotation_to_db(quotation):
        db = MongoDB.get_database()
        collection = db[MongoDB.swap_quotation_collection_name]
        quotation_doc = {
            "walletAddress": quotation.wallet_address,
            "reference": quotation.reference,
            "tokenName": quotation.token_name,
            "tokenAmount": quotation.token_amount,
            "solAmount": quotation.sol_amount,
            "swapOccurred": quotation.swap_occurred,
            "timestamp": quotation.timestamp
        }
        result = collection.insert_one(quotation_doc)
        print("Inserted Swap Quotation with ID:", quotation.wallet_address)

    @staticmethod
    def get_swap_quotations_from_db(wallet_address):
        all_swap_quotations = []
        try:
            # Connect to MongoDB
            client = MongoClient("mongodb://host.docker.internal:27017")
            db = client["mydatabase"]
            collection = db["swap_quotation_collection"]

            # Query documents
            documents = collection.find({"walletAddress": wallet_address})

            for document in documents:
                swap_quotation = SwapQuotation(
                    document["walletAddress"],
                    document["reference"],
                    document["tokenName"],
                    document["tokenAmount"],
                    document["solAmount"],
                    document["swapOccurred"],
                    document["timestamp"]
                )
                all_swap_quotations.append(swap_quotation)

            print("The following Swap Quotations were retrieved from the database from the wallet address:", wallet_address)
            MongoDB.display_fetched_quotation_references(all_swap_quotations)

        except Exception as e:
            print(e)

        return all_swap_quotations

    @staticmethod
    def add_staking_info_to_db(staking_info):
        db = MongoDB.get_database()
        collection = db[MongoDB.staking_info_collection_name]
        staking_doc = {
            "walletAddress": staking_info.wallet_address,
            "amount": staking_info.amount,
            "startTime": staking_info.start_time
        }
        filter = {"walletAddress": staking_info.wallet_address}
        result = collection.replace_one(filter, staking_doc, upsert=True)
        print("Inserted or Updated Staking Info:", staking_info._wallet_address)

    @staticmethod
    def get_staking_info_from_db(wallet_address):
        try:
            # Connect to MongoDB
            client = MongoClient("mongodb://host.docker.internal:27017")
            db = client["mydatabase"]
            collection = db["staking_info_collection"]

            # Query document
            staking_doc = collection.find_one({"walletAddress": wallet_address})

            if staking_doc:
                staking_doc.pop('_id', None)  # Remove the MongoDB-specific '_id' field
                print("Retrieved the following staking information from the Wallet Address:", wallet_address)
                staking_info = StakingInfo(
                    wallet_address,
                    staking_doc["amount"],
                    staking_doc["startTime"]
                )
                MongoDB.display_fetched_staking_info(staking_info)
                return staking_info
            else:
                print("No staking info associated with the Wallet Address:", wallet_address)
                return None

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def clear_database():
        db = MongoDB.get_database()
        db[MongoDB.wallet_collection_name].delete_many({})
        db[MongoDB.swap_quotation_collection_name].delete_many({})
        db[MongoDB.staking_info_collection_name].delete_many({})

    def test_collections_empty():
        client = MongoClient("mongodb://host.docker.internal:27017")
        db = client["mydatabase"]

        wallet_count = db[MongoDB.wallet_collection_name].count_documents({})
        swap_quotation_count = db[MongoDB.swap_quotation_collection_name].count_documents({})
        staking_info_count = db[MongoDB.staking_info_collection_name].count_documents({})

        print("Wallet Collection Empty:", wallet_count == 0)
        print("Swap Quotation Collection Empty:", swap_quotation_count == 0)
        print("Staking Info Collection Empty:", staking_info_count == 0)
        print("\n")
    
    def display_fetched_quotation_references(quotations):
        print("\nFetched Quotation References: \n")
        for quotation in quotations:
            print("Reference: " + quotation.reference)
            print("Wallet Address: " + quotation.wallet_address)
            print("Token Name: " + quotation.token_name)
            print(f"Token Amount: {quotation.token_amount}")
            print(f"Solana Amount: {quotation.sol_amount}")
            print(f"Timestamp: {quotation.timestamp}\n")
        print("\n\n")

    def display_fetched_staking_info(staking_info):
        print("\nFetched Staking Info: ")
        print("Wallet Address: " + staking_info.wallet_address)
        print("Amount:", staking_info.amount)
        print("Start Time:", staking_info.start_time)
        print("\n\n")

    def display_fetched_wallet_info(wallet):
        print("\nFetched Wallet Details: ")
        print("Wallet Address: " + wallet._wallet_address)
        print("Wallet Tag: " + wallet._wallet_tag)
        print(f"Wallet Solana Balance: {wallet._sol}")

        print("Tokens in Wallet: ")
        for token_name, balance in wallet._tokens.items():  # Use .items() to iterate over both keys and values
            print(f"{token_name} : {balance}")

        print("\n\n")

    def testMongo():
        # Test Wallet:
        wallet = Wallet("WalletAddress1", "DEV", "Password", None)
        wallet.add_sol_balance(100)
        wallet.add_token_balance("SaddleToken", 200)
        wallet.add_token_balance("EoinerCoin", 1000)
        MongoDB.add_wallet_to_db(wallet)
        test_wallet = MongoDB.get_wallet_from_db("WalletAddress1")

        # Test Staking Info:
        stakinginfo = StakingInfo("WalletAddress1", 200, datetime.now())
        MongoDB.add_staking_info_to_db(stakinginfo)
        stakingingotest = MongoDB.get_staking_info_from_db("WalletAddress1")

        # Test Quotations:
        swapquotation = SwapQuotation("WalletAddress1", "Reference1", "SaddleToken", 100, 200, True, datetime.now())
        swapquotation2 = SwapQuotation("WalletAddress1", "Reference2", "SaddleToken", 200, 400, True, datetime.now())
        MongoDB.add_swap_quotation_to_db(swapquotation)
        MongoDB.add_swap_quotation_to_db(swapquotation2)
        quotations = MongoDB.get_swap_quotations_from_db("WalletAddress1")

def main():
    print("Clearing collections...")
    MongoDB.clear_database()
    print("Testing if collections are empty...")
    MongoDB.test_collections_empty()

    MongoDB.testMongo()

if __name__ == "__main__":
    main()

