from rest_framework import serializers
from habits.models import Habit
from django.core.exceptions import ValidationError


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

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
            'is_public'
        ]

    def validate(self, data):
        # 1. Нельзя указывать reward и related_habit одновременно
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError({
                'reward': 'Нельзя одновременно указывать "reward" и "related_habit".',
                'related_habit': 'Нельзя одновременно указывать "reward" и "related_habit".'
            })

        # 2. Приятная привычка не может иметь reward или related_habit
        if data.get('is_pleasant'):
            if data.get('reward') or data.get('related_habit'):
                raise serializers.ValidationError({
                    'non_field_errors': 'Приятная привычка не может иметь "reward" или "related_habit".'
                })

        # 3. Связанная привычка должна быть приятной
        related = data.get('related_habit')
        if related and not related.is_pleasant:
            raise serializers.ValidationError({
                'related_habit': 'Связанная привычка должна быть приятной.'
            })

        return data