# Distributed Systems Project - Cryptocurrency Service
## Oklahoma City Thunder

## Members:
- Eoin McMahon 20387437
- Alex O'Donnell 20456522
- Danny Murray 19331403
- Cian Kelly 20429616


## Technologies Implemented:
- Docker
- Kubernetes
- REST Architecture (Flask)
- WebSockets
- MongoDB
- Gunicorn
- Swagger
- Python

## Microservices:
- Portfolio:
  - Client can view their account balance through their portfolio.
- Swap:
  - Client can swap SOL (native currency for the platform) with other available tokens, as well as view their swapping history.
- Stake:
  - Client can stake their SOL to receive rewards over time.
- Transfer:
  - Client can transfer funds from their wallet to another user's wallet.
 
## Summary
This code produces a functional and working cryptocurrency trading platform. Upon starting the system, the user is prompted with an option to login or sign up. Logging in prompts the user to input their wallet address and password before proceeding to check that this account is registered. To sign up, a user is prompted to create a wallet address, password, and load data. This address is checked within the database to ensure it is not associated with an account.

Within the system, users are offered four options: to display their portfolio, to stake funds, to swap funds, and to transfer funds.

When display portfolio is clicked, it displays the wallet address, the users solana balance, and any tokens that they own.

Within stake, users are offered the option to stake solana, unstake solana or display their associated staked amount.

Within swap, users are offered the option to swap solana for a given token, swap a given token for solana, or display their swap history, which is based on either the wallet or for a given reference.

Within transfer, the user is prompted to enter the wallet address to transfer money to, along with the amount, and the money will aptly be transferred between the two accounts.


## How to Run:
To run the project, follow these steps:
1. Start minikube: `minikube start`
2. Run `eval $(minikube docker-env)`
3. Build Docker images: `docker-compose build`
4. Port forward services:
    kubectl port-forward service/server-service 12345:12345 &
    kubectl port-forward service/portfolio-service 8081:8081 & 
    kubectl port-forward service/stake-service 8082:8082 &
    kubectl port-forward service/swap-service 8083:8083 &
    kubectl port-forward service/transfer-service 8084:8084
5. Lastly, open a new terminal and run the client:
   -python -m client.client
