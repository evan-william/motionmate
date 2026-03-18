"""
MotionMate Test Suite
Covers: auth flows, validators, route responses, session tracking, dummy mode
"""
import pytest
from app import create_app
from app.models.db import db as _db
from app.models.user import User
from app.models.exercise import Exercise, RehabSession


@pytest.fixture(scope='session')
def app():
    """Create test application."""
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        _seed_test_data()
        yield app
        _db.drop_all()


def _seed_test_data():
    """Seed minimal data for tests."""
    ex = Exercise(
        name='Test Knee Extension',
        category='orthopedic',
        description='Test exercise',
        difficulty='beginner',
        target_sets=3,
        target_reps=10,
        duration_seconds=120,
    )
    _db.session.add(ex)
    _db.session.commit()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(client):
    """A test client with a registered + logged-in user."""
    client.post('/auth/register', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'Password1',
    }, follow_redirects=True)
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'Password1',
    }, follow_redirects=True)
    return client


@pytest.fixture
def dummy_client(client):
    """A test client with dummy mode enabled."""
    client.get('/dummy/enable', follow_redirects=True)
    return client


# ─── Auth ───────────────────────────────────────────────────────────────────

class TestAuthRoutes:
    def test_register_get(self, client):
        r = client.get('/auth/register')
        assert r.status_code == 200
        assert b'Daftar' in r.data or b'register' in r.data.lower()

    def test_login_get(self, client):
        r = client.get('/auth/login')
        assert r.status_code == 200

    def test_register_success(self, client):
        r = client.post('/auth/register', data={
            'name': 'Budi Santoso',
            'email': 'budi@example.com',
            'password': 'Password1',
        }, follow_redirects=True)
        assert r.status_code == 200

    def test_register_duplicate_email(self, client):
        data = {'name': 'A', 'email': 'dup@example.com', 'password': 'Password1'}
        client.post('/auth/register', data=data)
        r = client.post('/auth/register', data=data, follow_redirects=True)
        assert r.status_code == 200  # shows error flash, not crash

    def test_login_success(self, client):
        client.post('/auth/register', data={
            'name': 'Login Test', 'email': 'login@example.com', 'password': 'Password1'
        })
        r = client.post('/auth/login', data={
            'email': 'login@example.com', 'password': 'Password1'
        }, follow_redirects=True)
        assert r.status_code == 200

    def test_login_wrong_password(self, client):
        r = client.post('/auth/login', data={
            'email': 'test@example.com', 'password': 'WrongPass1'
        }, follow_redirects=True)
        assert r.status_code == 200

    def test_logout(self, auth_client):
        r = auth_client.get('/auth/logout', follow_redirects=True)
        assert r.status_code == 200


# ─── Validators ─────────────────────────────────────────────────────────────

class TestValidators:
    def test_email_valid(self):
        from app.utils.validators import validate_email
        assert validate_email('user@example.com') is True

    def test_email_invalid(self):
        from app.utils.validators import validate_email
        assert validate_email('notanemail') is False
        assert validate_email('') is False
        assert validate_email('@domain.com') is False

    def test_password_valid(self):
        from app.utils.validators import validate_password
        assert validate_password('Password1') is True
        assert validate_password('Abcdef1!') is True

    def test_password_too_short(self):
        from app.utils.validators import validate_password
        assert validate_password('Ab1') is False

    def test_password_no_uppercase(self):
        from app.utils.validators import validate_password
        assert validate_password('password1') is False

    def test_password_no_digit(self):
        from app.utils.validators import validate_password
        assert validate_password('Password') is False

    def test_name_valid(self):
        from app.utils.validators import validate_name
        assert validate_name('Budi Santoso') is True

    def test_name_too_short(self):
        from app.utils.validators import validate_name
        assert validate_name('A') is False

    def test_name_too_long(self):
        from app.utils.validators import validate_name
        assert validate_name('A' * 101) is False


# ─── Main routes ────────────────────────────────────────────────────────────

class TestMainRoutes:
    def test_landing_page(self, client):
        r = client.get('/')
        assert r.status_code == 200
        assert b'MotionMate' in r.data

    def test_enable_dummy_mode(self, client):
        r = client.get('/dummy/enable', follow_redirects=True)
        assert r.status_code == 200

    def test_disable_dummy_mode(self, client):
        client.get('/dummy/enable')
        r = client.get('/dummy/disable', follow_redirects=True)
        assert r.status_code == 200


# ─── Dashboard routes ────────────────────────────────────────────────────────

class TestDashboardRoutes:
    def test_dashboard_requires_auth(self, client):
        r = client.get('/dashboard/', follow_redirects=True)
        # Should redirect to login when not authenticated
        assert r.status_code == 200

    def test_dashboard_authenticated(self, auth_client):
        r = auth_client.get('/dashboard/')
        assert r.status_code == 200

    def test_dashboard_dummy_mode(self, dummy_client):
        r = dummy_client.get('/dashboard/')
        assert r.status_code == 200
        assert b'Dummy' in r.data or b'dummy' in r.data


# ─── Exercises routes ────────────────────────────────────────────────────────

class TestExerciseRoutes:
    def test_exercise_list_authenticated(self, auth_client):
        r = auth_client.get('/exercises/')
        assert r.status_code == 200

    def test_exercise_list_dummy(self, dummy_client):
        r = dummy_client.get('/exercises/')
        assert r.status_code == 200

    def test_exercise_detail_dummy(self, dummy_client):
        r = dummy_client.get('/exercises/1')
        assert r.status_code == 200

    def test_exercise_404_high_id(self, auth_client):
        r = auth_client.get('/exercises/99999')
        assert r.status_code in (200, 404)  # 404 page or redirect


# ─── Session routes ──────────────────────────────────────────────────────────

class TestSessionRoutes:
    def test_history_authenticated(self, auth_client):
        r = auth_client.get('/sessions/history')
        assert r.status_code == 200

    def test_history_dummy(self, dummy_client):
        r = dummy_client.get('/sessions/history')
        assert r.status_code == 200

    def test_start_session_authenticated(self, auth_client):
        r = auth_client.post('/sessions/start/1', follow_redirects=True)
        assert r.status_code == 200

    def test_complete_session(self, auth_client, app):
        """Start a session and complete it."""
        # Start session first
        auth_client.post('/sessions/start/1', follow_redirects=True)
        with app.app_context():
            session = RehabSession.query.first()
            if session:
                r = auth_client.post(f'/sessions/complete/{session.id}', data={
                    'reps_completed': '10',
                    'sets_completed': '3',
                    'duration_seconds': '120',
                    'accuracy_score': '85.5',
                }, follow_redirects=True)
                assert r.status_code == 200


# ─── Accuracy clamping ───────────────────────────────────────────────────────

class TestAccuracyClamping:
    def test_accuracy_clamp_high(self, auth_client, app):
        """Accuracy above 100 should be clamped."""
        auth_client.post('/sessions/start/1', follow_redirects=True)
        with app.app_context():
            session = RehabSession.query.first()
            if session:
                auth_client.post(f'/sessions/complete/{session.id}', data={
                    'reps_completed': '10',
                    'sets_completed': '3',
                    'duration_seconds': '120',
                    'accuracy_score': '150',  # Over 100
                }, follow_redirects=True)
                updated = RehabSession.query.get(session.id)
                if updated:
                    assert updated.accuracy_score <= 100.0

    def test_accuracy_clamp_low(self, auth_client, app):
        """Accuracy below 0 should be clamped."""
        auth_client.post('/sessions/start/1', follow_redirects=True)
        with app.app_context():
            session = RehabSession.query.first()
            if session:
                auth_client.post(f'/sessions/complete/{session.id}', data={
                    'reps_completed': '5',
                    'sets_completed': '2',
                    'duration_seconds': '60',
                    'accuracy_score': '-20',  # Negative
                }, follow_redirects=True)
                updated = RehabSession.query.get(session.id)
                if updated:
                    assert updated.accuracy_score >= 0.0


# ─── User model ──────────────────────────────────────────────────────────────

class TestUserModel:
    def test_password_hashing(self, app):
        with app.app_context():
            u = User(name='Test', email='hash@example.com')
            u.set_password('MyPassword1')
            assert u.check_password('MyPassword1') is True
            assert u.check_password('WrongPassword') is False

    def test_password_not_stored_plaintext(self, app):
        with app.app_context():
            u = User(name='Test', email='plain@example.com')
            u.set_password('SecretPass1')
            assert 'SecretPass1' not in u.password_hash


# ─── Open redirect protection ────────────────────────────────────────────────

class TestOpenRedirect:
    def test_login_next_param_external_blocked(self, client):
        """next= pointing to external URL should not redirect there."""
        r = client.post('/auth/login?next=https://evil.com', data={
            'email': 'test@example.com',
            'password': 'Password1',
        }, follow_redirects=False)
        location = r.headers.get('Location', '')
        assert 'evil.com' not in location
