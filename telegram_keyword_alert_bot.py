from telethon.sync import TelegramClient, events
import re
from datetime import datetime

# === AYARLAR ===
api_id = 29120660  # Buraya kendi API ID'ni yaz
api_hash = 'a22e6c2850bc998882238f58bcfae60d'  # Buraya kendi API Hash'ini yaz
session_name = 'promo_session'  # .session dosyanın adı (uzantısı .session olacak)

# === ANAHTAR KELİMELER ===
KEYWORDS = ["KOD", "PROMO"]  # Büyük/küçük harfe duyarsız şekilde kontrol edilecek

# === TAKİP EDİLECEK KANALLAR ===
ALLOWED_CHANNELS = [
    "@kanal1",
    "@kanal2"
    # Buraya sadece takip edeceğin kanalları yaz
]

# === BOT BAŞLIYOR ===
client = TelegramClient(session_name, api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    chat = await event.get_chat()

    try:
        chat_username = f"@{chat.username}" if chat.username else None
        if chat_username not in ALLOWED_CHANNELS:
            return  # Bu kanal listede yoksa mesajı dikkate alma

        text = event.raw_text
        for keyword in KEYWORDS:
            if re.search(rf"\\b{keyword}\\b", text, re.IGNORECASE):
                msg = f"\ud83d\udce3 [ANAHTAR KELİME BULUNDU]\n\n" \
                      f"\ud83d\udccc Kanal: {chat_username}\n" \
                      f"\ud83d\udd50 Tarih: {datetime.now().strftime('%d.%m.%Y - %H:%M')}\n" \
                      f"\ud83d\udce8 Mesaj:\n{text}"
                await client.send_message("me", msg)  # "me" kendine mesaj gönderir
                break
    except Exception as e:
        print(f"Hata: {e}")

print("\u2728 Bot başlatılıyor...")
client.start()
client.run_until_disconnected()
