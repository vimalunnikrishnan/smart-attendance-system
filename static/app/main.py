from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint("main", __name__)

@main.route("/")
@login_required
def index():
    return render_template("dashboard.html")

@main.route("/mark-attendance")
@login_required
def mark_attendance():
    return render_template("mark_attendance.html")

@main.route("/attendance-report")
@login_required
def attendance_report():
    return render_template("attendance_report.html")
