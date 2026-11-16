from __future__ import annotations

from datetime import timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from .utils import normalize_phone_number


class UserManager(BaseUserManager):
    def create_user(self, phone_number: str, password: str | None = None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")

        phone_number = normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_phone_verified", True)
        return self.create_user(phone_number=phone_number, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS: list[str] = []

    def save(self, *args, **kwargs):
        self.phone_number = normalize_phone_number(self.phone_number)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number

    @property
    def phone(self) -> str:
        return self.phone_number


class TelegramLink(models.Model):
    phone_number = models.CharField(max_length=20, unique=True)
    telegram_chat_id = models.CharField(max_length=64)
    telegram_user_id = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.phone_number = normalize_phone_number(self.phone_number)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.phone_number} -> {self.telegram_chat_id}"


class PhoneVerificationCode(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="verification_codes")
    code_hash = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts_used = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=5)
    is_used = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["user", "expires_at"]),
        ]

    @classmethod
    def create_for_user(cls, user: User, raw_code: str, ttl_minutes: int = 5) -> "PhoneVerificationCode":
        now = timezone.now()
        return cls.objects.create(
            user=user,
            code_hash=make_password(raw_code),
            expires_at=now + timedelta(minutes=ttl_minutes),
        )

    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    def can_attempt(self) -> bool:
        return (not self.is_used) and (not self.is_expired()) and (self.attempts_used < self.max_attempts)

    def check_and_consume(self, raw_code: str) -> bool:
        if not self.can_attempt():
            return False

        self.attempts_used += 1
        ok = check_password(raw_code, self.code_hash)
        if ok:
            self.is_used = True
        self.save(update_fields=["attempts_used", "is_used"])
        return ok
