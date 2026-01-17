from flask import Flask, request, jsonify
from producer import send_message
import random

app = Flask(__name__)

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    message = {
        "id": random.randint(1, 1000),
        "text": data.get("text", ""),
    }
    send_message("input-topic", message)
    return jsonify({"status": "ok", "message": message})

if __name__ == '__main__':
    app.run(port=5000)
