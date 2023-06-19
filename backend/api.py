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


def get_chat_keywords(history: list[dict], api_key: str) -> list[dict]:
    keyword_system_message = """Assistant is a sommelier that creates keywords from customer messages about wine. The keyword should help assistant understand what type of wine the customer is looking for.
Only generate keywords separated by commas, nothing else. ONLY generate keywords relevant for a wine suggestion.
"""

    keyword_system_message_sv = """Assistenten är en sommelier som skapar nyckelord från användarmeddelanden om vin. Nyckelorden ska hjälpa assistenten att förstå vilken typ av vin användaren letar efter.
Generera ENDAST nyckelord separerade med kommatecken, inget annat. Generera ENDAST nyckelord som är relevanta för ett vinförslag.
"""

    openai_model = "gpt-3.5-turbo"
    user_messages_deque = deque()
    for h in reversed(history):
        user_messages_deque.appendleft(
            {"role": "user", "content": h.get("question")})
    user_messages_deque.appendleft(
        {"role": "system", "content": keyword_system_message_sv})

    openai.api_key = api_key
    completion = openai.ChatCompletion.create(
        model=openai_model,
        messages=list(user_messages_deque)
    )
    return completion.choices[0].message


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.environ.get('OPENAI_API_KEY')
    c = [{
        "question": "I want a red wine.",
        "answer": "I can help you with that. However I need to understand your preferences better. Do yo like fruity wines?",
    }, {
        "question": "Yes a fruity wine sounds nice.",
        "answer": "Are you planning to eat something with the wine?",
    }, {
        "question": "We are going to eat lamb. Perhaps a wine from Italy."
    }]
    c_small = [{
        "question": "I want a red wine.",
        "answer": "I can help you with that. However I need to understand your preferences better. Do yo like fruity wines?",
    }]

    #k = get_chat_keywords(history=c_small, api_key=api_key)
    #print(k)
