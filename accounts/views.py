from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from accounts.models import OTP, User
from accounts.serializers import UserRegistrationSerializer, LoginRequestSerializer, OTPSerializer
from accounts.utils.otp_utils import create_and_send_otp


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        captcha = serializer.validated_data['captcha']

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({'message': 'Invalid username'}, status=status.HTTP_404_NOT_FOUND)

        create_and_send_otp(user)
        return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)


class OTPVerificationThrottle(UserRateThrottle):
    scope = 'otp_verification'


class OTPVerifyView(APIView):
    throttle_classes = [OTPVerificationThrottle]

    def post(self, request):
        serializer = OTPSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']

            try:
                user = User.objects.get(email=email)
                otp = OTP.objects.get(user=user)

                if not otp.is_valid():
                    return Response({'error': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)

                if otp.otp_code == otp_code:
                    return Response({'message': 'Login Successful'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

            except (User.DoesNotExist, OTP.DoesNotExist):
                return Response({'error': 'Invalid email or OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        return Response({'message': 'Logout Successfully.'}, status=status.HTTP_200_OK)
