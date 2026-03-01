from . import db
from flask_login import UserMixin
from datetime import datetime


# -------------------------
# User Model (Teacher/Admin)
# -------------------------
class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="teacher")  # admin / teacher

    periods = db.relationship("Period", backref="teacher", lazy=True)


# -------------------------
# Student Model
# -------------------------
class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    class_name = db.Column(db.String(100), nullable=False)

    attendance_records = db.relationship(
        "Attendance",
        backref="student",
        cascade="all, delete",
        lazy=True
    )


# -------------------------
# Subject Model
# -------------------------
class Subject(db.Model):
    __tablename__ = "subject"

    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(150), nullable=False)

    periods = db.relationship(
        "Period",
        backref="subject",
        cascade="all, delete",
        lazy=True
    )


# -------------------------
# Period Model
# -------------------------
class Period(db.Model):
    __tablename__ = "period"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    period_number = db.Column(db.Integer, nullable=False)

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subject.id"),
        nullable=False
    )

    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    attendance_records = db.relationship(
        "Attendance",
        backref="period",
        cascade="all, delete",
        lazy=True
    )


# -------------------------
# Attendance Model
# -------------------------
class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    period_id = db.Column(
        db.Integer,
        db.ForeignKey("period.id"),
        nullable=False
    )

    status = db.Column(db.String(20), nullable=False)  # Present / Absent