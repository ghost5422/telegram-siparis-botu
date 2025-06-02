import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

@app.route("/", methods=["GET"])
def home():
    return "Telegram Bot Aktif ✅"

@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    if not data:
        return {"error": "Veri yok"}, 400

    # Örnek veri: { "name": "Berkay", "order": "1x Netflix, 1x Disney+", "total": "120₺" }
    name = data.get("name", "İsimsiz")
    order = data.get("order", "Sipariş yok")
    total = data.get("total", "0₺")

    message = f"📦 <b>Yeni Sipariş!</b>\n👤 Müşteri: {name}\n🛍 Ürünler: {order}\n💳 Tutar: {total}"
    send_telegram_message(message)

    return {"status": "Gönderildi"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
