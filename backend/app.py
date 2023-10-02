import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from data import SimpleDataStore
from chat import ChatReadRetriveRead

lang = ""
if len(sys.argv) > 1 and sys.argv[1] == "se":
    lang = "se"
else:
    lang = "en"

load_dotenv()

openai_api_key=os.environ.get('OPENAI_API_KEY')
dataImpl = SimpleDataStore(csv="data/red_wines_filtered_with_embeddings.csv")
chatImpl = ChatReadRetriveRead(data_store=dataImpl, openai_api_key=openai_api_key, lang=lang)

app = Flask(__name__)

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file(path)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    payload: dict = request.get_json()
    r = chatImpl.run(payload["history"])
    return jsonify(r)

if __name__ == '__main__':
    app.run(debug=True)
