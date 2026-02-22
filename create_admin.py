from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # check if admin already exists
    user = User.query.filter_by(username="admin").first()

    if not user:
        admin = User(username="admin")
        admin.set_password("admin123")  # login password
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created")
    else:
        print("ℹ️ Admin already exists")
