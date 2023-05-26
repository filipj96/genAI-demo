import openai
from collections import deque
from api import systembolaget_search
import json


def mock_keywords():
    return ['rött vin', 'lamm']


class ChatReadRetriveRead():

    system_message = """Mock system message
{follow_up_questions_prompt}\n
Sources:
{sources}\n
"""

    def run(self, history: list[dict]):

        # Step 3(?) - Genereate keywords that can be used in search
        search_keywords = mock_keywords()

        # Step 4(?) - Search Systembolaget
        products = systembolaget_search(search_keywords)
        products = self.systemet_product_list_to_string([products[0]])
        self.system_message = self.system_message.format(sources=products, follow_up_questions_prompt="whatever")
        print(self.system_message)

        # Step 5(?) - Get wine recommendation or follow up questions
        #print(self.chat_history_chat_format(history))

    def chat_history_chat_format(self, history: list[dict], approx_max_tokens=1000):
        messages_deque = deque()
        for h in reversed(history):
            messages_deque.appendleft(
                {"role": "assistant", "content": h.get("answer")})
            messages_deque.appendleft(
                {"role": "user", "content": h.get("question")})
        messages_deque.appendleft(
            {"role": "system", "content": self.system_message})

        return list(messages_deque)

    def systemet_product_list_to_string(self, systemet_product_list: list[dict]) -> str:
        s = ""

        for product in systemet_product_list:
            for k, v in product.items():
                if type(v) is not str:
                    v = str(v)
                s = s + k + ": " + v + "\n"
            s = s + "-\n"
        return s


if __name__ == '__main__':
    chat = ChatReadRetriveRead()

    h = [{
        "question": "What's the weather like today?",
        "answer": "Answer to What's the weather like today?",
    }, {
        "question": "How about the weather for the next week?",
        "answer": "Answer to How about the weather for the next week?",
    }, {
        "question": "Today?",
        "answer": "Answer to Today?"
    }]

    p = [{
        "namn": "Maison Robert Olivier, Vin Naturel Cuvée Tradition",
        "land": "Frankrike",
        "druvor": "Merlot",
        "kategori": "Fruktigt & Smakrikt",
        "smak": "Fruktig smak med inslag av svarta vinbär, färska örter, skogshallon, viol och blåbär.",
        "passar till": "Lamm, Nöt, Grönsaker",
        "fruktsyra": 9,
        "fyllighet": 7,
        "strävhet": 7
    },
    {
        "namn": "Maison Robert Olivier, Vin Naturel Cuvée Tradition",
        "land": "Frankrike",
        "druvor": "Merlot",
        "kategori": "Fruktigt & Smakrikt",
        "smak": "Fruktig smak med inslag av svarta vinbär, färska örter, skogshallon, viol och blåbär.",
        "passar till": "Lamm, Nöt, Grönsaker",
        "fruktsyra": 9,
        "fyllighet": 7,
        "strävhet": 7
    }]

    #print(chat.chat_history_chat_format(h))
    #print(chat.systemet_product_list_to_string(p))
    chat.run(h)
