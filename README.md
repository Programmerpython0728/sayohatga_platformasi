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

## Docker Production Stack

Files added for production deployment:

- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`
- `docker/entrypoint.sh`
- `docker/nginx/default.conf`
- `.env.docker.example`

### Start with Docker

1. Copy env template:

```powershell
copy .env.docker.example .env
```

2. Set real values in `.env`:

- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DB_PASSWORD`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_BOT_URL`
- security flags from `.env.docker.example`

3. Build and run:

```powershell
docker compose up --build -d
```

4. Open:

```text
http://localhost
```

### Services

- `web` — Django + Gunicorn
- `db` — PostgreSQL 16
- `nginx` — reverse proxy + static/media

### Production security settings

This project now supports production hardening through environment variables:

- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `SECURE_PROXY_SSL_HEADER_ENABLED=True`
- `SECURE_HSTS_SECONDS=31536000`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`
- `SECURE_HSTS_PRELOAD=True`
- `USE_X_FORWARDED_HOST=True`
- `USE_X_FORWARDED_PORT=True`

For real production, replace:

- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `SECRET_KEY`
- `DB_PASSWORD`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_BOT_URL`

with real values before first deploy.

### Useful commands

```powershell
docker compose logs -f web
docker compose exec web python manage.py createsuperuser
docker compose down
```

### First production deploy checklist

1. Set `ENVIRONMENT=production`
2. Set a strong `SECRET_KEY`
3. Set real domain names in `ALLOWED_HOSTS`
4. Set real HTTPS origins in `CSRF_TRUSTED_ORIGINS`
5. Set strong `DB_PASSWORD`
6. Set real `TELEGRAM_BOT_TOKEN`
7. Set real `TELEGRAM_BOT_URL`
8. Start:

```powershell
docker compose up --build -d
```

9. Create admin:

```powershell
docker compose exec web python manage.py createsuperuser
```

10. Verify:

- site opens through Nginx
- static files load
- media files load
- admin login works
- Telegram OTP flow works

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

## SEO & Performance

Sayt qidiruv tizimlari (Google/Yandex) uchun optimallashtirilgan:

- **`/sitemap.xml`** — barcha joylar, turar joylar va statik sahifalar avtomatik.
- **`/robots.txt`** — crawlerlar uchun; admin/kabinet sahifalari yopilgan.
- **Open Graph + Twitter Card** meta teglar (`base.html`) — ijtimoiy tarmoqlarda chiroyli ko'rinish.
- **JSON-LD structured data** — joylar `TouristAttraction`, turar joylar `LodgingBusiness` (Google rich results).
- **`<html lang>`** + canonical URL har sahifada.

### Muhim: production sitemap domeni

Sitemap `django.contrib.sites` domenidan foydalanadi (standart: `example.com`). Deploy'dan oldin admin panelda **Sites → Site** domenini `sayohatga.uz` ga o'zgartiring, aks holda sitemap URL'lari noto'g'ri bo'ladi.

### Performance

- `nav_context` regionlari cache'lanadi (har sahifadagi DB so'rovi olib tashlandi; Region o'zgarganda avtomatik tozalanadi).
- List/home/basket sahifalarida `cover_image` N+1 muammosi tuzatildi — kartalar soni ortsa ham query soni o'zgarmaydi.
- `TouristPlace`/`Accommodation` uchun DB indekslar (name, created_at, type, price, city).
- Redis cache qo'llab-quvvatlanadi: `.env` da `REDIS_URL=redis://...` bering (aks holda locmem ishlatiladi).

## Notes

- Uploads are stored in `media/` (Image galleries).
- Admin: `http://127.0.0.1:8000/admin/`
