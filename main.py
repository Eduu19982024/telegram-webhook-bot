from flask import Flask, request
import requests

app = Flask(__name__)

telegram_token = "8118228816:AAFx0wjs9eZqwwzHiNqPWrRAmuxG1JVQObI"
telegram_chat_ids = ["7686102175"]

def send_telegram_message(message):
    for chat_id in telegram_chat_ids:
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, data=payload)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return "Invalid payload", 400

    alert_type = data.get("type")
    ticker = data.get("ticker")
    price = data.get("price")
    time = data.get("time")

    if alert_type == "buy":
        message = f"🚀 *BUY SIGNAL* for *{ticker}*\nPrice: ₹{price}\nTime: {time}"
    elif alert_type == "stoploss":
        message = f"🔻 *STOPLOSS HIT* for *{ticker}*\nPrice: ₹{price}\nTime: {time}"
    else:
        message = f"⚠️ Unknown alert type received.\n\nData: `{data}`"

    send_telegram_message(message)
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "✅ Webhook is Live!", 200

if __name__ == "__main__":
    app.run(debug=True)
