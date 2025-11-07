from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    # Валидатор: только цифры, допускается минус (для групповых чатов)
    telegram_id_validator = RegexValidator(
        regex=r'^-?\d+$',
        message='Telegram ID должен содержать только цифры (минус допускается для групп).'
    )

    telegram_chat_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True,
        validators=[telegram_id_validator],
        verbose_name='Telegram Chat ID',
        help_text='Введите ID чата Telegram (например, 123456789 или -100123456789)'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # Индекс для ускорения поиска
        indexes = [
            models.Index(fields=['telegram_chat_id'])
        ]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Очищаем пробелы перед сохранением
        if self.telegram_chat_id:
            self.telegram_chat_id = self.telegram_chat_id.strip()
        super().save(*args, **kwargs)