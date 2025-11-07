from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated
from habits.tasks import send_habit_reminder
import logging  # Импорт модуля

# Инициализация логгера
logger = logging.getLogger(__name__)  # ← ЭТО НУЖНО ДОБАВИТЬ!


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Habit.objects.filter(is_public=True)


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Habit.objects.filter(
            user=self.request.user,
            user__is_active=True
        )

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)

        if instance.user.telegram_chat_id:
            send_habit_reminder.apply_async(
                args=[instance.id],
                countdown=3600
            )
            logger.info(  # Теперь работает!
                f"Создана привычка ID={instance.id}. "
                f"Напоминание запланировано для {instance.user.id}."
            )
        else:
            logger.warning(  # Теперь работает!
                f"У пользователя {instance.user.id} не указан telegram_chat_id. "
                "Напоминание не отправлено."
            )
