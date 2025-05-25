import requests
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получаем данные из .env
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

# Проверяем, что все данные получены
if not bot_token or not chat_id:
    print("❌ Не хватает TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID в .env")
else:
    # Отправляем сообщение
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": "Привет! Это Django шлёт тебе привет из курсового проекта!"}
    response = requests.post(url, data=data)

    print("Отправлено в Telegram:")
    print("URL:", url)
    print("Data:", data)
    print("Ответ от Telegram:", response.json())