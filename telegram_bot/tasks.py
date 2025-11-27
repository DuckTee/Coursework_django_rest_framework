from celery import shared_task
from telegram import Bot
from django.conf import settings
from habits.models import Habit
from habits.views import logger


@shared_task
def send_habit_reminder(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
        if habit.user.telegram_chat_id:
            bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            message = f"⏰ Напоминание: {habit.action} в {habit.place}!"
            bot.send_message(chat_id=habit.user.telegram_chat_id, text=message)
    except Habit.DoesNotExist:
        logger.error(f"Привычка с ID {habit_id} не найдена")
    except Exception as e:
        logger.error(f"Ошибка отправки напоминания: {e}")
