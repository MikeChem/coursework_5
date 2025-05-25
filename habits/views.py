from django.contrib.auth.models import User
from rest_framework import generics, permissions, serializers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Habit
from .serializers import HabitSerializer


# ========== Сериализатор регистрации ==========
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# ========== Вьюшки регистрации и входа ==========
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    # Используем стандартную логику из SimpleJWT
    pass


# ========== Пермишен для владельца ==========
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


# ========== Привычки текущего пользователя ==========
class StandardResultsSetPagination(PageNumberPagination):
    """Пагинация по 5 записей на странице"""

    page_size = 5
    page_size_query_param = "page_size"


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ========== Публичные привычки ==========
class PublicHabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]  # или []
