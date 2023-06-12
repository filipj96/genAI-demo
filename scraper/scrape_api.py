import csv
import requests


def systembolaget_search():
    url = "https://api-systembolaget.azure-api.net/sb-api-ecommerce/v1/productsearch/search"
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'cfc702aed3094c86b92d6d4ff7a54c84'
    }

    current_page = 1
    default_params = {
        'page': str(current_page),
        'size': '30',
        'sortBy': 'Score',
        'sortDirection': 'Ascending',
        'assortmentText': ['Fast sortiment', 'Tillfälligt sortiment'],
        'packagingLevel1': 'Flaska',
        'packagingLevel2': 'Glasflaska',
        'categoryLevel1': 'Vin',
        'categoryLevel2': 'Rött vin',
        'price.min': '90',
        'price.max': '150'
    }

    processed_products = []
    while current_page > 0:
        response = requests.get(url, params=default_params, headers=headers)
        products = response.json().get('products', [])
        current_page = response.json().get('metadata').get('nextPage')
        default_params['page'] = current_page

        for product in products:
            grapes = ""
            if len(product.get('grapes')) > 0:
                grapes = ', '.join(product.get('grapes'))


            processed_product = {
                'name': f"{product.get('productNameBold', '')}, {product.get('productNameThin', '')}",
                'country': product.get('country', ''),
                'grapes': grapes,
                'category': product.get('categoryLevel3', ''),
                'taste': product.get('taste', ''),
                'usage': product.get('usage', ''),
                'pairing': ', '.join(product.get('tasteSymbols', '')),
                'fruitacid': product.get('tasteClockFruitacid', ''),
                'body': product.get('tasteClockBody', ''),
                'roughness': product.get('tasteClockRoughness', ''),
            }
            if processed_product['taste']:
                processed_product['taste'] = processed_product['taste'].strip()

            processed_products.append(processed_product)

    filename = "red_wines.csv"
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['name', 'country', 'grapes', 'category', 'taste',
                      'usage', 'pairing', 'fruitacid', 'body', 'roughness']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for dict in processed_products:
            writer.writerow(dict)


if __name__ == '__main__':
    systembolaget_search()
