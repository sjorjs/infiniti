from django.urls import path
from accounts.views import UserRegisterView, UserLoginView, OTPVerifyView, LogoutView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify_otp'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
