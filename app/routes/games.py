"""
Games routes for Memory and Speech therapy.
"""

from flask import Blueprint, render_template, request, jsonify
from ..utils.auth import login_required, current_user_id, is_dummy_mode
from ..models.db import db
from ..models.exercise import GameSession

games_bp = Blueprint("games", __name__)


@games_bp.route("/hub")
@login_required
def hub():
    return render_template("games/hub.html", dummy_mode=is_dummy_mode())


@games_bp.route("/memory")
@login_required
def memory():
    return render_template("games/memory.html", dummy_mode=is_dummy_mode())


@games_bp.route("/speech")
@login_required
def speech():
    return render_template("games/speech.html", dummy_mode=is_dummy_mode())


@games_bp.route("/save", methods=["POST"])
@login_required
def save():
    if is_dummy_mode():
        return jsonify({"status": "ok", "msg": "Dummy mode, not saved"})
    
    data = request.get_json(silent=True) or {}
    uid = current_user_id()
    
    session_obj = GameSession(
        user_id=uid,
        game_type=data.get("game_type", "unknown"),
        difficulty=data.get("difficulty", "easy"),
        score=int(data.get("score", 0)),
        max_score=int(data.get("max_score", 0)),
        accuracy=float(data.get("accuracy", 0.0))
    )
    
    db.session.add(session_obj)
    db.session.commit()
    
    return jsonify({"status": "ok", "session_id": session_obj.id})