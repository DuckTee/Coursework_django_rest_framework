from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import HabitViewSet, PublicHabitViewSet

router = DefaultRouter()
router.register(r'habits', HabitViewSet)
router.register(r'public-habits', PublicHabitViewSet, basename='public-habit')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
