from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import RegisterSerializer
from accounts.models import User


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "OTP has been sent to your email."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            # Find the user with the provided email and OTP
            user = User.objects.get(email=email, otp=otp)

            # If user is found, proceed with verification (you can add further logic here)
            return Response(
                {"message": "OTP verified successfully!"}, status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"error": "Invalid OTP or email."}, status=status.HTTP_400_BAD_REQUEST
            )
