from django.contrib import admin

from .models import TelegramOtp


@admin.register(TelegramOtp)
class TelegramOtpAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "created_at", "expires_at", "attempts_used", "is_used")
    list_filter = ("is_used",)
    search_fields = ("phone_number",)

