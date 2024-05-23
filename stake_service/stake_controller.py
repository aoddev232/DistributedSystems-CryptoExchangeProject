import json
from flask import Flask, request, jsonify
from flasgger import Swagger
from stake_service.stake import Stake

app = Flask(__name__)
swagger = Swagger(app, template={
    "info": {
        "title": "Stake Endpoints",
        "description": "Endpoints for staking and unstaking Solana"
    }
})

stake_service = Stake()

@app.route('/stakeSol', methods=['POST'])
def stake_sol():
    """
    Stake SOL tokens from a specified wallet.

    This endpoint expects a JSON request containing 'wallet_address' and 'amount' parameters.
    It parses the JSON data from the POST request and retrieves the amount and wallet address.
    Then, it attempts to stake the specified amount of SOL tokens using the `stake_sol` method
    from the stake_service. If the stake operation is successful, it returns a JSON response
    with a success message and status code 200. If an error occurs during the stake operation,
    it returns a JSON response with an error message and status code 400.

    ---
    tags:
      - Stake
    parameters:
      - in: body
        name: stake_request
        required: true
        schema:
          type: object
          properties:
            wallet_address:
              type: string
              description: The address of the wallet to stake SOL tokens from.
            amount:
              type: number
              description: The amount of SOL tokens to stake.
    responses:
      200:
        description: Returns a JSON response with a success message if the stake operation is successful.
      400:
        description: Returns a JSON response with an error message if the stake operation fails.
    """
    data = request.get_json()  # Correctly parsing JSON data from POST request
    amount = data.get('amount')
    wallet_address = data.get('wallet_address')
    stake_result = stake_service.stake_sol(wallet_address, amount)
    if stake_result == "Stake successful.":
        response = {
            "Status": "Successfully Staked Solana",
        }
        json_result = json.dumps(response)
        return json_result
    else:
      return jsonify(error=f"Failed to stake SOL"), 400
    

@app.route('/unstakeSol', methods=['POST'])
def unstake_sol():
    """
    Unstake SOL tokens from a specified wallet.

    This endpoint expects a JSON request containing 'wallet_address' and 'amount' parameters.
    It parses the JSON data from the POST request and retrieves the amount and wallet address.
    Then, it attempts to unstake the specified amount of SOL tokens using the `unstake_sol` method
    from the stake_service. If the unstake operation is successful, it returns a JSON response
    with a success message and status code 200. If an error occurs during the unstake operation,
    it returns a JSON response with an error message and status code 400.

    ---
    tags:
      - Unstake
    parameters:
      - in: body
        name: unstake_request
        required: true
        schema:
          type: object
          properties:
            wallet_address:
              type: string
              description: The address of the wallet to unstake SOL tokens from.
            amount:
              type: number
              description: The amount of SOL tokens to unstake.
    responses:
      200:
        description: Returns a JSON response with a success message if the unstake operation is successful.
      400:
        description: Returns a JSON response with an error message if the unstake operation fails.
    """
    data = request.get_json()
    amount = data['amount']
    wallet_address = data['wallet_address']
    try:
        stake_service.unstake_sol(wallet_address, amount)
        return jsonify(message=f"Successfully unstaked {amount} SOL"), 200
    except Exception as e:
        return jsonify(error=f"Failed to unstake SOL: {str(e)}"), 400

@app.route('/getStakedAmount', methods=['GET'])
def get_staked_amount():
    """
    Retrieve the amount of SOL tokens staked by a specified wallet.

    This endpoint expects a query parameter 'wallet_address' specifying the address of the wallet.
    It retrieves the staked amount for the specified wallet using the `get_staked_amount` method
    from the stake_service. If the staked amount is found, it returns a JSON response with the
    staked amount and status code 200. If no staked amount is found for the wallet, it returns
    a JSON response with an error message and status code 404.

    ---
    tags:
      - Stake
    parameters:
      - in: query
        name: wallet_address
        required: true
        schema:
          type: string
        description: The address of the wallet to retrieve staked amount for.
    responses:
      200:
        description: Returns a JSON response with the staked amount.
      400:
        description: Returns a JSON response with an error message if the wallet address is missing.
      404:
        description: Returns a JSON response with an error message if no staked amount is found.
    """
    wallet_address = request.args.get('wallet_address')
    if not wallet_address:
        return jsonify(error="Wallet address is required"), 400
    staked_amount = stake_service.get_staked_amount(wallet_address)
    print(staked_amount)
    if staked_amount is not None:
        return jsonify(stakedAmount=staked_amount), 200
    else:
        return jsonify(error="No amount found"), 404

if __name__ == '__main__':
    app.run()
