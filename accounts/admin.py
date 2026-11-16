from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .admin_forms import UserChangeForm, UserCreationForm
from .models import PhoneVerificationCode, TelegramLink, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    ordering = ("phone_number",)
    list_display = ("phone_number", "full_name", "is_phone_verified", "is_active", "is_staff")
    search_fields = ("phone_number", "full_name", "email")
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Profile", {"fields": ("full_name", "email")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Verification", {"fields": ("is_phone_verified",)}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "full_name", "email", "password1", "password2", "is_staff", "is_superuser"),
            },
        ),
    )
    filter_horizontal = ("groups", "user_permissions")
    readonly_fields = ("date_joined",)
    list_filter = ("is_active", "is_staff", "is_phone_verified")


@admin.register(TelegramLink)
class TelegramLinkAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "telegram_chat_id", "telegram_user_id", "updated_at")
    search_fields = ("phone_number", "telegram_chat_id")


@admin.register(PhoneVerificationCode)
class PhoneVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "expires_at", "attempts_used", "is_used")
    list_filter = ("is_used",)
    search_fields = ("user__phone_number",)
