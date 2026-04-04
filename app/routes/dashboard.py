"""
Dashboard routes , user overview, progress stats.
"""

from flask import Blueprint, render_template
from ..utils.auth import login_required, current_user_id, is_dummy_mode
from ..models.user import User
from ..models.exercise import RehabSession, Progress, GameSession

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    dummy = is_dummy_mode()

    if dummy:
        return render_template(
            "dashboard/index.html",
            dummy_mode=True,
            user_name="Dummy User",
            total_sessions=24,
            avg_accuracy=87.0,
            streak=12,
            recent_sessions=[],
            progress_records=[],
            memory_scores={'easy': 450, 'medium': 320, 'hard': 150},
            speech_accuracy=92.5
        )

    uid = current_user_id()
    user = User.query.get_or_404(uid)

    recent_sessions = (
        RehabSession.query
        .filter_by(user_id=uid)
        .order_by(RehabSession.started_at.desc())
        .limit(5)
        .all()
    )

    progress_records = (
        Progress.query
        .filter_by(user_id=uid)
        .order_by(Progress.date.desc())
        .limit(7)
        .all()
    )

    total_sessions = RehabSession.query.filter_by(user_id=uid, status="completed").count()

    avg_accuracy = 0.0
    if total_sessions:
        all_scores = [s.accuracy_score for s in RehabSession.query.filter_by(user_id=uid, status="completed").all()]
        avg_accuracy = sum(all_scores) / len(all_scores) if all_scores else 0.0

    streak = progress_records[0].streak_days if progress_records else 0

    memory_sessions = GameSession.query.filter_by(user_id=uid, game_type='memory').all()
    memory_scores = {
        'easy': max([s.score for s in memory_sessions if s.difficulty == 'easy'] + [0]),
        'medium': max([s.score for s in memory_sessions if s.difficulty == 'medium'] + [0]),
        'hard': max([s.score for s in memory_sessions if s.difficulty == 'hard'] + [0])
    }

    speech_sessions = GameSession.query.filter_by(user_id=uid, game_type='speech').all()
    speech_accuracy = sum([s.accuracy for s in speech_sessions]) / len(speech_sessions) if speech_sessions else 0.0

    return render_template(
        "dashboard/index.html",
        dummy_mode=False,
        user_name=user.name.split(" ")[0],
        total_sessions=total_sessions,
        avg_accuracy=round(avg_accuracy, 1),
        streak=streak,
        recent_sessions=recent_sessions,
        progress_records=progress_records,
        memory_scores=memory_scores,
        speech_accuracy=round(speech_accuracy, 1)
    )