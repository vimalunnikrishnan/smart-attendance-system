from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

# ---------------- REGISTER ----------------

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("Username already exists")
            return redirect(url_for("auth.register"))

        hashed = generate_password_hash(password)

        user = User(username=username, password_hash=hashed)
        db.session.add(user)
        db.session.commit()

        flash("Registered successfully — please login")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        from werkzeug.security import generate_password_hash, check_password_hash
        login_user(user)
        return redirect(url_for("student.students"))

        flash("Invalid username or password")

    return render_template("login.html")


# ---------------- LOGOUT ----------------

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
