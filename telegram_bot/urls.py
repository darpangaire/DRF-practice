from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import chatbot

# router = DefaultRouter()
# router.register(r'users', TelegramUserViewSet)

urlpatterns = [
    path('protected/',chatbot,name='protected'),
    
]

