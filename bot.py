import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def telegram_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": mesaj})

def ilanlari_cek():
    url = "https://www.sahibinden.com/otomobil"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    return r.text

def kontrol_et():
    data = ilanlari_cek()
    
    if "Clio" in data or "Egea" in data or "Corolla" in data:
        telegram_gonder("🚗 FIRSAT ARAÇ BULUNDU! Sahibinden kontrol et!")

while True:
    try:
        kontrol_et()
        time.sleep(300)
    except Exception as e:
        print(e)
