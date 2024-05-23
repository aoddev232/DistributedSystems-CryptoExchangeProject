import json
from flask import Flask, request, jsonify
from flasgger import Swagger
from transfer_service.transfer import TransferService
from core.mongo import MongoDB


app = Flask(__name__)
swagger = Swagger(app, template={
    "info": {
        "title": "Transfer Endpoints",
        "description": "Endpoints for making transfers between wallets"
    }
})

# This will act as the in-memory database
wallets = {}

transfer_service = TransferService()

@app.route('/transfer', methods=['POST'])
def transfer_funds():
    """
    Transfer funds from one wallet to another.

    This endpoint expects a JSON request containing 'from', 'to', and 'amount' parameters.
    It retrieves the source and destination wallets based on the provided wallet IDs.
    Then, it calls the `transfer_money` method from TransferService to perform the funds transfer.
    If the transfer is successful, it updates the wallets in the database and returns a JSON response
    with the status and the updated balance of the source wallet. If the transfer fails, it returns
    a JSON response with an error message and status code 400.

    ---
    tags:
      - Transfer
    parameters:
      - in: body
        name: transfer_request
        required: true
        schema:
          type: object
          properties:
            from:
              type: string
              description: The address of the source wallet.
            to:
              type: string
              description: The address of the destination wallet.
            amount:
              type: number
              description: The amount to transfer.
    responses:
      200:
        description: Returns a JSON response with the status and the updated balance of the source wallet.
      400:
        description: Returns a JSON response with an error message if the transfer fails.
    """
    transfer_request = request.get_json()
    from_wallet_id = transfer_request.get('from')
    to_wallet_id = transfer_request.get('to')
    amount = transfer_request.get('amount')

    from_wallet = MongoDB.get_wallet_from_db(from_wallet_id)
    to_wallet = MongoDB.get_wallet_from_db(to_wallet_id)

    # Call transferMoney method from TransferService
    transfer_result = transfer_service.transfer_money(from_wallet, to_wallet, amount)
    if transfer_result == "Transfer successful.":
        # Update the wallets in the map
        MongoDB.add_wallet_to_db(from_wallet)
        MongoDB.add_wallet_to_db(to_wallet)
        new_balance = from_wallet.sol_balance
        response = {
            "Status": "Successfully transferred",
            "Updated balance": f"Updated balance is: {new_balance}"
        }
        json_result = json.dumps(response)
        return json_result
    else:
        return jsonify({"error": transfer_result}), 400

if __name__ == '__main__':
    app.run()
