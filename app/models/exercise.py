"""
Core domain models: Exercise, RehabSession, Progress.
"""

from datetime import datetime
from .db import db


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text)
    target_reps = db.Column(db.Integer, default=10)
    target_sets = db.Column(db.Integer, default=3)
    duration_seconds = db.Column(db.Integer, default=30)
    difficulty = db.Column(db.String(20), default="beginner")
    thumbnail = db.Column(db.String(255), default="default.png")
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "target_reps": self.target_reps,
            "target_sets": self.target_sets,
            "duration_seconds": self.duration_seconds,
            "difficulty": self.difficulty,
            "thumbnail": self.thumbnail,
        }


class RehabSession(db.Model):
    __tablename__ = "rehab_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    reps_completed = db.Column(db.Integer, default=0)
    sets_completed = db.Column(db.Integer, default=0)
    accuracy_score = db.Column(db.Float, default=0.0)
    duration_seconds = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="pending")
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    exercise = db.relationship("Exercise", backref="sessions")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "exercise": self.exercise.to_dict() if self.exercise else None,
            "reps_completed": self.reps_completed,
            "sets_completed": self.sets_completed,
            "accuracy_score": self.accuracy_score,
            "duration_seconds": self.duration_seconds,
            "status": self.status,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class Progress(db.Model):
    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    sessions_count = db.Column(db.Integer, default=0)
    total_reps = db.Column(db.Integer, default=0)
    avg_accuracy = db.Column(db.Float, default=0.0)
    streak_days = db.Column(db.Integer, default=0)

    def to_dict(self) -> dict:
        return {
            "date": self.date.isoformat(),
            "sessions_count": self.sessions_count,
            "total_reps": self.total_reps,
            "avg_accuracy": self.avg_accuracy,
            "streak_days": self.streak_days,
        }
