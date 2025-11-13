from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .serializers import RegisterSerializer
from rest_framework.authtoken.models import Token


class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="Регистрация нового пользователя",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response(
                description="Пользователь создан",
                examples={
                    "application/json": {
                        "id": 1,
                        "username": "testuser",
                        "email": "test@example.com",
                        "telegram_chat_id": "123456789"
                    }
                }
            ),
            400: "Неверные данные"
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаём пользователя
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data.get('email', ''),
            telegram_chat_id=serializer.validated_data.get('telegram_chat_id', None)
        )

        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'telegram_chat_id': user.telegram_chat_id
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Авторизация пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response(
                description="Успешная авторизация",
                examples={
                    "application/json": {
                        "token": "abc123...",
                        "user_id": 1,
                        "username": "testuser",
                        "telegram_chat_id": "123456789"
                    }
                }
            ),
            400: "Неверные данные",
            401: "Неверные логин или пароль"
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username и password обязательны'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Аутентификация пользователя
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {'error': 'Неверные логин или пароль'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Получаем или создаём токен
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'telegram_chat_id': user.telegram_chat_id
        }, status=status.HTTP_200_OK)
