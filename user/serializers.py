from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    telegram_chat_id = serializers.CharField(
        required=False, allow_blank=True, help_text="ID чата Telegram (опционально)"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "telegram_chat_id"]
        extra_kwargs = {"email": {"required": False}}
