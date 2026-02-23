from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import db, Student, Subject, Period, Attendance
from datetime import datetime

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
                    date=datetime.today(),
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


# -----------------------------------
# Create Period (Step 1)
# -----------------------------------
@attendance_bp.route('/select-period', methods=['GET', 'POST'])
@login_required
def select_period():

    if request.method == 'POST':
        date = request.form['date']
        subject_id = request.form['subject']
        teacher_id = request.form['teacher']
        period_number = request.form['period_number']

        period = Period(
            date=date,
            subject_id=subject_id,
            teacher_id=teacher_id,
            period_number=period_number
        )

        db.session.add(period)
        db.session.commit()

        return redirect(url_for('attendance.mark_attendance', period_id=period.id))

    subjects = Subject.query.all()
    teachers = teachers.query.all()

    return render_template('select_period.html',
                           subjects=subjects,
                           teachers=teachers)

# -----------------------------------
# Mark Attendance (Step 2)
# -----------------------------------
@attendance_bp.route('/mark-attendance/<int:period_id>', methods=['GET', 'POST'])
@login_required
def mark_attendance(period_id):

    period = Period.query.get_or_404(period_id)
    students = Student.query.all()

    if request.method == 'POST':
        for student in students:
            status = request.form.get(f'status_{student.id}')

            attendance = Attendance(
                student_id=student.id,
                period_id=period.id,
                status=status
            )
            db.session.add(attendance)

        db.session.commit()
        flash("Attendance saved successfully!")
        return redirect(url_for('dashboard'))

    return render_template('mark_attendance.html',
                           students=students,
                           period=period)


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
