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
