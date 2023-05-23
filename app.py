from flask import Flask, request
import requests

app = Flask(__name__)

def search_products(params):
    # API endpoint
    url = "https://api-systembolaget.azure-api.net/sb-api-ecommerce/v1/productsearch/search"

    # Default query parameters
    default_params = {
        'page': '1',
        'size': '30',
        'sortBy': 'Score',
        'sortDirection': 'Ascending',
        'assortmentText': ['Fast sortiment', 'Tillfälligt sortiment'],
        'packagingLevel1': 'Flaska',
        'categoryLevel1': 'Vin',
        'categoryLevel2': 'Rött vin'
    }

    # Update default parameters with payload
    default_params.update(params)

    # Headers
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'cfc702aed3094c86b92d6d4ff7a54c84'
    }

    # Send GET request to the API endpoint with parameters and headers
    response = requests.get(url, params=default_params, headers=headers)

    # Print the status code
    print("Status Code:", response.status_code)

    # Get the products from the response JSON
    products = response.json().get('products', [])

    # Create a new list of products with only the required fields
    processed_products = []
    for product in products:
        processed_product = {
            'name': f"{product.get('productNameBold', '')}, {product.get('productNameThin', '')}",
            'country': product.get('country', ''),
            'customCategoryTitle': product.get('customCategoryTitle', ''),
            'usage': product.get('usage', ''),
            'taste': product.get('taste', ''),
            'grapes': product.get('grapes', ''),
            'tasteClockFruitacid': product.get('tasteClockFruitacid', ''),
            'tasteClockBody': product.get('tasteClockBody', ''),
            'tasteClockRoughness': product.get('tasteClockRoughness', ''),
        }
        processed_products.append(processed_product)

    return processed_products

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    payload = request.get_json()
    print(payload)
    products = search_products(payload)
    print(products)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
