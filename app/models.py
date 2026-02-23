from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# -------------------------
# User Model (Teacher/Admin)
# -------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="teacher")  # admin / teacher


# -------------------------
# Student Model
# -------------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    class_name = db.Column(db.String(100), nullable=False)


# -------------------------
# Subject Model
# -------------------------
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(150), nullable=False)


# -------------------------
# Period Model (NEW)
# -------------------------
class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    period_number = db.Column(db.Integer, nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    subject = db.relationship('Subject', backref='periods')
    teacher = db.relationship('User', backref='periods')


# -------------------------
# Attendance Model (Updated)
# -------------------------
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'), nullable=False)

    status = db.Column(db.String(20), nullable=False)  # Present / Absent

    student = db.relationship('Student', backref='attendance_records')
    period = db.relationship('Period', backref='attendance_records')