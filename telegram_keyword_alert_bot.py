from telethon.sync import TelegramClient, events
import re
from datetime import datetime
import requests
import os

# === TELEGRAM API BİLGİLERİ ===
api_id = int(os.environ['API_ID'])  # Railway'de ortam değişkeninden okunacak
api_hash = os.environ['API_HASH']
session_name = 'promo_session'

# === TELEGRAM BOT BİLGİLERİ ===
bot_token = os.environ['BOT_TOKEN']
chat_id = int(os.environ['CHAT_ID'])

# === ANAHTAR KELİMELER ===
KEYWORDS = ["KOD", "PROMO"]

# === TAKİP EDİLECEK KANALLAR ===
ALLOWED_CHANNELS = [
    "@zbahis_com",
    "@zbahiscom",
    "@otobetcom",
    "@betkomtelegram",
    "@resmibetine",
    "@grandpashagir",
    "@TarafbetDuyuru",
    "@casinoroyalcom",
    "@asyaresmi",
    "@maltresmi",
    "@bahiscomtg",
    "@dumanresmi",
    "@fixofficial",
    "@matadorbetresmi",
    "@betpublicofficial",
    "@supertotobet_official",
    "@padisah_sosyal",
]

# === TELETHON CLIENT ===
client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    try:
        chat_username = f"@{chat.username}" if chat.username else None
        if chat_username not in ALLOWED_CHANNELS:
            return

        text = event.raw_text
        for keyword in KEYWORDS:
            if re.search(rf"\b{keyword}\b", text, re.IGNORECASE):
                msg = f"📣 [ANAHTAR KELİME BULUNDU]\n\n" \
                      f"📌 Kanal: {chat_username}\n" \
                      f"🕐 Tarih: {datetime.now().strftime('%d.%m.%Y - %H:%M')}\n" \
                      f"📨 Mesaj:\n{text}"
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    data={"chat_id": chat_id, "text": msg}
                )
                break
    except Exception as e:
        print(f"Hata: {e}")

async def on_start():
    requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        data={"chat_id": chat_id, "text": "🚀 Bot Railway'de başlatıldı. Kanal dinlemesi aktif."}
    )

async def on_stop():
    requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        data={"chat_id": chat_id, "text": "⛔️ Bot durduruluyor. Kanal dinlemesi sona erdi."}
    )

print("✨ Bot başlatılıyor...")

with client:
    client.loop.run_until_complete(on_start())
    try:
        client.run_until_disconnected()
    finally:
        client.loop.run_until_complete(on_stop())
