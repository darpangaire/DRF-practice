from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView



urlpatterns = [
  path('api/register/',UserRegistrationView.as_view(),name='register'),
  path('api/login/',UserLoginView.as_view(),name='login'),
  path('api/profile/',UserProfileView.as_view(),name='profile'),
  path('api/change-password/',UserChangePasswordView.as_view(),name='passwordChange'),
  
  path('api/reset-password/',SendPasswordResetEmailView.as_view(),name='passwordReset'),
  
  path('api/reset/<uid>/<token>',UserPasswordResetView.as_view(),name='userPasswordReset'),
  
]






