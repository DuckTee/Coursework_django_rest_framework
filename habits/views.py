from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated
from habits.tasks import send_habit_reminder


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]  # Без авторизации
    queryset = Habit.objects.filter(is_public=True)

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]  # Только для авторизованных

    def get_queryset(self):
        # Возвращаем только привычки текущего пользователя
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        # Запланировать напоминание через 1 час
        send_habit_reminder.apply_async(
            args=[instance.id],
            countdown=3600  # 1 час в секундах
        )
