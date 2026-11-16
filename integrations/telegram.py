from __future__ import annotations

import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class TelegramSendError(RuntimeError):
    pass


def telegram_is_configured() -> bool:
    return bool(settings.TELEGRAM_BOT_TOKEN)


def build_telegram_bot_url(start: str | None = None) -> str:
    base_url = (getattr(settings, "TELEGRAM_BOT_URL", "") or "").strip()
    if not base_url:
        return ""
    if start:
        separator = "&" if "?" in base_url else "?"
        return f"{base_url}{separator}start={start}"
    return base_url


def send_otp(phone_number: str, otp_code: str, message_prefix: str = "Sayohatga") -> bool:
    """
    Sends OTP via Telegram.

    Modes:
    - link: uses accounts.TelegramLink mapping (phone -> chat_id).
    - static: uses TELEGRAM_STATIC_CHAT_ID for dev/testing.
    """
    from accounts.models import TelegramLink

    if not telegram_is_configured():
        return False

    mode = (settings.TELEGRAM_CHAT_ID_MODE or "link").lower()
    chat_id = None

    if mode == "static":
        chat_id = settings.TELEGRAM_STATIC_CHAT_ID or None
    else:
        link = TelegramLink.objects.filter(phone_number=phone_number).first()
        if link:
            chat_id = str(link.telegram_chat_id)

    if not chat_id:
        return False

    text = f"{message_prefix}: verification code is {otp_code}"

    try:
        from telegram import Bot
    except Exception as exc:  # pragma: no cover
        raise TelegramSendError(
            "python-telegram-bot is not installed. Run: pip install -r requirements.txt"
        ) from exc

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    try:
        bot.send_message(chat_id=chat_id, text=text)
    except Exception as exc:
        logger.warning("Telegram send failed: %s", exc)
        return False
    return True
