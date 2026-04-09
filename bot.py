import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
resp = requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": "TEST MESAJI ✅"
})

print(resp.status_code)
print(resp.text)
