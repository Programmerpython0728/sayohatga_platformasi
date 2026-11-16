from __future__ import annotations

import re
import secrets


PHONE_RE = re.compile(r"^[+]?[0-9]{7,15}$")


def normalize_phone_number(raw: str) -> str:
    if raw is None:
        return ""
    cleaned = raw.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if cleaned and cleaned[0] != "+" and cleaned.isdigit():
        cleaned = f"+{cleaned}"
    return cleaned


def validate_phone_number(phone_number: str) -> bool:
    return bool(PHONE_RE.match(phone_number or ""))


def generate_otp_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"

