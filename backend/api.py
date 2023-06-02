import os
import requests
from collections import deque
import openai

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


def get_keywords(history: list[dict], api_key: str = os.getenv("OPENAI_API_KEY")) -> list[str]:
    # Works OK but not tested thoroughly
    system_message = """Assistant is a sommelier that creates keywords from customer messages about wine.
Only generate keywords separated by commas, nothing else. ONLY generate keywords relevant for a wine suggestion. Absolutely NOT any words that cannot be useful for a wine recommendation.
Generate no more than 5 keywords.
"""

    messages_deque = deque()
    for h in reversed(history):
        messages_deque.appendleft(
            {"role": "user", "content": h.get("question")})
    messages_deque.appendleft(
        {"role": "system", "content": system_message})

    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_deque
    )
    print(completion.choices[0].message)

    return list(messages_deque)


if __name__ == '__main__':
    print("api.py")
    # systembolaget_search(['rött vin', 'lamm'])

    """ h = [{
        "question": "What's the weather like today?",
        "answer": "Answer to What's the weather like today?",
    }, {
        "question": "How about the weather for the next week?",
        "answer": "Answer to How about the weather for the next week?",
    }, {
        "question": "Today?",
        "answer": "Answer to Today?"
    }]
    print(get_keywords(h)) """
