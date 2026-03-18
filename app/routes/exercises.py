"""
Exercise library routes.
"""

from flask import Blueprint, render_template, request
from ..utils.auth import login_required, is_dummy_mode
from ..models.exercise import Exercise

exercises_bp = Blueprint("exercises", __name__)

CATEGORIES = ["all", "stroke", "sports", "orthopedic", "elderly", "cardiac"]


@exercises_bp.route("/")
@login_required
def index():
    dummy = is_dummy_mode()
    category = request.args.get("category", "all")
    if category not in CATEGORIES:
        category = "all"

    if dummy:
        return render_template(
            "exercises/index.html",
            dummy_mode=True,
            exercises=[],
            categories=CATEGORIES,
            active_category=category,
        )

    query = Exercise.query.filter_by(is_active=True)
    if category != "all":
        query = query.filter_by(category=category)

    exercises = query.order_by(Exercise.name).all()
    return render_template(
        "exercises/index.html",
        dummy_mode=False,
        exercises=exercises,
        categories=CATEGORIES,
        active_category=category,
    )


@exercises_bp.route("/<int:exercise_id>")
@login_required
def detail(exercise_id):
    dummy = is_dummy_mode()

    if dummy:
        # Provide a dummy exercise object as a dict
        dummy_exercise = {
            "id": exercise_id,
            "name": "Knee Extension",
            "category": "orthopedic",
            "description": "Luruskan lutut sepenuhnya dari posisi duduk. Efektif untuk memperkuat otot quadriceps pasca operasi.",
            "target_reps": 10,
            "target_sets": 3,
            "duration_seconds": 30,
            "difficulty": "beginner",
        }
        return render_template("exercises/detail.html", dummy_mode=True, exercise=dummy_exercise)

    exercise = Exercise.query.filter_by(id=exercise_id, is_active=True).first_or_404()
    return render_template("exercises/detail.html", dummy_mode=False, exercise=exercise)
