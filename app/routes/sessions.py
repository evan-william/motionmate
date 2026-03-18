"""
Rehab session routes — start, track, complete.
"""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..utils.auth import login_required, current_user_id, is_dummy_mode
from ..models.db import db
from ..models.exercise import Exercise, RehabSession

sessions_bp = Blueprint("sessions", __name__)


@sessions_bp.route("/start/<int:exercise_id>", methods=["POST"])
@login_required
def start(exercise_id):
    dummy = is_dummy_mode()

    if dummy:
        dummy_exercise = {
            "id": exercise_id,
            "name": "Knee Extension",
            "category": "orthopedic",
            "target_reps": 10,
            "target_sets": 3,
            "duration_seconds": 30,
            "difficulty": "beginner",
        }
        dummy_session = {"id": 1}
        return render_template("sessions/tracker.html", dummy_mode=True, session=dummy_session, exercise=dummy_exercise)

    exercise = Exercise.query.filter_by(id=exercise_id, is_active=True).first_or_404()
    session_obj = RehabSession(
        user_id=current_user_id(),
        exercise_id=exercise.id,
        status="in_progress",
    )
    db.session.add(session_obj)
    db.session.commit()
    return render_template("sessions/tracker.html", dummy_mode=False, session=session_obj, exercise=exercise)


@sessions_bp.route("/<int:session_id>/complete", methods=["POST"])
@login_required
def complete(session_id):
    dummy = is_dummy_mode()

    if dummy:
        return jsonify({"status": "ok", "session_id": session_id})

    session_obj = RehabSession.query.filter_by(
        id=session_id, user_id=current_user_id()
    ).first_or_404()

    data = request.get_json(silent=True) or {}

    reps = max(0, int(data.get("reps_completed", 0)))
    sets = max(0, int(data.get("sets_completed", 0)))
    accuracy = min(100.0, max(0.0, float(data.get("accuracy_score", 0.0))))
    duration = max(0, int(data.get("duration_seconds", 0)))

    session_obj.reps_completed = reps
    session_obj.sets_completed = sets
    session_obj.accuracy_score = accuracy
    session_obj.duration_seconds = duration
    session_obj.status = "completed"
    session_obj.completed_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"status": "ok", "session_id": session_obj.id})


@sessions_bp.route("/history")
@login_required
def history():
    dummy = is_dummy_mode()

    if dummy:
        return render_template("sessions/history.html", dummy_mode=True, pagination=None)

    uid = current_user_id()
    page = request.args.get("page", 1, type=int)
    pagination = (
        RehabSession.query
        .filter_by(user_id=uid)
        .order_by(RehabSession.started_at.desc())
        .paginate(page=page, per_page=10, error_out=False)
    )
    return render_template("sessions/history.html", dummy_mode=False, pagination=pagination)
