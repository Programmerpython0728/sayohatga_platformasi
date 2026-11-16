from __future__ import annotations

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User
from .utils import normalize_phone_number, validate_phone_number


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("phone_number", "full_name", "email")

    def clean_phone_number(self):
        phone_number = normalize_phone_number(self.cleaned_data["phone_number"])
        if not validate_phone_number(phone_number):
            raise forms.ValidationError("Enter a valid phone number.")
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number already exists.")
        return phone_number

    def clean(self):
        data = super().clean()
        if data.get("password1") != data.get("password2"):
            self.add_error("password2", "Passwords do not match.")
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="Passwords are not stored in plain text.")

    class Meta:
        model = User
        fields = (
            "phone_number",
            "full_name",
            "email",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_phone_verified",
            "groups",
            "user_permissions",
        )

    def clean_phone_number(self):
        return normalize_phone_number(self.cleaned_data["phone_number"])

