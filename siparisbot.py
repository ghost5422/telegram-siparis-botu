import requests
import time

FIREBASE_URL = "https://onlinesiparis-2cf91-default-rtdb.europe-west1.firebasedatabase.app/orders.json"
TELEGRAM_TOKEN = "8125878519:AAFyTh0zwt7pfQeALhVUmL_ejbwWNxFGyuk"
CHAT_ID = "1642514642"

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
