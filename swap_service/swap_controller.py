from flask import Flask, jsonify, request
from flasgger import Swagger
from core.mongo import MongoDB
import json

from swap_service.swapper import Swapper

swapper = Swapper()

app = Flask(__name__)
swagger = Swagger(app, template={
    "info": {
        "title": "Swap Endpoints",
        "description": "Endpoints for swapping tokens"
    }
})

@app.route('/quotations', methods=['POST'])
def getQuotations():
    """
    Retrieve swap quotations for a given wallet.

    This endpoint expects a JSON request containing a 'wallet' parameter.
    It retrieves swap quotations for the specified wallet from the database
    using the `get_swap_quotations_from_db` method from MongoDB.
    It then constructs a nested dictionary containing the quotations and
    converts it to a JSON string for the response.

    ---
    tags:
      - Quotations
    parameters:
      - in: body
        name: wallet
        required: true
        schema:
          type: object
          properties:
            wallet:
              type: string
              description: The ID of the wallet to retrieve swap quotations for.
    responses:
      200:
        description: Returns JSON response with swap quotations.
      400:
        description: Returns a JSON response with an error message if the request is not in JSON format.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    wallet_id = data['wallet_id']
    swap_quotations = MongoDB.get_swap_quotations_from_db(wallet_id)
    nested_quotations = {}
    for index, quotation in enumerate(swap_quotations):
        reference_dict = {
                'wallet_address':quotation.wallet_address,
                'reference':quotation.reference,
                'token_name':quotation.token_name,
                'token_amount':quotation.token_amount,
                'sol_amount':quotation.sol_amount,
                'swap_occurred':quotation.swap_occurred,
                'timestamp':str(quotation.timestamp)
        }
        nested_quotations[index] = reference_dict
    json_result = json.dumps(nested_quotations)
    return json_result

@app.route('/quotation', methods=['POST'])
def getQuotation():
    """
    Retrieve a swap quotation for a given wallet and reference.

    This endpoint expects a JSON request containing 'wallet' and 'reference' parameters.
    It retrieves swap quotations for the specified wallet from the database using
    the `get_swap_quotations_from_db` method from MongoDB. It then searches for a
    quotation with the specified reference and returns its details if found.
    If no matching reference is found for the given wallet, it returns a JSON response
    with an error message and status code 400.

    ---
    tags:
      - Quotations
    parameters:
      - in: body
        name: quotation_request
        required: true
        schema:
          type: object
          properties:
            wallet:
              type: string
              description: The ID of the wallet to retrieve the quotation for.
            reference:
              type: string
              description: The reference of the quotation to retrieve.
    responses:
      200:
        description: Returns JSON response with the quotation details.
      400:
        description: Returns a JSON response with an error message if the request is not in JSON format
                     or if the reference for the given wallet is not found.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    wallet = data['wallet']
    reference = data['reference']
    swap_quotations = MongoDB.get_swap_quotations_from_db(wallet)
    for quotation in swap_quotations:
        if quotation.reference == reference:
            reference_dict = {
                'wallet_address':quotation.wallet_address,
                'reference':quotation.reference,
                'token_name':quotation.token_name,
                'token_amount':quotation.token_amount,
                'sol_amount':quotation.sol_amount,
                'swap_occurred':quotation.swap_occurred,
                'timestamp':str(quotation.timestamp)
            }

            json_result = json.dumps(reference_dict)
            return json_result
    return jsonify({"error": "Couldn't find reference for the given wallet"}), 400

@app.route('/swap/token', methods=['POST'])
def swapToken():
    """
    Swap tokens for SOL.

    This endpoint expects a JSON request containing 'wallet', 'token', and 'amount' parameters.
    It swaps the specified amount of tokens for SOL using the `swap_token_for_sol` method
    from the swapper and adds the swap quotation to the database using the `add_swap_quotation_to_db`
    method from MongoDB. It then constructs a dictionary containing the details of the swap
    quotation and returns it as a JSON response.

    ---
    tags:
      - Swap
    parameters:
      - in: body
        name: swap_request
        required: true
        schema:
          type: object
          properties:
            wallet:
              type: string
              description: The ID of the wallet initiating the swap.
            token:
              type: string
              description: The name of the token to swap.
            amount:
              type: number
              description: The amount of tokens to swap for SOL.
    responses:
      200:
        description: Returns a JSON response with the details of the swap quotation.
      400:
        description: Returns a JSON response with an error message if the request is not in JSON format.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    wallet_id = data['wallet']
    token_name = data['token']
    token_amount = data['amount']

    quotation = swapper.swap_token_for_sol(wallet_id, token_name, token_amount)
    MongoDB.add_swap_quotation_to_db(quotation)

    quotation_dict = {
        'wallet_address':quotation.wallet_address,
        'reference':quotation.reference,
        'token_name':quotation.token_name,
        'token_amount':quotation.token_amount,
        'sol_amount':quotation.sol_amount,
        'swap_occurred':quotation.swap_occurred,
        'timestamp':str(quotation.timestamp)
    }
    json_result = json.dumps(quotation_dict)
    return json_result

@app.route('/swapsol', methods=['POST'])
def swap_sol():
    """
    Swap SOL for tokens.

    This endpoint expects a JSON request containing 'wallet', 'token', and 'amount' parameters.
    It retrieves the wallet information from the database using the `get_wallet_from_db` method
    from MongoDB. Then, it swaps the specified amount of SOL for tokens using the `swap_sol_for_token`
    method from the swapper and adds the swap quotation to the database using the `add_swap_quotation_to_db`
    method from MongoDB. It then constructs a dictionary containing the details of the swap quotation
    and returns it as a JSON response.

    ---
    tags:
      - Swap
    parameters:
      - in: body
        name: swap_request
        required: true
        schema:
          type: object
          properties:
            wallet:
              type: string
              description: The ID of the wallet initiating the swap.
            token:
              type: string
              description: The name of the token to receive in exchange for SOL.
            amount:
              type: number
              description: The amount of SOL to swap for tokens.
    responses:
      200:
        description: Returns a JSON response with the details of the swap quotation.
      400:
        description: Returns a JSON response with an error message if the request is not in JSON format.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    wallet_id = data['wallet']
    token_name = data['token']
    token_amount = data['amount']
    wallet = MongoDB.get_wallet_from_db(wallet_id)

    quotation = swapper.swap_sol_for_token(wallet, token_name, token_amount)
    MongoDB.add_swap_quotation_to_db(quotation)
    
    quotation_dict = {
        'wallet_address':quotation.wallet_address,
        'reference':quotation.reference,
        'token_name':quotation.token_name,
        'token_amount':quotation.token_amount,
        'sol_amount':quotation.sol_amount,
        'swap_occurred':quotation.swap_occurred,
        'timestamp':str(quotation.timestamp)
    }
    json_result = json.dumps(quotation_dict)
    return json_result

if __name__ == '__main__':
    app.run()