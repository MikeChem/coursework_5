from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from habits.models import Habit
from habits.validators import validate_duration, validate_frequency
from django.core.exceptions import ValidationError


class HabitViewSetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123'
        )

        # Получаем токен
        login_url = reverse('login')
        login_data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(login_url, login_data, format='json')
        self.token = response.data['access']

        # Устанавливаем заголовок авторизации
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.habit_data = {
            'action': 'Выпить воду',
            'time': '10:00',
            'place': 'Дом',
            'duration': 60,
            'frequency': 1
        }

    def test_create_habit(self):
        url = reverse('habit-list')
        response = self.client.post(url, self.habit_data, format='json')

        print(response.data)  # 👈 Выведет ошибки валидации

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().user, self.user)

    def test_get_own_habits(self):
        Habit.objects.create(user=self.user, action='Бег', time='09:00', place='Парк', duration=120, frequency=2)
        url = reverse('habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_cannot_see_other_users_habits(self):
        other_user = User.objects.create_user(username='other', password='password123')
        Habit.objects.create(user=other_user, action='Медитация', time='08:00', place='Офис', duration=90, frequency=3)

        url = reverse('habit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_update_habit(self):
        habit = Habit.objects.create(
            user=self.user, action='Чтение', time='12:00', place='Библиотека', duration=120, frequency=4
        )
        url = reverse('habit-detail', args=[habit.id])
        updated_data = {**self.habit_data, 'action': 'Обновлённая привычка'}
        response = self.client.put(url, updated_data, format='json')

        print(response.data)  # 👈 Выведет ошибки валидации

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, 'Обновлённая привычка')

    def test_delete_habit(self):
        habit = Habit.objects.create(user=self.user, action='Спорт', time='07:00', place='Зал', duration=60, frequency=5)
        url = reverse('habit-detail', args=[habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)


# === Тесты для валидаторов ===
class TestHabitValidators(APITestCase):

    def test_validate_duration_valid(self):
        validate_duration(120)  # Должно пройти без ошибок
        with self.assertRaises(ValidationError):
            validate_duration(121)

    def test_validate_frequency_valid(self):
        validate_frequency(1)  # OK
        validate_frequency(7)  # OK
        with self.assertRaises(ValidationError):
            validate_frequency(0)
        with self.assertRaises(ValidationError):
            validate_frequency(8)