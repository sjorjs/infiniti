from django.urls import path
from accounts.views import RegisterView, VerifyOtpView, LoginView, VerifyLoginOtpView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-otp/", VerifyOtpView.as_view(), name="verify-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("login/verify/", VerifyLoginOtpView.as_view(), name="verify-login-otp"),
]
