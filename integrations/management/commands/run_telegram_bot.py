from __future__ import annotations

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from accounts.models import TelegramLink
from accounts.utils import generate_otp_code, normalize_phone_number, validate_phone_number
from integrations.models import TelegramOtp


class Command(BaseCommand):
    help = "Run Telegram bot to link phone numbers to chat_id."

    def handle(self, *args, **options):
        if not settings.TELEGRAM_BOT_TOKEN:
            raise CommandError("TELEGRAM_BOT_TOKEN is empty. Set it in .env first.")

        try:
            from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
            from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater
        except Exception as exc:  # pragma: no cover
            raise CommandError(
                "python-telegram-bot is not installed. Run: pip install -r requirements.txt"
            ) from exc

        def start(update: Update, context: CallbackContext):
            button = KeyboardButton("Share phone", request_contact=True)
            markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
            update.message.reply_text(
                "Welcome to Sayohatga.\n\nSend your phone number like +998901234567, or press 'Share phone'.",
                reply_markup=markup,
            )

        def _link_and_send_code(update: Update, phone_number: str):
            TelegramLink.objects.update_or_create(
                phone_number=phone_number,
                defaults={
                    "telegram_chat_id": str(update.effective_chat.id),
                    "telegram_user_id": str(update.effective_user.id) if update.effective_user else "",
                },
            )
            code = generate_otp_code()
            TelegramOtp.create_code(phone_number=phone_number, raw_code=code, ttl_minutes=5)
            update.message.reply_text(
                f"Your Sayohatga code: {code}\n\nEnter this 6-digit code on the website (valid 5 minutes)."
            )

        def handle_contact(update: Update, context: CallbackContext):
            contact = update.message.contact
            if not contact or not contact.phone_number:
                update.message.reply_text("No phone number received. Try again.")
                return

            phone_number = normalize_phone_number(contact.phone_number.strip())
            if not validate_phone_number(phone_number):
                update.message.reply_text("Invalid phone number format. Example: +998901234567")
                return

            _link_and_send_code(update, phone_number)

        def handle_text(update: Update, context: CallbackContext):
            text = (update.message.text or "").strip()
            phone_number = normalize_phone_number(text)
            if not validate_phone_number(phone_number):
                update.message.reply_text("Send phone like +998901234567 (only digits and +).")
                return
            _link_and_send_code(update, phone_number)

        updater = Updater(token=settings.TELEGRAM_BOT_TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.contact, handle_contact))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

        self.stdout.write(self.style.SUCCESS("Telegram bot is running. Press Ctrl+C to stop."))
        updater.start_polling()
        updater.idle()
