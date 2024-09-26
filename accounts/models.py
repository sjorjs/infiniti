from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email=None, otp=None, password=None, role=None, **extra_fields
    ):
        """
        Create and save a regular User with the given email and otp.
        """
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if role is None and not extra_fields.get("is_superuser", False):
            user.role = User.NORMAL_USER
        else:
            user.role = role

        if otp:  # OTP for regular users
            user.otp = otp
        else:
            user.set_password(
                password
            )  # Password for superusers or regular password users

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.SUPERUSER)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        user = self.create_user(email=email, password=password, **extra_fields)
        return user


class User(AbstractUser):
    NORMAL_USER = "normal"
    BLOGGER = "blogger"
    SUPERUSER = "superuser"

    ROLE_CHOICES = [
        (NORMAL_USER, "Normal User"),
        (BLOGGER, "Blogger"),
        (SUPERUSER, "Superuser"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=10,
        default=NORMAL_USER,
        blank=True,
        null=True,
    )
    otp = models.CharField(
        max_length=6, null=True, blank=True
    )  # OTP for non-superusers

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
