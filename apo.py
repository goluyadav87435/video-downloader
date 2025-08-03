from flask import Flask, request
from bot import handle_message

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    handle_message(data)
    return "OK", 200

@app.route('/', methods=['GET'])
def index():
    return "Telegram Video Bot is Running!", 200

if __name__ == '__main__':
    app.run()

