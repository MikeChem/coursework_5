import os
from celery import Celery
from django.conf import settings

# Установи стандартные настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('habit_tracker')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживай задачи в файлах tasks.py
app.autodiscover_tasks()