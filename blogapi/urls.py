from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView

from . import views


urlpatterns = [
  path('api/register/',UserRegistrationView.as_view(),name='register'),
  path('api/login/',UserLoginView.as_view(),name='login'),
  path('api/profile/',UserProfileView.as_view(),name='profile'),
  path('api/change-password/',UserChangePasswordView.as_view(),name='passwordChange'),
  
  path('api/reset-password/',SendPasswordResetEmailView.as_view(),name='passwordReset'),
  
  path('api/reset/<uid>/<token>',UserPasswordResetView.as_view(),name='userPasswordReset'),
  
  
  path('', views.login_page, name='login'),
  # path('protected/', views.protected_page, name='protected'),
  path('register/', views.register_Page, name='register'),
  path('reset-email-pass/', views.reset_email_Password, name='resetEmailPassword'),
  
  path('reset-password/', views.password_reset, name='passwordReset'),
  
]






