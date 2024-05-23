from locale import format_string
from core.mongo import MongoDB
from core.mongo import MongoDB
import requests
from core.wallet import Wallet
from core.wallet import Wallet
import ast

class ClientHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket
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
        self.tokens = list(self.token_urls.keys())

    def login(self):
        self.client_socket.sendall(b"Enter 1 to login, enter 2 to sign up: ")
        decision = int(self.client_socket.recv(1024).decode())
        if decision == 2:
            self.client_socket.sendall(b"Enter Wallet Address: ")
            wallet_address = self.client_socket.recv(1024).decode()
            if MongoDB.get_wallet_from_db(wallet_address):
                self.client_socket.sendall(b"Wallet Already Exists, returning to Login: ")
                return 0
            self.client_socket.sendall(b"Enter Wallet password: ")
            password = self.client_socket.recv(1024).decode()
            self.client_socket.sendall(b"How much Solana do you want to load in: ")
            sol = self.client_socket.recv(1024).decode()
            MongoDB.add_wallet_to_db(Wallet(wallet_address, wallet_address, password, sol, None))
            self.client_socket.sendall(b"Account Created Successfully: ")
        else:
            exit

    def get_wallet(self):
        MongoDB.add_wallet_to_db(Wallet("eoin", "eoin", "eoin", "1000", None))
        MongoDB.add_wallet_to_db(Wallet("danny", "danny", "danny", "1000", None))
        MongoDB.add_wallet_to_db(Wallet("cian", "cian", "cian", "1000", None))
        MongoDB.add_wallet_to_db(Wallet("alex", "alex", "alex", "100", None))
        MongoDB.add_wallet_to_db(Wallet("rem", "rem", "rem", "100000", None))
        self.client_socket.sendall(b"Enter your wallet address: ")
        self.wallet_address = self.client_socket.recv(1024).decode()
        print("Received wallet address:", self.wallet_address)

    def get_password(self):
        self.client_socket.sendall(b"Enter your wallet password: ")
        self.wallet_password = self.client_socket.recv(1024).decode()
        print("Received wallet password:", self.wallet_password)

    def authenticate_user(self):
        wallet = MongoDB.get_wallet_from_db(self.wallet_address)
        if wallet.wallet_address == 'rem':
            print("""                                   
                                            .:^~~~~~~::.                                    
                            .:.....  ..:~7JY555555YYYJJ?7~^:..                             
                            .......:!?Y5PPGGGGGGGGGGGPP5555J7~~^:..                         
                        .....:~?5GGBBGGBBBBBBBGGGPPPPPPPPP5J7!~~^.......                  
                        .....~JPGBBBBBBBBBGP5J??7!!!~~~^~~!7?JYYYYJ?!^:....                 
                    ...:!5BBBBBB##BG5YJ?7~~~^^^^:::........:^!J55Y!^::......             
                .....^?PBB######G5?77!!~^^^^^^:::...     ......:!J55555YJ?7~:..          
            ......:~JGB#######GY?77!!~~~^^^^:::::..       ........^YB##BGP55YJ!^.        
            ......:!YGG#&&###B5??777!~~~^^^^^:::.....    ............~5##BGGP555Y?^       
            ......:JGB&&&&&#GY??777!!!!~~~~^^^^::...........:::::.....:J###BGPPPP5Y.      
            ......^YB&&&&##GYJ?7777!!!!~~~~~~^^^^::.........:::::::....^Y##BGGGPPPPY:     
            .....:!5#&@&&&BYJ?777!!!!!!~~~~^^^^^^^:::.........:::::.:.::~P#BGBBGP555J.    
            ....:^~G&&&&&#PJ?77!!!!!!~~~^^^^^:::::::...... ..........:::^7GBBBBBBGPJ7~    
            .....:!#&&&&#B5??777!!!~~~^^:::::...::......     ......:::::^~YGBB####B5~^.   
            .....:7#&&&&#GY??777!!!~~~^^^:::.....::...... ......::::::::^~JPB######P!:.   
            ......~B&&&##GY?777!!!~~~~~~^^^^:::::^^::::........:::::::::^~?G####&##G^..   
            ......:5&&&##GJ7!!!~!!~~!!!!~~!~~~^~~~~~~^^^^^^^^::::::::::::^JB#&&####5^..   
            .......?&&&##5?!!!~~~!!~!!!!!!!7!!!!!!77!!!!!~!~^^^^^^^:::..::?#&&&&##B!...   
            :......~#&&&BJ77!!~!!7777?????????7777777?????JJ???7!!!~~^^:::!G&&&&##Y:...   
            :......^B&&&G??JJ?JJJJY5PGGGGGPP5YYJ???JYYY5PPGGGGP5YYYJJ??77!~Y&&&#BB~....   
            :.......P&&#5?J555PPGGBBBBB##BBBGG5Y?777J5PGBB####BBBBBBGGP5YJ~7#&&#BJ.....   
            ::......7##BJ?YPPPGBBB###&&&&&###B5J!~^~!JG##&&&&&&&&&####GPP5!~P#&GP^.....   
            .:::.....:?BG?JYPPPGGGGB#&&#BB#&##B57~^..^!5##&&#B#&&&BGGGGGP5?~^?G##Y:......  
            .::::.....:P57JY55Y555555PPPPPPPPP5?!^^..:^7YPGGGPPPP555YJJ?7!~^^~PBG^........ 
            .::::::...:5Y7????JJYYYYYYJJJJ???77!~^:...:^~7JY555YYYJJ?7!^::::^^J55^........ 
            .:::::::.:.?J7777!!7777777777!!!!!!~^^:....:^~~~!77777!!~^:::::::^!?7^........ 
            ::::::::::.~??77!!!!!~~~~~~~~~!!77~^^^:::...:^~~^^^^^^^:::::::^^^^!~^......... 
            .:::::::::::^???7!!!!~~~~~~~^^~!?777!!~~~~^^^^^~7!~^:::::::::^^^^~~~^:......... 
            :::::::::::~???7!!~~~~~~~~~~~!777JYYYYYJJJJJJ?!!?7!~^^^:::::^^~~~~~^.......... 
            .::::::::^^:!J??77!!~~~~~~~!!!7JY5G##BGGGGGBBBG5?55J7!~~~^^^^^^^~~~^:.........: 
            .:::::^^^^^^!????777!!!!!!!!77JPGGB##BBBBBB####G?75PYJ?7!!~~~~~~~~~~:........:. 
            .^^^^^^^^^^^!?????????????7777?Y55PPPPGGBGGPPP5J~~!?Y5YJ?7!!!!!!!~~~:......:.:  
            ^^^^^^^~~~~~7?JJJYJJJJJJJ?777??JJJJY55PP5YJ?7!~~~~!7?YYYJ??777!!!!:.......::.  
            ^~~~~~~~~~~~7?JJJJJJJJJJJJ???????????7777!~~~^~~~!!!77JYYJ???777!~:...:::::    
            .~~~~~~~!!!!!?JJJJJJJJJJYYY5YYJ??JJJJJ7777?J?7!!!7???7??JJ????77!J7..:::::.    
            ~~~~!!!!!!!75JJJJJJ???JYPGGGP5PPPPPP555555PPPGGPPGG5J?77???7777?B&7.:::.      
            ^!~!!!!!!!7G&PJYJJJJ???JYYJ????7777!!!!~~~~~!!777J55YJ?777?????5&&#^:::       
            ~!!!!!7?YG&@&5JYYJJJJJJJ??777?????JJJ???7!!!~~~~!7?JJ??7?????JB&&&Y:.        
                ~5PPB#&&&@@@&YYYYYYYYYJ??777??JJY555YYYJJ?7!!~!!77?YYJJJJJJJ5&&&&#!         
                Y&&@@@&&@@@@&5YYYYYYJJ?7777??JJJJJJJJ??77!!!!!!77?JYYYYYYYJ#@&&#^          
                P@@@@@&@@@@@&55555YYY???777777777!!!!!!~~~~~~!!7?JY5555YYP&&&@:           
                ^B@@@@@@@@@@&PPPPPP55J??777!!!!!!~~~~~~~~~~~!7?5PGGPP55P#&&&J            
                    :B@@@@@@@@@@#PPPPPP55YJJJ????77777777777777J5PGGGPPPPB#&@&!             
                    Y@@@@@@@@@@&GP5P55555555YYYYYYJJYYYYYYY5PPPPPPPPGBB5PJ^               
                    :~J5#@@@@@@&BPP5555Y55PGGGGGGGGGGGGBGGPP55PGGGGP~.                   
                            ^~7#&@@@&BGP5555555PPPGGGGGGGGGGPPPPGP??^                       
                                .^?5GGGGPP55555PPPGGGGGGGGGGP?~.                           
                                    .~~~JJ????JJJJJJJJ7~~~. 
            """)
            print("""
                      ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗
                      ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝    
                      ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗      
                      ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝      
                      ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗    
                       ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝    
            """)
            print("""
                                    ██████╗ ███████╗███╗   ███╗
                                    ██╔══██╗██╔════╝████╗ ████║
                                    ██████╔╝█████╗  ██╔████╔██║
                                    ██╔══██╗██╔══╝  ██║╚██╔╝██║
                                    ██║  ██║███████╗██║ ╚═╝ ██║
                                    ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝
            """)

        if wallet.password != self.wallet_password:
           self.client_socket.sendall(b"Incorrect password provided for wallet")
           self.client_socket.close()
        elif wallet is None:
           self.client_socket.sendall(b"The wallet provided does not currently exist")
           self.client_socket.close()
        else:
            self.wallet = wallet

    def stake_or_unstake(self):
        # Prompt the user for action
        wallet = MongoDB.get_wallet_from_db(self.wallet_address)
        wallet_address = str(wallet.wallet_address)
        self.client_socket.sendall(b"Enter '1' to stake, '2' to unstake, '3' to check staked amount, or '0' to return to main menu: ")
        decision_made = self.client_socket.recv(1024).decode().strip()

        if decision_made == '1':
            # Handle staking
            self.client_socket.sendall(b"Enter the amount to stake, must be positive float: ")
            amount_str = self.client_socket.recv(1024).decode().strip()
            amount = float(amount_str)
            if amount <= 0:
                self.client_socket.sendall(b"Incorrect input! Make sure to read the instructions and try to run the program again. Press enter to return to menu.1")
                self.decision()
            response = requests.post('http://host.docker.internal:8082/stakeSol', json={'wallet_address': wallet_address, 'amount': amount})
            response_dict = response.json()
            print(response_dict['Status'])
            self.print_staked_amount(wallet_address)

        elif decision_made == '2':
            # Handle unstaking
            self.client_socket.sendall(b"Enter the amount to unstake, must be positive float: ")
            amount_str = self.client_socket.recv(1024).decode().strip()
            amount = float(amount_str)
            if amount <= 0:
                self.client_socket.sendall(b"Incorrect input! Make sure to read the instructions and try to run the program again. Press enter to return to menu.2")
                self.decision()
            response = requests.post('http://host.docker.internal:8082/unstakeSol', json={'wallet_address': wallet_address, 'amount': amount})
            response.raise_for_status()
            self.print_staked_amount(wallet_address)
            return amount  # Successfully unstaked, return the amount

        elif decision_made == '3':
            # Check staked amount
            response = requests.get('http://host.docker.internal:8082/getStakedAmount', params={'wallet_address': wallet_address})
            staked_amount = response.json().get('stakedAmount', 0)
            self.print_staked_amount(wallet_address)
            return staked_amount

        elif decision_made == '0':
            # Return to main menu
            self.decision()

        else:
            self.client_socket.sendall(b"Incorrect input! Make sure to read the instructions and try to run the program again. Press enter return to Menu.3")
            self.decision()
        self.decision()
        
    def print_staked_amount(self, wallet_address):
        responce = requests.get('http://host.docker.internal:8082/getStakedAmount', params={'wallet_address': self.wallet_address})
        staked_amount = responce.json().get('stakedAmount')
        
        format_string = (
        "|===============================================================|\n"
        "|                                                               |\n"
        "| Wallet address: {:<46}|\n"
        "|                                                               |\n"
        "| Staked Amount in SOL: {:<40}|\n"
        "|                                                               |\n"
        "| Press Enter To Return To Menu                                 |\n"
        "|===============================================================|\n"
    ).format(wallet_address, staked_amount)

        self.client_socket.sendall(format_string.encode('utf-8'))
        self.decision()
    
    def transfer_funds(self):
        wallet = MongoDB.get_wallet_from_db(self.wallet_address)
        wallet_address = str(self.wallet_address)
        
        self.client_socket.sendall(b"\nEnter Wallet Address to Send to: ")
        recipent_address = str(self.client_socket.recv(1024).decode())
        
        if MongoDB.get_wallet_from_db(recipent_address) == None:
            self.client_socket.sendall(b"\nNo Account With Associated Address, Do Not Make This Mistake Again, press enter to return to main menu")
            self.decision()
        
        else:
            self.client_socket.sendall(b"\nEnter the amount to transfer: ")
            amount = int(self.client_socket.recv(1024).decode())

            if (int(amount) > 0) and (int(wallet.sol_balance) > int(amount)):
                response = requests.post('http://host.docker.internal:8084/transfer', json={'from': wallet_address, 'to': recipent_address, 'amount': amount})
                response_dict = response.json() 
                status = response_dict["Status"]
                balance = response_dict["Updated balance"]
                display = (
                    "\n|===============================================================|\n"
                    "|                                                               |\n"
                    "| Transfer Status: {status:<45}|\n"
                    "|                                                               |\n"
                    "| Updated Balance: ${balance:<44}|\n"
                    "|                                                               |\n"
                    "| Press Enter to Return to Menu                                 |\n"
                    "|                                                               |\n"
                    "|===============================================================|\n"
                ).format(status=status, balance=balance)
                self.client_socket.sendall(display.encode('utf-8'))
                self.decision()
            elif (int(amount) <= 0):
                self.client_socket.sendall(b"\nInvalid Transfer Amount, You Are Ruining The Project, press enter to return to main menu")
                self.decision()
            elif (int(wallet.sol_balance) < int(amount)):
                self.client_socket.sendall(b"\nNot Enough Funds, Get Your Money Up! Press enter to return to Main menu")
                self.decision()
                    
    def decision(self):
        menu = (
        "\n|===============================================================|\n"
        "|                                                               |\n"
        "| Wallet address: {wallet:<46}|\n"
        "|                                                               |\n"
        "| Please select a function:                                     |\n"
        "|                                                               |\n"
        "| 1. Display portfolio                                          |\n"
        "| 2. Stake Solana                                               |\n"
        "| 3. Swap Currencies                                            |\n"
        "| 4. Transfer Funds                                             |\n"
        "|                                                               |\n"
        "|===============================================================|\n"
        "\n"
        "Value entered : "
        ).format(wallet=self.wallet_address)

        self.client_socket.sendall(menu.encode('utf-8'))
        self.decision_made = self.client_socket.recv(10240).decode()

        if self.decision_made in ('1', '2', '3', '4'):
            if self.decision_made in ('1'):
                self.display_portfolio()
            if self.decision_made in ('2'):
                print("Deciding To Stake Solana", self.decision_made)
                self.stake_or_unstake()  # Added 'self' parameter
            if self.decision_made in ('3'):
                self.swap()
            if self.decision_made in ('4'):
                print("Deciding To Transfer Funds", self.decision_made)
                self.transfer_funds()  # Added 'self' parameter
        else:
            print("Invalid Decision!")
            self.decision()
            
    def swap(self):
        menu = (
            "\n|===============================================================|\n"
            "|                                                               |\n"
            "| Wallet address: {wallet:<46}|\n"
            "|                                                               |\n"
            "| Please select a function:                                     |\n"
            "|                                                               |\n"
            "| 1. Swap Sol for a token                                       |\n"
            "| 2. Swap a token for Sol                                       |\n"
            "| 3. Get swap history                                           |\n"
            "| 4. Get swap with given reference                              |\n"
            "|                                                               |\n"
            "|===============================================================|\n"
            "\n"
        ).format(wallet=self.wallet_address)

        self.client_socket.sendall(menu.encode('utf-8'))
        choice = self.client_socket.recv(1024).decode()

        if choice == '1':
            option_chosen = self.get_token_choice()
            if (int(option_chosen) > len(self.tokens)) or (int(option_chosen) < 1):
                self.client_socket.sendall("Invalid option, press enter to return to main menu")
                self.decision()
            option_chosen = ast.literal_eval(option_chosen) - 1
            self.client_socket.sendall(b"Please enter Sol amount: ")
            sol_amount = self.client_socket.recv(1024).decode()
            if ((int(sol_amount) <=0) or (int(sol_amount) > (int(MongoDB.get_wallet_from_db(self.wallet_address).sol_balance)))):
                self.client_socket.sendall(b"Invalid Amount, press enter to return to main menu: ")
                self.decision()
            token_name = self.tokens[option_chosen]
            wallet_id = self.wallet.wallet_address

            # Make the POST request
            response = requests.post('http://host.docker.internal:8083/swapsol', json={'wallet': wallet_id, 'token': token_name, 'amount': sol_amount})
            response_dict = response.json()

            self.client_socket.sendall(b"Swap complete ! Press enter to continue ! ")
            self.decision()
        elif choice == '2':
            option_chosen = int(self.get_token_choice()) - 1
            self.client_socket.sendall(b"Please enter token amount: ")
            token_amount = self.client_socket.recv(1024).decode()            
            token_name = self.tokens[option_chosen]
            wallet_id = self.wallet.wallet_address

            response = requests.post('http://host.docker.internal:8083/swap/token', json={'wallet': wallet_id, 'token': token_name, 'amount': token_amount})
            response_dict = response.json()

            self.client_socket.sendall(b"Swap complete ! Press enter to continue ! ")
            self.decision()
        elif choice == '3':
            response = requests.post('http://host.docker.internal:8083/quotations', json={'wallet_id': self.wallet_address})
            response_dict = response.json()

            total_references = len(response_dict)
            display = ""
            for index, reference_dict in enumerate(response_dict.values()):
                if index == total_references - 1:
                    display += self.print_reference(reference_dict, True)
                else:
                    display += self.print_reference(reference_dict, False)

            self.client_socket.sendall(display.encode('utf-8'))
            self.decision()
        elif choice == '4':
            self.client_socket.sendall(b"Please enter a reference: ")
            reference = self.client_socket.recv(1024).decode()

            response = requests.post('http://host.docker.internal:8083/quotation', json={'wallet': self.wallet_address, 'reference': reference})
            response_dict = response.json()

            display = self.print_reference(response_dict, True)
            self.client_socket.sendall(display.encode('utf-8'))
            self.decision()
        else:
            self.client_socket.sendall(b"Error : Invalid choice ! Press enter to return to menu")
            self.decision()

    def print_reference(self, reference_dictionary, prompt):
        # Check transaction status
        if reference_dictionary['swap_occurred'] == True:
            transaction_status = 'Success'
        else:
            transaction_status = 'Failure'

        # Create the formatted string
        display = (
            "\n|===============================================================|\n"
            "|                                                               |\n"
            "| Wallet address: {wallet_address:<46}|\n"
            "| Reference: {reference:<51}|\n"
            "| Token Name: {token_name:<50}|\n"
            "| Token Amount: {token_amount:<48}|\n"
            "| Sol Amount: {sol_amount:<50}|\n"
            "| Transaction Status: {swap_occurred:<42}|\n"
            "| Timestamp: {timestamp:<51}|\n"
        ).format(wallet_address=reference_dictionary['wallet_address'], reference=reference_dictionary['reference'], token_name=reference_dictionary['token_name'], 
                 token_amount=reference_dictionary['token_amount'], sol_amount=reference_dictionary['sol_amount'], swap_occurred=transaction_status,
                 timestamp=reference_dictionary['timestamp'])

        # Finish the menu with the bottom border
        if prompt is True:
            display += "|                                                               |\n"
            display += "| Press Enter to Return to Menu                                 |\n"

        display += "|                                                               |\n"
        display += "|===============================================================|"
        return display

    def get_token_choice(self):
        menu = (
            "|===============================================================|\n"
            "|                                                               |\n"
            "| Please select a token:                                        |\n"
            "|                                                               |\n"
        )
        for index, token in enumerate(self.tokens, start=1):
            if index >= 10:
                menu += "| {0}. {1:<58}|\n".format(index, token)
            else:
                menu += "| {0}. {1:<59}|\n".format(index, token)
        menu += "|                                                               |\n"
        menu += "|===============================================================|\n"

        self.client_socket.sendall(menu.encode('utf-8'))
        token_choice = self.client_socket.recv(1024).decode()
        print(token_choice)
        return token_choice


    def display_portfolio(self):
        # Define the data
        wallet = MongoDB.get_wallet_from_db(self.wallet.wallet_address)
        portfolio_value = 0
        portfolio = []

        # Add sol first
        sol_data = ['SOL']
        sol_balance = wallet.sol_balance
        sol_data.append(sol_balance)
        response = requests.post('http://host.docker.internal:8081/token', json={"token": 'SOL'})
        response_dict = response.json()
        current_price = response_dict['price']
        value = float(current_price) * float(sol_balance)
        portfolio_value += value 
        sol_data.append(value)
        sol_data.append(response_dict['price_change'])
        portfolio.append(sol_data)

        # Now iterate over tokens
        for token_name, token_amount in wallet.token_balances.items():
            token_data = []
            token_data.append(token_name)
            token_data.append(token_amount)
            response = requests.post('http://host.docker.internal:8081/token', json={"token": token_name})
            response_dict = response.json()
            current_price = response_dict['price']
            value = float(current_price) * float(token_amount)
            portfolio_value += value 
            token_data.append(value)
            token_data.append(response_dict['price_change'])
            portfolio.append(token_data)
            
        # Create the formatted string
        display = (
            "\n|===============================================================|\n"
            "|                                                               |\n"
            "| Wallet address: {wallet_address:<46}|\n"
            "|                                                               |\n"
            "| Portfolio Value: ${value:<44}|\n"
            "|                                                               |\n"
            "| Tokens        Amount      Value       24hr % Change           |\n"
        ).format(wallet_address=wallet.wallet_address, value=round(portfolio_value, 2))

        # Add each token row to the menu
        for token in portfolio:
            display += "| {0:<13} {1:<11} {2:<11} {3:<24}|\n".format(token[0], round(float(token[1]), 2), round(float(token[2]), 2), float(token[3]))

        # Finish the menu with the bottom border
        display += "|                                                               |\n"
        display += "| Press Enter to Return to Menu                                 |\n"
        display += "|                                                               |\n"
        display += "|===============================================================|"

        # Output the string
        self.client_socket.sendall(display.encode('utf-8'))

        self.decision()
