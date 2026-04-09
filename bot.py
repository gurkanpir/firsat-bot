import os
import re
import time
import requests
from statistics import median
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")

URLS = [
    "https://www.sahibinden.com/renault-clio",
    "https://www.sahibinden.com/fiat-egea",
    "https://www.sahibinden.com/toyota-corolla",
    "https://www.sahibinden.com/fiat-doblo",
    "https://www.sahibinden.com/fiat-fiorino",
    "https://www.sahibinden.com/volkswagen-polo",
    "https://www.sahibinden.com/skoda-fabia",
]

SEHIRLER = ["ordu", "giresun", "samsun", "trabzon", "rize", "gümüşhane"]

def create_driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)

driver = create_driver()

def telegram(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("TOKEN eksik")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def sayi(text):
    return int(re.sub(r"[^0-9]", "", text)) if text else 0

def km(text):
    m = re.search(r"(\d{2,3}(?:\.\d{3})+|\d{4,6})\s*km", text.lower())
    return sayi(m.group(1)) if m else 999999

def yil(text):
    y = re.findall(r"\b(20\d{2}|19\d{2})\b", text)
    return int(y[0]) if y else 0

def sehir_var(text):
    return any(s in text.lower() for s in SEHIRLER)

def ilanlari_cek(url):
    driver.get(url)
    time.sleep(5)
    items = driver.find_elements(By.CSS_SELECTOR, ".searchResultsItem")

    ilanlar = []
    for item in items[:40]:
        try:
            title = item.find_element(By.CSS_SELECTOR, ".classifiedTitle").text
            price = sayi(item.find_element(By.CSS_SELECTOR, ".classifiedPrice").text)
            link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
            detay = item.text.lower()

            ilanlar.append({
                "title": title,
                "price": price,
                "link": link,
                "detay": detay,
                "km": km(detay),
                "yil": yil(detay),
            })
        except:
            continue
    return ilanlar

def analiz(ilanlar):
    fiyatlar = [i["price"] for i in ilanlar if i["price"] > 0]
    if not fiyatlar:
        return []

    medyan = int(median(fiyatlar))
    sonuc = []

    for i in ilanlar:
        skor = 0
        fark = (medyan - i["price"]) / medyan if medyan else 0

        if fark > 0.15: skor += 40
        elif fark > 0.10: skor += 30
        elif fark > 0.05: skor += 20

        if i["km"] < 120000: skor += 20
        if i["yil"] >= 2020: skor += 20
        if not sehir_var(i["detay"]): skor -= 20
        if any(x in i["detay"] for x in ["hasar","pert","tramer","airbag"]): skor -= 30

        if skor >= 60:
            sonuc.append(i)

    return sonuc

def run():
    print("AKILLI SİSTEM BAŞLADI")
    while True:
        for url in URLS:
            try:
                ilanlar = ilanlari_cek(url)
                firsatlar = analiz(ilanlar)

                for i in firsatlar:
                    mesaj = f"🚀 FIRSAT\n{i['title']}\n💰 {i['price']} TL\n{i['link']}"
                    telegram(mesaj)

            except Exception as e:
                print("Hata:", e)

        time.sleep(300)

if __name__ == "__main__":
    run()
