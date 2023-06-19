import sys
import logging
import openai
from openai.embeddings_utils import get_embedding
from collections import deque
from api import get_chat_keywords

# Logging configuration
log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s %(name)s : %(message)s'))
log.addHandler(handler)
log.setLevel(logging.INFO)


class ChatReadRetriveRead():

    def __init__(self, data_store, openai_api_key):
        self.data_store = data_store
        self.api_key = openai_api_key
        self.embedding_model = "text-embedding-ada-002"

    system_message = """Assistant is a sommelier that suggests red wines to the user. Be brief in your answers and suggestions. Suggestions are ONLY allowed from the list of wines below. Assistant is NEVER allowed to suggest wines that are not in the provided list of wines. Assistant needs at least three user preferences to make a personal wine suggestion. If there is not enough information provided by the user for assistant to make a personal wine suggestion, do not make any suggestion. Instead say you need more information to make a suggestion and ask a follow-up question. When assistant does suggest a wine/s, it is enough to give the name of the wines. When assistant asks follow-up questions use the following guidelines:
Generate three very brief follow-up questions that will help you make a wine suggestion. 
Use double angle brackets to reference the questions, e.g. <<Do you prefer bolder or lighter wines?>>.
Try not to repeat questions that have already been asked.
Politely let the user know you need some more information to make a suggestion.

<wines>
{sources}\n
</wines>
"""

    system_message_sv = """Du är en sommelier och ska ge vinrekommendationer baserat på användarens input. Du måste följa dessa steg för att ge rekommendation till användaren:

Steg 1. Förstå vilka preferenser användaren har för vinet baserat på användarens meddelanden.

Steg 2. Du behöver minst tre stycken användarpreferenser för vin för att ge en rekommendation. Får du mindre än tre preferenser ska du ställa följdfrågor tills du har tillräckligt med information. Använda riktlinjerna för följdfråg i Steg 3.

Steg 3. Riktlinjer för följdfrågor: De ska vara vänliga och kortfattade. Försök att inte upprepa frågor som redan har ställts.

Steg 4. Om du vet tillräckligt om användarens vinpreferenser så rekommenderar du ett eller två viner till användaren. Du får ENDAST ge vinrekommendationer utifrån vinlistan som bifogas i chatten (avgränsas med XML-taggar).

<viner>
{sources}\n
</viner>
"""

    system_message_en = """You are a sommelier and you will give wine recommendations based on the user's input. You must follow these steps to give a recommendation to the user:

Step 1. Understand the user's wine preferences based on the user's messages.
Step 2. You need at least three user wine preferences to give a recommendation. If you receive fewer than three preferences, you should ask follow-up questions until you have 
        enough information. Use the guidelines for follow-up questions in Step 3.
Step 3. Guidelines for follow-up questions: They should be friendly and concise. Try not to repeat questions that have already been asked.
Step 4. If you know enough about the user's wine preferences, you recommend one or two wines to the user. You may ONLY give wine recommendations based on the wine list attached 
        in the chat (delimited with XML tags).

<wines>
{sources}\n
</wines>
"""

    def run(self, history: list[dict]):
        openai.api_key = self.api_key

        # STEP 1 - Generate keywords from the user chat messages, this should capture what the user wants
        chat_keywords: list[dict] = get_chat_keywords(
            history=history, api_key=self.api_key)
        log.info("Chat keywords retrieved: %s", chat_keywords["content"])

        # STEP 2 - Get embeddings for the keywords. This should probably be cached to save money.
        keyword_embedding: list[float] = get_embedding(
            chat_keywords["content"], engine=self.embedding_model)

        # STEP 3 - Get wine data from vector database based on vector similarity
        top_n_similar = self.data_store.search(
            embedding=keyword_embedding, n=10)

        top_n_similar_string = ""
        for t in top_n_similar:
            top_n_similar_string = top_n_similar_string + \
                "Namn: " + t[0] + "; " + t[1] + "\n"
        log.info("Data retrieved from datastore: " +
                 "\n" + top_n_similar_string)

        # STEP 4 - Get wine recommendation or follow up questions. More advanced implementation could be to mimin ReAct paper, i.e. implement actions for to bot to take.
        system_message_formated = self.system_message_sv.format(
            sources=top_n_similar_string.strip())

        messages = self.chat_history_chat_format(
            history, sys_message=system_message_formated)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages, temperature=0.5)
        reply = completion["choices"][0]["message"]["content"]
        log.info("Assistant reply: " + "\n" + reply)
        print(messages)

        # STEP 5 return response object
        # Response object should look like {answer: OpenAI text response, products: raw list of products fetched from datastore, search_keywords: key words used to search datastore)
        return {"answer": reply, "products": top_n_similar_string, "searchWords": chat_keywords["content"]}

    def chat_history_chat_format(self, history: list[dict], sys_message: str, approx_max_tokens=1000):
        messages_deque = deque()
        for h in reversed(history):
            messages_deque.appendleft(
                {"role": "assistant", "content": h.get("answer") if h.get("answer") else ""})
            messages_deque.appendleft(
                {"role": "user", "content": h.get("question")})
        messages_deque.appendleft(
            {"role": "system", "content": sys_message})

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
    import os
    from dotenv import load_dotenv
    from data import SimpleDataStore

    load_dotenv()

    openai_api_key = os.environ.get('OPENAI_API_KEY')
    dataImpl = SimpleDataStore(
        csv="data/red_wines_filtered_with_embeddings.csv")
    chatImpl = ChatReadRetriveRead(
        data_store=dataImpl, openai_api_key=openai_api_key)

    h = [{
        "question": "I want a red wine.",
        "answer": "I can help you with that. However I need to understand your preferences better. Do yo like fruity wines?",
    }, {
        "question": "Yes a fruity wine sounds nice.",
        "answer": "Are you planning to eat something with the wine?",
    }, {
        "question": "We are going to eat lamb. Perhaps a wine from Italy."
    }]

    # chatImpl.run(h)
