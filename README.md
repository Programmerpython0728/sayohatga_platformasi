# Sayohatga

Unified tourism platform for Uzbekistan: places, accommodations, booking, and Telegram-based phone verification.

## Requirements

- Python 3.11+ (recommended 3.12+)
- PostgreSQL (optional for production)

## Quickstart (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Telegram Phone Verification (OTP)

This project uses Telegram bot to generate a 6-digit OTP code and you enter it on the website (signup/login).

### Mode A: Link phone to Telegram (recommended)

1. Create a bot with @BotFather and put token into `.env` (`TELEGRAM_BOT_TOKEN`).
2. Run the bot locally in a separate terminal:

```powershell
python manage.py run_telegram_bot
```

3. In Telegram, open your bot, press "Start", and send your phone number (or press "Share phone").
4. The bot will send you a 6-digit code. Use that code on the website during signup/login.

### Mode B: Dev fallback (no Telegram)

If Telegram is not configured and `DEBUG=True`, the OTP will be printed in server logs (console).

## i18n (UZ/RU/EN)

Language switcher uses Django i18n. For dev:

```powershell
python manage.py makemessages -l ru
python manage.py compilemessages
```

## Notes

- Uploads are stored in `media/` (Image galleries).
- Admin: `http://127.0.0.1:8000/admin/`
