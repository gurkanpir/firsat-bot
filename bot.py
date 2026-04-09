import os
import requests
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": mesaj
    }, timeout=20)
    print("STATUS:", r.status_code)
    print("BODY:", r.text)

print("BOT BASLADI")
print("BOT_TOKEN VAR MI:", bool(BOT_TOKEN))
print("CHAT_ID:", CHAT_ID)

gonder("TEST MESAJI ✅ Telegram hattı çalışıyor")

while True:
    time.sleep(60)
