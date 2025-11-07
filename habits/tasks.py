from celery import shared_task
from django.core.mail import send_mail
from .models import Habit

@shared_task
def send_habit_reminder(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
        if habit.user.email:
            send_mail(
                subject=f'Напоминание: {habit.action}',
                message=f'Сегодня в {habit.time} вам нужно выполнить: {habit.action} в {habit.place}.',
                from_email='no-reply@habit-tracker.com',
                recipient_list=[habit.user.email],
            )
    except Habit.DoesNotExist:
        pass  # Задача игнорируется, если привычка удалена
