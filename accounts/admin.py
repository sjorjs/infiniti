from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "role",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Roles", {"fields": ("role",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "role"),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
