from rest_framework import serializers
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
