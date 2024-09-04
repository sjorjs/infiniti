import random
from accounts.models import OTP
from accounts.utils.email_utils import send_otp_email


def generate_otp():
    return str(random.randint(100000, 999999))


def create_and_send_otp(user):
    otp_code = generate_otp()
    OTP.objects.update_or_create(user=user, defaults={'otp_code': otp_code})
    send_otp_email(user, otp_code)
