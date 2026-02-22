from flask import Blueprint, render_template
from flask_login import login_required
from datetime import date
from app.models import Student, Attendance

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def dashboard():

    total_students = Student.query.count()
    total_attendance = Attendance.query.count()

    today_attendance = Attendance.query.filter_by(
        date=date.today()
    ).count()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_attendance=total_attendance,
        today_attendance=today_attendance
    )
