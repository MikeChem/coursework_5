# habits/tests.py
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Habit


class HabitAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        data = {
            "action": "Проснуться",
            "place": "Дом",
            "time": "08:00:00",
            "duration": 60,
            "frequency": 1,
            "is_public": True,
        }
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().action, "Проснуться")
