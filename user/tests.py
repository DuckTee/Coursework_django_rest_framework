from django.test import TestCase
from django.core.exceptions import ValidationError
from user.models import User


class UserModelTest(TestCase):
    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")

    def test_create_user(self):
        """Тест: создание пользователя"""
        user = User.objects.get(username="testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertFalse(user.is_superuser)

    def test_telegram_chat_id_save(self):
        """Тест: сохранение корректного Telegram Chat ID"""
        self.user.telegram_chat_id = "123456789"
        self.user.save()

        updated_user = User.objects.get(username="testuser")
        self.assertEqual(updated_user.telegram_chat_id, "123456789")

    def test_telegram_id_with_minus(self):
        """Тест: ID группы (с минусом)"""
        self.user.telegram_chat_id = "-100123456789"
        self.user.save()

        updated_user = User.objects.get(username="testuser")
        self.assertEqual(updated_user.telegram_chat_id, "-100123456789")

    def test_invalid_telegram_id_letters(self):
        """Тест: ошибка при буквенном ID"""
        self.user.telegram_chat_id = "abc123"
        with self.assertRaises(ValidationError):
            self.user.full_clean()  # Запускает валидацию

    def test_invalid_telegram_id_empty(self):
        """Тест: пустое значение (допустимо, так как blank=True)"""
        self.user.telegram_chat_id = ""
        self.user.full_clean()  # Не должно вызвать ошибку
        self.user.save()

        updated_user = User.objects.get(username="testuser")
        self.assertEqual(
            updated_user.telegram_chat_id, ""
        )  # Сохраняется как пустая строка

    def test_unique_telegram_chat_id(self):
        """Тест: уникальность telegram_chat_id"""
        # Создаём пользователя с ID
        User.objects.create_user(username="user2", telegram_chat_id="999999", password="testpass123")

        # Пытаемся создать второго с тем же ID
        duplicate_user = User(
            username="user3", telegram_chat_id="999999"  # Повторяющийся ID
        )
        duplicate_user.set_password("testpass123")  # Устанавливаем пароль для валидации

        with self.assertRaises(ValidationError):
            duplicate_user.full_clean()
