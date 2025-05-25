import os

import requests
from celery import shared_task
from dotenv import load_dotenv

from .models import Habit

# Загружаем переменные окружения из .env файла
load_dotenv()


@shared_task(name="habits.tasks.send_telegram_reminder")
def send_telegram_reminder(habit_id):
    """
    Отправляет напоминание о привычке через Telegram.

    :param habit_id: ID привычки, о которой нужно напомнить
    :return: dict — результат выполнения запроса или сообщение об ошибке
    """
    try:
        # Получаем привычку по ID
        habit = Habit.objects.get(id=habit_id)

        # Получаем данные из переменных окружения
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not bot_token or not chat_id:
            raise ValueError("Не заданы TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID")

        # Формируем сообщение
        message = f"⏰ Напоминание! Вы должны: {habit.action} в {habit.time} в {habit.place}."

        # URL для отправки сообщения
        url = f"https://api.telegram.org/bot {bot_token}/sendMessage"
        data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}

        # Отправляем запрос
        response = requests.post(url, data=data)
        result = response.json()

        # Логируем успех
        print(f"[INFO] Reminder sent for habit ID={habit_id}. Response: {result}")
        return result

    except Habit.DoesNotExist:
        print(f"[ERROR] Привычка с ID={habit_id} не найдена.")
        return {"error": f"Habit with ID={habit_id} does not exist."}

    except Exception as e:
        print(f"[ERROR] Ошибка при отправке напоминания: {e}")
        return {"error": str(e)}
