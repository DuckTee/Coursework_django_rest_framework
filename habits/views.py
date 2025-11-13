from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated
from habits.tasks import send_habit_reminder


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]  # Без авторизации
    queryset = Habit.objects.filter(is_public=True)

    @swagger_auto_schema(
        operation_description="Получить список публичных привычек",
        responses={200: HabitSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить детали публичной привычки",
        responses={200: HabitSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

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

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        # Запланировать напоминание через 1 час
        send_habit_reminder.apply_async(
            args=[instance.id],
            countdown=3600  # 1 час в секундах
        )

    @swagger_auto_schema(
        operation_description="Создать новую привычку",
        request_body=HabitSerializer,
        responses={201: HabitSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить список привычек текущего пользователя",
        responses={200: HabitSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить детали привычки",
        responses={200: HabitSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить привычку",
        request_body=HabitSerializer,
        responses={200: HabitSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично обновить привычку",
        request_body=HabitSerializer,
        responses={200: HabitSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить привычку",
        responses={204: 'No content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
