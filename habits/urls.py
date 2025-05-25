# habits/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import HabitViewSet, LoginView, PublicHabitListView, RegisterView

urlpatterns = [
    # Авторизация
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Привычки
    path("habits/", HabitViewSet.as_view({"get": "list", "post": "create"})),
    path("public/", PublicHabitListView.as_view(), name="public-habits"),
]
