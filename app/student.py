from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Student

student_bp = Blueprint("student", __name__)


# ---------------- VIEW ALL STUDENTS ----------------
@student_bp.route("/students")
@login_required
def students():
    students = Student.query.all()
    return render_template("students.html", students=students)


# ---------------- ADD STUDENT ----------------
@student_bp.route("/add-student", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "POST":
        name = request.form.get("name")
        roll_number = request.form.get("roll_number")
        class_name = request.form.get("class_name")

        # Check duplicate roll number
        if Student.query.filter_by(roll_number=roll_number).first():
            flash("Roll number already exists")
            return redirect(url_for("student.add_student"))

        new_student = Student(
            name=name,
            roll_number=roll_number,
            class_name=class_name
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("student.students"))

    return render_template("add_student.html")


# ---------------- EDIT STUDENT ----------------
@student_bp.route("/edit-student/<int:id>", methods=["GET", "POST"])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == "POST":
        student.name = request.form.get("name")
        student.roll_number = request.form.get("roll_number")
        student.class_name = request.form.get("class_name")

        db.session.commit()
        return redirect(url_for("student.students"))

    return render_template("edit_student.html", student=student)


# ---------------- DELETE STUDENT ----------------
@student_bp.route("/delete-student/<int:id>")
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return redirect(url_for("student.students"))