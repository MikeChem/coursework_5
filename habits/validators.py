from django.core.exceptions import ValidationError


def validate_duration(value):
    if value > 120:
        raise ValidationError("Время выполнения не должно превышать 120 секунд.")


def validate_frequency(value):
    if value < 1 or value > 7:
        raise ValidationError("Периодичность должна быть от 1 до 7 дней.")
