from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(user, otp_code):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp_code}. It is valid for 2 minutes.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
