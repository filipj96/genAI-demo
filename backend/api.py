import requests

def systembolaget_search(keywords: list[str]):
    url = "https://api-systembolaget.azure-api.net/sb-api-ecommerce/v1/productsearch/search"
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'cfc702aed3094c86b92d6d4ff7a54c84'
    }
    
    # Default query parameters
    default_params = {
        'page': '1',
        'size': '30',
        'sortBy': 'Score',
        'sortDirection': 'Ascending',
        'assortmentText': ['Fast sortiment', 'Tillfälligt sortiment'],
        'packagingLevel1': 'Flaska',
        'categoryLevel1': 'Vin',
        'categoryLevel2': 'Rött vin',
        'price.min': '90',
        'price.max': '150'
    }

    # Adding the keywords as parameter to API call
    textQuery = ' '.join(keywords)
    default_params.update({"textQuery": textQuery})

    response = requests.get(url, params=default_params, headers=headers)
    products = response.json().get('products', [])

    processed_products = []
    for product in products:
        processed_product = {
            'namn': f"{product.get('productNameBold', '')}, {product.get('productNameThin', '')}",
            'land': product.get('country', ''),
            'druvor': ', '.join(product.get('grapes', '')),
            'kategori': product.get('categoryLevel3', ''),
            'smak': product.get('taste', ''),
            'passar till': ', '.join(product.get('tasteSymbols', '')),
            'fruktsyra': product.get('tasteClockFruitacid', ''),
            'fyllighet': product.get('tasteClockBody', ''),
            'strävhet': product.get('tasteClockRoughness', ''),
        }
        processed_products.append(processed_product)
    
    return processed_products

if __name__ == '__main__':
    systembolaget_search(['rött vin', 'lamm'])