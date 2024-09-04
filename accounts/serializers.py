from rest_framework import serializers
from accounts.models import User, OTP


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "role"]

        def create(self, validated_data):
            user = User.objects.create_user(
                email=validated_data["email"],
                password=validated_data["password"],
                role=validated_data["role"],
            )
            return user


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    captcha = serializers.CharField(max_length=6)


class OTPSerializer(serializers.ModelSerializer):
    otp_code = serializers.CharField(max_length=6)
    email = serializers.EmailField()

    class Meta:
        model = OTP
        fields = ["otp_code", "email"]
