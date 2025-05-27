from rest_framework import serializers
from .models import Habit
from users.models import CustomUser


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')  # 👈 Теперь сериализуется без ошибок

    class Meta:
        model = Habit
        fields = [
            'id',
            'user',
            'place',
            'time',
            'action',
            'is_pleasant',
            'related_habit',
            'frequency',
            'reward',
            'duration',
            'is_public',
        ]

    def validate(self, data):
        # 1. Одновременное указание reward и related_habit
        if data.get("reward") and data.get("related_habit"):
            raise serializers.ValidationError({
                "reward": "Нельзя одновременно указывать вознаграждение и связанную привычку.",
                "related_habit": "Нельзя одновременно указывать вознаграждение и связанную привычку."
            })

        # 2. Приятная привычка не может иметь reward или related_habit
        if data.get("is_pleasant"):
            if data.get("reward") or data.get("related_habit"):
                raise serializers.ValidationError(
                    {"non_field_errors": ["Приятная привычка не может иметь вознаграждения или связанной привычки."]}
                )

        # 3. Связанная привычка должна быть приятной
        related = data.get("related_habit")
        if related and not related.is_pleasant:
            raise serializers.ValidationError({"related_habit": "Связанная привычка должна быть приятной."})

        return data