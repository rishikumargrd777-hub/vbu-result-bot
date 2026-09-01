import os
import requests

url = f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": os.environ["CHAT_ID"],
        "text": "✅ Bot Test Successful!\n\nVBU Result Bot Telegram connection working."
    },
    timeout=30
)
