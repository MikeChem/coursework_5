from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_pleasant": True},
        verbose_name="Связанная привычка",
    )
    frequency = models.PositiveIntegerField(default=1, verbose_name="Периодичность (в днях)")
    reward = models.TextField(null=True, blank=True, verbose_name="Вознаграждение")
    duration = models.PositiveIntegerField(verbose_name="Время на выполнение (секунды)")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    def clean(self):
        # 1. Нельзя указывать одновременно вознаграждение и связанную привычку
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя указывать одновременно вознаграждение и связанную привычку.")

        # 2. У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

        # 3. Время выполнения не больше 120 секунд
        if self.duration > 120:
            raise ValidationError("Время выполнения должно быть не больше 120 секунд.")

        # 4. Периодичность не реже 7 дней
        if self.frequency < 1 or self.frequency > 7:
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.action}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
