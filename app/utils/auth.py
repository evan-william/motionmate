"""
Session-based authentication helpers.
"""

from functools import wraps
from flask import session, redirect, url_for, flash


def login_user(user) -> None:
    session["user_id"] = user.id
    session["user_name"] = user.name
    session["user_role"] = user.role
    session.permanent = True


def logout_user() -> None:
    session.clear()


def current_user_id() -> int | None:
    return session.get("user_id")


def is_authenticated() -> bool:
    return "user_id" in session


def is_dummy_mode() -> bool:
    return session.get("dummy_mode", False)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated() and not is_dummy_mode():
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not is_authenticated() and not is_dummy_mode():
                return redirect(url_for("auth.login"))
            if is_authenticated() and session.get("user_role") not in roles:
                flash("Access denied.", "danger")
                return redirect(url_for("dashboard.index"))
            return f(*args, **kwargs)
        return decorated
    return decorator
