from flask import Flask, jsonify, request
from flasgger import Swagger
import requests
import json

app = Flask(__name__)
swagger = Swagger(app, template={
    "info": {
        "title": "Portfolio Endpoints",
        "description": "Endpoints for updating the portfolio"
    }
})

base_url = "https://api.dexscreener.com/latest/dex/pairs/solana/"
solana_url = "https://api.dexscreener.com/latest/dex/pairs/bsc/0x1e4600929edf7f36b4a7eac4c7571057d82a246c"

token_urls = {
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

@app.route('/token', methods=['POST'])
def get_price():
    """
     Retrieve the price and 24-hour price change for a given token.

    This function expects a JSON request containing a 'token' parameter.
    If the request is not in JSON format, it returns a JSON response with
    an error message and status code 400.

    ---
    tags:
      - Token
    parameters:
      - in: body
        name: token
        required: true
        schema:
          type: object
          properties:
            token:
              type: string
              description: Token name
    responses:
      200:
        description: Returns token price and 24-hour price change.
      400:
        description: Request must be JSON or token not found.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    token = data['token']

    if token == 'SOL':
        response = requests.post(solana_url)
    else:
        token_url = token_urls[token]
        response = requests.post(base_url + token_url)
    response = response.json()

    price_change_24h = response['pair']['priceChange']['h24']
    price_usd = response['pair']['priceUsd']

    result = {
        "price": price_usd,
        "price_change": price_change_24h
    }

    json_result = json.dumps(result)
    return json_result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
