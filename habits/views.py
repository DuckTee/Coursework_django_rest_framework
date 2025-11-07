from rest_framework import viewsets
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]  # Только для авторизованных

    def get_queryset(self):
        # Возвращаем только привычки текущего пользователя
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Автоматически присваиваем пользователя при создании
        serializer.save(user=self.request.user)
