"""
Authentication routes: register, login, logout.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.db import db
from ..models.user import User
from ..utils.auth import login_user, logout_user, is_authenticated, is_dummy_mode
from ..utils.validators import sanitize, validate_email, validate_password, validate_name

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # If in dummy mode, simulate register success
    if is_dummy_mode():
        session.pop("dummy_mode", None)
        flash("Account created! Welcome, Dummy User!", "success")
        return redirect(url_for("dashboard.index"))

    if is_authenticated():
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        name = sanitize(request.form.get("name", ""))
        email = sanitize(request.form.get("email", "")).lower()
        password = request.form.get("password", "")

        if not validate_name(name):
            flash("Name must be between 2 and 120 characters.", "danger")
            return render_template("auth/register.html", dummy_mode=False)

        if not validate_email(email):
            flash("Invalid email address.", "danger")
            return render_template("auth/register.html", dummy_mode=False)

        ok, msg = validate_password(password)
        if not ok:
            flash(msg, "danger")
            return render_template("auth/register.html", dummy_mode=False)

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return render_template("auth/register.html", dummy_mode=False)

        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f"Welcome, {user.name}!", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("auth/register.html", dummy_mode=False)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # If in dummy mode, simulate login success
    if is_dummy_mode():
        session.pop("dummy_mode", None)
        flash("Logged in as Dummy User!", "success")
        return redirect(url_for("dashboard.index"))

    if is_authenticated():
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = sanitize(request.form.get("email", "")).lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email, is_active=True).first()

        if user and user.check_password(password):
            login_user(user)
            next_url = request.args.get("next")
            if next_url and next_url.startswith("/"):
                return redirect(next_url)
            return redirect(url_for("dashboard.index"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", dummy_mode=False)


@auth_bp.route("/logout")
def logout():
    # Also clear dummy mode on logout
    session.pop("dummy_mode", None)
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))
