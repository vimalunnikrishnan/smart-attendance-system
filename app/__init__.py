from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(__name__)

    # Secret Key
    app.config["SECRET_KEY"] = "smart-attendance-secret"

    # ✅ Database Configuration (FIXED)
    if os.environ.get("DATABASE_URL"):
        database_url = os.environ.get("DATABASE_URL")

    # Fix old postgres:// issue
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"sslmode": "require"}
    }

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register Blueprints
    from app.auth import auth_bp
    from app.student import student_bp
    from app.attendance_backup import attendance_bp
    from app.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print("Database initialization skipped:", e)

    return app