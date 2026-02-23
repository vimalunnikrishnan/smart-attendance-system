from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .models import db, Student, Subject, User, Period, Attendance
from datetime import datetime

attendance_bp = Blueprint("attendance", __name__)


# =========================
# STEP 1 — SELECT PERIOD
# =========================
@attendance_bp.route('/select-period', methods=['GET', 'POST'])
@login_required
def select_period():

    if request.method == 'POST':
        date = request.form['date']
        subject_id = request.form['subject']
        period_number = request.form['period_number']

        period = Period(
            date=datetime.strptime(date, "%Y-%m-%d"),
            subject_id=subject_id,
            teacher_id=request.form['teacher'],
            period_number=period_number
        )

        db.session.add(period)
        db.session.commit()

        return redirect(url_for('attendance.mark_attendance', period_id=period.id))

    subjects = Subject.query.all()
    teachers = User.query.filter_by(role="teacher").all()

    return render_template(
        'select_period.html',
        subjects=subjects,
        teachers=teachers
    )


# =========================
# STEP 2 — MARK ATTENDANCE
# =========================
@attendance_bp.route('/mark-attendance/<int:period_id>', methods=['GET', 'POST'])
@login_required
def mark_attendance(period_id):

    period = Period.query.get_or_404(period_id)
    students = Student.query.all()

    if request.method == 'POST':

        for student in students:
            status = request.form.get(f'status_{student.id}')

            if status:
                attendance = Attendance(
                    student_id=student.id,
                    period_id=period.id,
                    status=status
                )
                db.session.add(attendance)

        db.session.commit()
        flash("Attendance saved successfully!")
        return redirect(url_for('attendance.attendance_report'))

    return render_template(
        'mark_attendance.html',
        students=students,
        period=period
    )


# =========================
# ATTENDANCE REPORT
# =========================
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
    ).select_from(Attendance) \
     .join(Student, Attendance.student_id == Student.id) \
     .join(Period, Attendance.period_id == Period.id) \
     .join(Subject, Period.subject_id == Subject.id) \
     .order_by(Period.date.desc()) \
     .all()

    return render_template(
        "attendance_report.html",
        records=records
    )