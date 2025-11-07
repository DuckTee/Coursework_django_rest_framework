from rest_framework import serializers
from .models import Habit
from user.models import User

class HabitSerializer(serializers.ModelSerializer):
    # Поле для отображения имени пользователя (опционально)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id',
            'user',
            'user_name',
            'place',
            'time',
            'action',
            'is_pleasant',
            'related_habit',
            'periodicity',
            'reward',
            'execution_time',
            'is_public'
        ]
        # Укажите поля, которые нельзя изменять через API (например, user)
        read_only_fields = ['user']

    def validate(self, data):
        # Повторная валидация бизнес‑правил (дублирует clean() модели)
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError(
                'Нельзя указать одновременно вознаграждение и связанную привычку.'
            )
        if data.get('execution_time') > 120:
            raise serializers.ValidationError(
                'Время выполнения не может превышать 120 секунд.'
            )
        if not (1 <= data.get('periodicity', 0) <= 7):
            raise serializers.ValidationError(
                'Периодичность должна быть от 1 до 7 дней.'
            )
        if data.get('is_pleasant') and (data.get('reward') or data.get('related_habit')):
            raise serializers.ValidationError(
                'Приятная привычка не может иметь вознаграждения или связанной привычки.'
            )
        return data
