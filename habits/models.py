from django.db import models
from django.core.exceptions import ValidationError
from user.models import User


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=100, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.TextField(verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_pleasant": True},
        verbose_name="Связанная приятная привычка",
        help_text="Выберите приятную привычку, которая будет вознаграждением",
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность (дни)",
        help_text="Сколько дней между выполнениями (1–7)",
    )
    reward = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Вознаграждение",
        help_text="Что вы получите за выполнение (если нет связанной привычки)",
    )
    execution_time = models.PositiveIntegerField(
        verbose_name="Время на выполнение (сек)", help_text="Не более 120 секунд"
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичная привычка",
        help_text="Если включено, привычка будет видна другим пользователям",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.action} в {self.place}"

    def clean(self):
        # 1. Либо вознаграждение, либо связанная привычка
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя указать одновременно вознаграждение и связанную привычку."
            )

        # 2. Время выполнения ≤ 120 сек
        if self.execution_time > 120:
            raise ValidationError("Время выполнения не может превышать 120 секунд.")

        # 3. Периодичность 1–7 дней
        if not (1 <= self.periodicity <= 7):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")

        # 4. Для приятных привычек: нет вознаграждения/связанной привычки
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "Приятная привычка не может иметь вознаграждения или связанной привычки."
            )
