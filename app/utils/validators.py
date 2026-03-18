"""
Input validation and sanitization helpers.
"""

import re
import html


EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
PASSWORD_MIN = 8


def sanitize(value: str) -> str:
    """Strip and HTML-escape a string to prevent XSS."""
    return html.escape(value.strip()) if value else ""


def validate_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email))


def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < PASSWORD_MIN:
        return False, f"Password must be at least {PASSWORD_MIN} characters."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    return True, ""


def validate_name(name: str) -> bool:
    return 2 <= len(name.strip()) <= 120
