import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from data import SimpleDataStore
from chat import ChatReadRetriveRead

load_dotenv()

openai_api_key=os.environ.get('OPENAI_API_KEY')
dataImpl = SimpleDataStore(csv="data/red_wines_filtered_with_embeddings.csv")
chatImpl = ChatReadRetriveRead(data_store=dataImpl, openai_api_key=openai_api_key)

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")

# The payload to this function should be a list of dictionaries contains user-assistant message pairs
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    payload = request.get_json()
    r = chatImpl.run(payload)
    return jsonify(r)

if __name__ == '__main__':
    app.run(debug=True)
