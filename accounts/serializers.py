import datetime

from django.core.cache import cache
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.utils.email_utils import send_otp_email
from accounts.utils.otp_utils import generate_otp


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    role = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["email", "role"]

    def create(self, validated_data):
        email = validated_data.get("email")
        role = validated_data.get("role")

        if not role and not validated_data.get("is_superuser", False):
            role = User.NORMAL_USER

        otp = generate_otp()

        user = User.objects.create(
            email=email,
            role=role,
            otp=otp,
            is_active=False,  # Set the user as inactive until OTP is verified
        )

        send_otp_email(user, otp)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("user with this email does not exist")
        return value

    def save(self, **kwargs):
        email = self.validated_data.get("email")
        user = User.objects.get(email=email)

        otp = generate_otp()
        cache.set(f"otp_{email}", otp, timeout=120)
        send_otp_email(user, otp)


class VerifyLoginOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")
        checked_otp = cache.get(f"otp_{email}")

        if checked_otp is None or checked_otp != otp:
            raise serializers.ValidationError("Invalid or expired otp.")
        return data

    def save(self, **kwargs):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        token = RefreshToken.for_user(user)
        user.last_login = datetime.datetime.now()
        user.save()
        return {"access_token": str(token.access_token), "refresh_token": str(token)}


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        try:
            user = User.objects.get(email=email, otp=otp)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email.")

        data["user"] = user
        return data
