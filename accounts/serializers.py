from rest_framework import serializers
from accounts.models import User
from accounts.utils.email_utils import send_otp_email
from accounts.utils.otp_utils import generate_otp


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ["email"]

    def create(self, validated_data):
        email = validated_data.get("email")
        otp = generate_otp()

        user = User.objects.create(
            email=email,
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
