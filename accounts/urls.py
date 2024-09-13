from django.urls import path
from accounts.views import RegisterView, VerifyOtpView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-otp/", VerifyOtpView.as_view(), name="verify-otp"),
]
