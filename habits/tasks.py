from celery import shared_task
import requests
import os
from dotenv import load_dotenv
from .models import Habit


load_dotenv()


@shared_task
def send_telegram_reminder(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")

        message = f"⏰ Напоминание! {habit.action} в {habit.time} в {habit.place}."
        url = f"https://api.telegram.org/bot {bot_token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        requests.post(url, data=data)
    except Habit.DoesNotExist:
        pass