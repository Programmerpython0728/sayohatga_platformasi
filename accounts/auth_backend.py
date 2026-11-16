from __future__ import annotations

from django.contrib.auth.backends import ModelBackend

from .models import User
from .utils import normalize_phone_number


class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, phone_number=None, **kwargs):
        phone = phone_number or username or kwargs.get("phone_number")
        if not phone or not password:
            return None
        phone = normalize_phone_number(phone)
        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

