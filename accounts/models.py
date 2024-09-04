from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    NORMAL_USER = 'normal'
    BLOGGER = 'blogger'
    ROLE_CHOICES = [
        (NORMAL_USER, 'Normal User'),
        (BLOGGER, 'Blogger'),
    ]

    username = None
    role = models.CharField(choices=ROLE_CHOICES, max_length=10, default=NORMAL_USER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.email


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # It must be 2 minutes but for Synchronize server time issue changed to 60 minutes
        # return timezone.now() < self.created_at + timedelta(minutes=60)
        return self.created_at

    def __str__(self):
        return f"OTP for {self.user.email}"
