from django.urls import path
from . import views

urlpatterns = [
    path('normal_signup/', views.signup, name='singup'),
    path('social_signup_signin/', views.social_signup_signup, name='social_signup'),
    path('login/', views.login, name='login'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('forgot-password/', views.forgot_password),
    path('reset-password/', views.reset_password),
    path('change-password/', views.change_password),
]