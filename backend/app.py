from flask import Flask, request, jsonify
from chat import ChatReadRetriveRead

chatImpl = ChatReadRetriveRead

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    payload = request.get_json()
    print(payload)
    r = chatImpl.run()
    return jsonify(r)

if __name__ == '__main__':
    app.run(debug=True)
