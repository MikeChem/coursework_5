from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser as User
from habits.models import Habit


class HabitViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Получаем токен
        login_url = reverse("login")
        login_data = {"username": "testuser", "password": "password123"}
        response = self.client.post(login_url, login_data, format="json")
        self.token = response.data["access"]

        # Устанавливаем заголовок авторизации
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        self.habit_data = {
            "action": "Выпить воду",
            "time": "10:00",
            "place": "Дом",
            "duration": 60,
            "frequency": 1,
        }

    def test_create_habit(self):
        url = reverse("habit-list")
        response = self.client.post(url, self.habit_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().user, self.user)

    def test_get_own_habits(self):
        Habit.objects.create(user=self.user, action="Бег", time="09:00", place="Парк", duration=120, frequency=2)
        url = reverse("habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_cannot_see_other_users_habits(self):
        other_user = User.objects.create_user(username="other_unique_user", password="password123")
        Habit.objects.create(user=other_user, action="Медитация", time="08:00", place="Офис", duration=90, frequency=3)
        url = reverse("habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_update_habit(self):
        habit = Habit.objects.create(
            user=self.user, action="Чтение", time="12:00", place="Библиотека", duration=120, frequency=4
        )
        url = reverse("habit-detail", args=[habit.id])
        updated_data = {**self.habit_data, "action": "Обновлённая привычка"}
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, "Обновлённая привычка")

    def test_delete_habit(self):
        habit = Habit.objects.create(
            user=self.user, action="Спорт", time="07:00", place="Зал", duration=60, frequency=5
        )
        url = reverse("habit-detail", args=[habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)


class TestAccessPermissions(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.other_user = User.objects.create_user(username="other_unique_user", password="password123")
        self.habit = Habit.objects.create(
            user=self.other_user,
            action="Привычка другого пользователя",
            time="09:00",
            place="Работа",
            duration=60,
            frequency=1,
        )

        # Логинимся как testuser
        login_url = reverse("login")
        login_data = {"username": "testuser", "password": "password123"}
        response = self.client.post(login_url, login_data, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_cannot_edit_others_habit(self):
        url = reverse("habit-detail", args=[self.habit.id])
        updated_data = {
            "action": "Изменённая привычка",
            "time": "10:00",
            "place": "Дом",
            "duration": 60,
            "frequency": 1,
        }
        response = self.client.put(url, updated_data, format="json")

        # 👇 Меняем ожидание на 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_delete_others_habit(self):
        url = reverse("habit-detail", args=[self.habit.id])
        response = self.client.delete(url)

        # 👇 Меняем ожидание на 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)