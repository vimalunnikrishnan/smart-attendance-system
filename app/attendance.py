from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from datetime import date

from app import db
from app.models import Student, Subject, Attendance


attendance_bp = Blueprint("attendance", __name__)


# =========================
# MARK ATTENDANCE
# =========================
@attendance_bp.route('/mark-attendance', methods=['GET', 'POST'])
@login_required
def mark_attendance():

    students = Student.query.all()
    subjects = Subject.query.all()

    if request.method == 'POST':

        subject_id = request.form.get('subject_id')

        if not subject_id:
            return "Subject not selected"

        for student in students:
            status = request.form.get(str(student.id))

            if status:
                record = Attendance(
                    student_id=student.id,
                    subject_id=subject_id,
                    date=date.today(),
                    status=status
                )
                db.session.add(record)

        db.session.commit()
        return redirect(url_for("attendance.attendance_report"))

    return render_template(
        "mark_attendance.html",
        students=students,
        subjects=subjects
    )


# =========================
# ATTENDANCE REPORT
# =========================
@attendance_bp.route("/attendance-report")
@login_required
def attendance_report():

    # ✅ FIXED JOIN QUERY — matches your model fields
    records = db.session.query(
        Student.name,
        Student.roll_no,
        Subject.subject_name,   # ← FIXED HERE
        Attendance.date,
        Attendance.status
    ).select_from(Attendance) \
     .join(Student, Attendance.student_id == Student.id) \
     .join(Subject, Attendance.subject_id == Subject.id) \
     .order_by(Attendance.date.desc()) \
     .all()

    # -------------------------
    # Student percentage report
    # -------------------------
    students = Student.query.all()
    report = []

    for student in students:

        total = Attendance.query.filter_by(
            student_id=student.id
        ).count()

        present = Attendance.query.filter_by(
            student_id=student.id,
            status="Present"
        ).count()

        percentage = 0
        if total > 0:
            percentage = round((present / total) * 100, 2)

        report.append({
            "name": student.name,
            "roll": student.roll_no,
            "percentage": percentage
        })

    return render_template(
        "attendance_report.html",
        records=records,
        report=report
    )
