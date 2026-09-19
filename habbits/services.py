import requests
from django.conf import settings


def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message,
    }

    response = requests.post(url, json=data)

    return response.json()
