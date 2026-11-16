from __future__ import annotations

import logging

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from integrations.telegram import build_telegram_bot_url, telegram_is_configured

from .forms import LoginForm, ProfileForm, RegisterForm, TelegramLoginForm
from .models import User
from .utils import normalize_phone_number

logger = logging.getLogger(__name__)


def register(request):
    post_data = request.POST.copy() if request.method == "POST" else None
    if request.method == "POST" and "phone" in request.POST:
        post_data["phone_number"] = request.POST.get("phone", "")
        post_data["telegram_code"] = request.POST.get("otp_code", "")
    if request.method == "POST":
        form = RegisterForm(post_data)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            full_name = form.cleaned_data.get("full_name", "")
            password = form.cleaned_data["password1"]

            user = User.objects.create_user(
                phone_number=phone_number,
                password=password,
                full_name=full_name,
                is_active=True,
                is_phone_verified=True,
            )
            login(request, user, backend="accounts.auth_backend.PhoneBackend")
            messages.success(request, "Account created.")
            return redirect("accounts:profile")
    else:
        form = RegisterForm()
    return render(
        request,
        "users/register.html",
        {
            "form": form,
            "telegram_bot_url": build_telegram_bot_url("register"),
            "telegram_configured": telegram_is_configured(),
        },
    )


def verify(request):
    messages.info(request, "Verification is done in Telegram bot now. Use Telegram code during registration.")
    return redirect("accounts:register")


def resend_otp(request):
    return redirect("accounts:telegram_help")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    mode = request.POST.get("_mode") or request.POST.get("login_type")
    password_post = request.POST.copy() if request.method == "POST" else None
    otp_post = request.POST.copy() if request.method == "POST" else None
    if request.method == "POST" and "phone" in request.POST:
        if password_post is not None:
            password_post["phone_number"] = request.POST.get("phone", "")
        if otp_post is not None:
            otp_post["phone_number"] = request.POST.get("phone", "")
            otp_post["telegram_code"] = request.POST.get("otp_code", "")
    if request.method == "POST" and mode == "password":
        form = LoginForm(password_post)
        tg_form = TelegramLoginForm()
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user, backend="accounts.auth_backend.PhoneBackend")
            return redirect("accounts:dashboard")
    elif request.method == "POST" and mode in {"telegram", "otp"}:
        tg_form = TelegramLoginForm(otp_post)
        form = LoginForm()
        if tg_form.is_valid():
            user = tg_form.cleaned_data["user"]
            login(request, user, backend="accounts.auth_backend.PhoneBackend")
            return redirect("accounts:dashboard")
    else:
        form = LoginForm()
        tg_form = TelegramLoginForm()

    return render(
        request,
        "users/login.html",
        {
            "form": form,
            "tg_form": tg_form,
            "telegram_bot_url": build_telegram_bot_url("login"),
            "telegram_configured": telegram_is_configured(),
        },
    )


def logout_view(request):
    logout(request)
    return redirect("core:home")


@login_required
def dashboard(request):
    from bookings.models import Booking, PlaceBooking
    from django.contrib.contenttypes.models import ContentType
    from django.db.utils import OperationalError
    from catalog.models import Accommodation, Image, Like, TouristPlace

    bookings = (
        Booking.objects.select_related("accommodation", "accommodation__city", "accommodation__city__region")
        .filter(user=request.user)
        .order_by("-created_at")
    )
    place_bookings = (
        PlaceBooking.objects.select_related("place", "place__city", "place__city__region")
        .filter(user=request.user)
        .order_by("-created_at")
    )
    try:
        likes = Like.objects.filter(user=request.user).order_by("-created_at")[:24]
    except OperationalError:
        likes = []

    place_ct = ContentType.objects.get_for_model(TouristPlace)
    acc_ct = ContentType.objects.get_for_model(Accommodation)
    place_ids = [l.object_id for l in likes if l.content_type_id == place_ct.id]
    acc_ids = [l.object_id for l in likes if l.content_type_id == acc_ct.id]

    liked_places = list(TouristPlace.objects.filter(id__in=place_ids).select_related("city", "city__region")[:12])
    liked_accommodations = list(
        Accommodation.objects.filter(id__in=acc_ids).select_related("city", "city__region")[:12]
    )

    def first_image_map(model_cls, ids):
        if not ids:
            return {}
        ct = ContentType.objects.get_for_model(model_cls)
        imgs = Image.objects.filter(content_type=ct, object_id__in=ids).order_by("object_id", "sort_order", "id")
        m = {}
        for img in imgs:
            if img.object_id not in m:
                m[img.object_id] = img
        return m

    place_images = first_image_map(TouristPlace, [p.id for p in liked_places])
    acc_images = first_image_map(Accommodation, [a.id for a in liked_accommodations])

    return render(
        request,
        "users/dashboard.html",
        {
            "bookings": bookings,
            "place_bookings": place_bookings,
            "liked_places": liked_places,
            "liked_accommodations": liked_accommodations,
            "place_images": place_images,
            "acc_images": acc_images,
        },
    )


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(
        request,
        "users/profile.html",
        {
            "form": form,
            "profile_user": request.user,
        },
    )


def telegram_help(request):
    return render(
        request,
        "users/otp_help.html",
        {
            "telegram_configured": telegram_is_configured(),
            "telegram_bot_url": build_telegram_bot_url("help"),
        },
    )
