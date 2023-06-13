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

    system_message = """Assistant is a sommelier that suggests red wines to the customer. Be brief in your answers and suggestions.
Suggestions are ONLY allowed from the list of wines below. If there is not enough information below to make a wine suggestion, say you need more information to suggest. If asking a follow-up question to the user would help, ask the question.
Do not generate answers that do not use the wine list below.
{follow_up_questions_prompt}\n
Wines:
{sources}\n
"""

    follow_up_questions = """Generate three very brief follow-up questions that will help you make a wine suggestion. 
Use double angle brackets to reference the questions, e.g. <<Do you prefer bolder or lighter wines?>>.
Try not to repeat questions that have already been asked.
Politely let the user know you need some more information to make a suggestion.
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
            top_n_similar_string = top_n_similar_string + "Namn: " + t[0] + "; " + t[1] + "\n"
        log.info("Data retrieved from datastore: " + "\n" +  top_n_similar_string)

        # STEP 4 - Get wine recommendation or follow up questions. More advanced implementation could be to mimin ReAct paper, i.e. implement actions for to bot to take.
        self.system_message = self.system_message.format(
            sources=top_n_similar_string.strip(), follow_up_questions_prompt=self.follow_up_questions)

        messages = self.chat_history_chat_format(history)
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages)
        reply = completion["choices"][0]["message"]["content"]
        log.info("Assistant reply: " + "\n" + reply)

        # STEP 5 return response object
        # Response object should look like {answer: OpenAI text response, products: raw list of products fetched from datastore, search_keywords: key words used to search datastore)
        return {"answer": reply, "products": top_n_similar_string, "searchWords": chat_keywords["content"]}

    def chat_history_chat_format(self, history: list[dict], approx_max_tokens=1000):
        messages_deque = deque()
        for h in reversed(history):
            messages_deque.appendleft(
                {"role": "assistant", "content": h.get("answer") if h.get("answer") else ""})
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

    #chatImpl.run(h)
