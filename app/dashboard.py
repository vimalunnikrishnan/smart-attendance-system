from flask import Blueprint, render_template
from flask_login import login_required
from datetime import date
from app.models import Student, Attendance, Period
from app import db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def dashboard():

    # Total students
    total_students = Student.query.count()

    # Total attendance records
    total_attendance = Attendance.query.count()

    # Today's attendance (JOIN with Period)
    today_attendance = db.session.query(Attendance).join(Period).filter(
        Period.date == date.today()
    ).count()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_attendance=total_attendance,
        today_attendance=today_attendance
    )