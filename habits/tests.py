from django.test import TestCase
from django.core.exceptions import ValidationError
from user.models import User
from .models import Habit


class HabitModelTest(TestCase):
    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_create_habit_valid(self):
        """Тест: создание корректной привычки."""
        habit = Habit(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Бегать по утрам",
            is_pleasant=False,
            periodicity=1,
            execution_time=60,
            is_public=False,
        )
        habit.full_clean()  # Вызывает clean()
        habit.save()

        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(str(habit), "Бегать по утрам в Дом")

    def test_clean_reward_and_related_habit(self):
        """Тест: нельзя указать reward и related_habit одновременно."""
        habit = Habit(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Читать книгу",
            reward="Чашка чая",
            related_habit=Habit(
                user=self.user, action="Приятная привычка", is_pleasant=True
            ),
            periodicity=1,
            execution_time=60,
        )

        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()

        self.assertIn(
            "Нельзя указать одновременно вознаграждение и связанную привычку.",
            str(cm.exception),
        )

    def test_clean_execution_time_too_long(self):
        """Тест: execution_time > 120 секунд."""
        habit = Habit(
            user=self.user,
            place="Офис",
            time="12:00:00",
            action="Медитировать",
            execution_time=150,  # > 120
            periodicity=1,
        )

        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()

        self.assertIn(
            "Время выполнения не может превышать 120 секунд.", str(cm.exception)
        )

    def test_clean_periodicity_out_of_range(self):
        """Тест: periodicity не в диапазоне 1–7."""
        # periodicity = 0
        habit = Habit(
            user=self.user,
            place="Парк",
            time="18:00:00",
            action="Гулять",
            periodicity=0,
            execution_time=30,
        )

        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()

        self.assertIn("Периодичность должна быть от 1 до 7 дней.", str(cm.exception))

        # periodicity = 8
        habit.periodicity = 8
        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()

        self.assertIn("Периодичность должна быть от 1 до 7 дней.", str(cm.exception))

    def test_clean_pleasant_habit_with_reward(self):
        """Тест: приятная привычка не может иметь reward."""
        habit = Habit(
            user=self.user,
            place="Спальня",
            time="22:00:00",
            action="Слушать музыку",
            is_pleasant=True,
            reward="Конфета",  # Нельзя для приятной привычки
            periodicity=1,
            execution_time=30,
        )

        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()

        self.assertIn(
            "Приятная привычка не может иметь вознаграждения или связанной привычки.",
            str(cm.exception),
        )

    def test_clean_pleasant_habit_with_related_habit(self):
        """Тест: приятная привычка не может иметь related_habit."""
        related = Habit.objects.create(
            user=self.user,
            action="Приятная привычка",
            is_pleasant=True,
            periodicity=1,
            execution_time=30,
        )

        habit = Habit(
            user=self.user,
            place="Гостиная",
            time="20:00:00",
            action="Пить чай",
            is_pleasant=True,
            related_habit=related,  # Нельзя для приятной привычки
            periodicity=1,
            execution_time=30,
        )

        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()

        self.assertIn(
            "Приятная привычка не может иметь вознаграждения или связанной привычки.",
            str(cm.exception),
        )

    def test_clean_valid_pleasant_habit(self):
        """Тест: корректная приятная привычка (без reward/related_habit)."""
        habit = Habit(
            user=self.user,
            place="Балкон",
            time="07:00:00",
            action="Дышать свежим воздухом",
            is_pleasant=True,
            periodicity=1,
            execution_time=60,
        )
        habit.full_clean()  # Не должно быть ошибок
        habit.save()

        self.assertEqual(Habit.objects.count(), 1)

    def test_string_representation(self):
        """Тест: метод __str__ возвращает корректную строку."""
        habit = Habit(
            user=self.user,
            place="Кухня",
            time="09:00:00",
            action="Пить воду",
            periodicity=1,
            execution_time=10,
        )
        self.assertEqual(str(habit), "Пить воду в Кухня")
