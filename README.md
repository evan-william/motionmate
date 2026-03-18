# MotionMate 🏃‍♂️

**Platform rehabilitasi rumahan berbasis AI** — MotionMate memandu pasien melalui latihan fisioterapi dengan pose detection real-time, progress tracking, dan exercise library yang terverifikasi oleh fisioterapis.

---

## Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask 3.x · Python 3.11+ |
| ORM | SQLAlchemy + SQLite (dev) / PostgreSQL (prod) |
| Auth | Session-based · PBKDF2-SHA256 password hashing |
| AI (WIP) | MediaPipe Pose via WebAssembly |
| Frontend | Vanilla HTML/CSS/JS · Jinja2 templates |
| Tests | pytest |

---

## Quickstart

```bash
# Clone & install
git clone https://github.com/evan-william/motionmate
cd motionmate
pip install -r requirements.txt

# Run (development)
python app.py
```

Then open http://localhost:5000

---

## Dummy Data Mode

MotionMate ships with a **Dummy Data Mode** — a zero-registration demo that lets anyone explore all features without creating an account. To enable:

1. Click **"Explore with Dummy Data"** on the landing page, or
2. Visit `/dummy/enable` directly.

Dummy mode shows hardcoded sample data across all pages:
- Dashboard with realistic stats, weekly chart, accuracy ring
- Exercise library (12 exercises across 5 categories)
- Session history (7 sample sessions)
- Fully functional session tracker (manual rep counting + timer)

Exit dummy mode at any time via the **"Exit Demo"** link in the nav or `/dummy/disable`.

---

## Project Structure

```
motionmate/
├── app.py                  # Entry point
├── requirements.txt
├── pytest.ini
├── app/
│   ├── __init__.py         # App factory (create_app)
│   ├── config.py           # Dev / Prod / Testing configs
│   ├── models/
│   │   ├── db.py           # SQLAlchemy setup
│   │   ├── user.py         # User model + password hashing
│   │   └── exercise.py     # Exercise, RehabSession, Progress
│   ├── routes/
│   │   ├── main.py         # Landing, dummy enable/disable
│   │   ├── auth.py         # Register, login, logout
│   │   ├── dashboard.py    # Main dashboard
│   │   ├── exercises.py    # Exercise library + detail
│   │   └── sessions.py     # Start, tracker, complete, history
│   └── utils/
│       ├── auth.py         # login_required, is_dummy_mode
│       └── validators.py   # Email, password, name validators
├── templates/
│   ├── index.html          # Landing page
│   ├── partials/nav.html   # Shared nav include
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── dashboard/
│   │   └── index.html
│   ├── exercises/
│   │   ├── index.html
│   │   └── detail.html
│   └── sessions/
│       ├── tracker.html    # Live session tracker (timer + rep counter)
│       └── history.html
└── tests/
    └── test_app.py         # Full test suite
```

---

## Routes

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Landing page |
| GET | `/dummy/enable` | Enable dummy data mode |
| GET | `/dummy/disable` | Disable dummy data mode |
| GET/POST | `/auth/register` | Register |
| GET/POST | `/auth/login` | Login |
| GET | `/auth/logout` | Logout |
| GET | `/dashboard/` | Main dashboard |
| GET | `/exercises/` | Exercise library |
| GET | `/exercises/<id>` | Exercise detail |
| POST | `/sessions/start/<exercise_id>` | Create session |
| GET | `/sessions/tracker/<session_id>` | Live tracker |
| POST | `/sessions/complete/<session_id>` | Save & complete |
| GET | `/sessions/history` | Session history |

---

## Tests

```bash
pytest -v
```

Covers: auth flows, validators, route responses, dummy mode, accuracy clamping, password hashing, open redirect protection.

---

## Environment Variables

Create a `.env` file for production:

```env
FLASK_ENV=production
SECRET_KEY=your-very-secret-key-here
DATABASE_URL=postgresql://user:pass@host/dbname
```

---

## Roadmap

| Phase | Timeline | Status |
|-------|----------|--------|
| MVP (auth, exercises, tracking, analytics) | Q1 2026 | ✅ Done |
| AI Pose Detection (MediaPipe WebAssembly) | Q2 2026 | 🔄 In Dev |
| Physio Protocols + B2B Clinic Dashboard | Q3 2026 | 📋 Planned |
| ASEAN Expansion + Mobile App | Q4 2026 | 📋 Planned |

---

## Team

**Team Catalyst** — Universitas Airlangga · NVC 2026

---

*MotionMate — Recover smarter, move better, feel stronger.*
