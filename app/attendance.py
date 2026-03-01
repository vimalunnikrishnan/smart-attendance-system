from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, date
from app import db
from app.models import Student, Subject, User, Period, Attendance

attendance_bp = Blueprint("attendance", __name__)


# ====================================
# STEP 1 — SELECT / CREATE PERIOD
# ====================================
@attendance_bp.route("/select-period", methods=["GET", "POST"])
@login_required
def select_period():

    if request.method == "POST":

        selected_date = request.form.get("date")
        subject_id = request.form.get("subject")
        period_number = request.form.get("period_number")

        # Convert string to date
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

        # Check if period already exists
        existing_period = Period.query.filter_by(
            date=selected_date,
            subject_id=subject_id,
            period_number=period_number
        ).first()

        if existing_period:
            return redirect(
                url_for("attendance.mark_attendance", period_id=existing_period.id)
            )

        # Create new period
        new_period = Period(
            date=selected_date,
            subject_id=subject_id,
            teacher_id=current_user.id,
            period_number=period_number
        )

        db.session.add(new_period)
        db.session.commit()

        return redirect(
            url_for("attendance.mark_attendance", period_id=new_period.id)
        )

    subjects = Subject.query.all()

    return render_template(
        "select_period.html",
        subjects=subjects
    )


# ====================================
# STEP 2 — MARK ATTENDANCE
# ====================================
@attendance_bp.route("/mark-attendance/<int:period_id>", methods=["GET", "POST"])
@login_required
def mark_attendance(period_id):

    period = Period.query.get_or_404(period_id)
    students = Student.query.all()

    if request.method == "POST":

        for student in students:

            status = request.form.get(f"status_{student.id}")

            if status:

                # Prevent duplicate attendance
                existing_record = Attendance.query.filter_by(
                    student_id=student.id,
                    period_id=period.id
                ).first()

                if not existing_record:
                    attendance = Attendance(
                        student_id=student.id,
                        period_id=period.id,
                        status=status
                    )
                    db.session.add(attendance)

        db.session.commit()
        flash("Attendance saved successfully!")

        return redirect(url_for("attendance.attendance_report"))

    return render_template(
        "mark_attendance.html",
        students=students,
        period=period
    )


# ====================================
# ATTENDANCE REPORT
# ====================================
@attendance_bp.route("/attendance-report")
@login_required
def attendance_report():

    records = db.session.query(
        Student.name,
        Student.roll_number,
        Subject.subject_name,
        Period.date,
        Period.period_number,
        Attendance.status
    ).join(Attendance, Student.id == Attendance.student_id) \
     .join(Period, Attendance.period_id == Period.id) \
     .join(Subject, Period.subject_id == Subject.id) \
     .order_by(Period.date.desc()) \
     .all()

    return render_template(
        "attendance_report.html",
        records=records
    )