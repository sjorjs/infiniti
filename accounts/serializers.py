from rest_framework import serializers
from accounts.models import User
from django.core.mail import send_mail

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
