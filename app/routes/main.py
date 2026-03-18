from flask import Blueprint, render_template, session, redirect, url_for
from ..utils.auth import is_authenticated, is_dummy_mode

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html", authenticated=is_authenticated(), dummy_mode=is_dummy_mode())


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/dummy/enable")
def enable_dummy():
    """Enable dummy data mode — simulate a logged-in demo user."""
    session["dummy_mode"] = True
    session["user_id"] = None
    session["user_name"] = "Dummy User"
    session["user_role"] = "patient"
    session.permanent = True
    return redirect(url_for("dashboard.index"))


@main_bp.route("/dummy/disable")
def disable_dummy():
    """Disable dummy data mode."""
    session.pop("dummy_mode", None)
    session.pop("user_id", None)
    session.pop("user_name", None)
    session.pop("user_role", None)
    return redirect(url_for("main.index"))
