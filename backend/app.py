from flask import Flask, request

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    payload = request.get_json()
    print(payload)

    # Step 5(?) - Chat with assistant
    r = chatImpl.run()

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
