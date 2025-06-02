import os
import requests
import time
from keep_alive import keep_alive

keep_alive()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FIREBASE_URL = os.getenv("FIREBASE_URL")

seen = set()

while True:
    try:
        response = requests.get(FIREBASE_URL)
        data = response.json()
        for key, order in data.items():
            if key not in seen:
                seen.add(key)
                items = "\n".join([f"- {i['name']} x{i['quantity']} = ₺{i['price']*i['quantity']}" for i in order.get("items", [])])
                total = sum(i['price'] * i['quantity'] for i in order.get("items", []))
                text = f"""📦 Yeni Sipariş
👤 {order['name']}
📞 {order['phone']}
📝 {order.get('note', '')}
{items}
💰 Toplam: ₺{total}
🕒 {order.get('date', '')}"""
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={
                    "chat_id": CHAT_ID,
                    "text": text
                })
        time.sleep(10)
    except Exception as e:
        print("Hata:", e)
        time.sleep(10)
