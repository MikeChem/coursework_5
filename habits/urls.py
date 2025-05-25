from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Для документации
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from habits.views import HabitViewSet, RegisterView, LoginView, PublicHabitViewSet

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')
router.register(r'public-habits', PublicHabitViewSet, basename='public-habit')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # Документация
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('', include(router.urls)),
]