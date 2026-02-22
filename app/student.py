from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Student

student_bp = Blueprint("student", __name__)


@student_bp.route("/students")
@login_required
def students():
    students = Student.query.all()
    return render_template("students.html", students=students)


@student_bp.route("/add-student", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "POST":
        name = request.form.get("name")
        roll_no = request.form.get("roll_no")

        if Student.query.filter_by(roll_no=roll_no).first():
            flash("Roll number already exists")
            return redirect(url_for("student.add_student"))

        student = Student(name=name, roll_no=roll_no)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for("student.students"))

    return render_template("add_student.html")


@student_bp.route("/edit-student/<int:id>", methods=["GET", "POST"])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == "POST":
        student.name = request.form.get("name")
        student.roll_no = request.form.get("roll_no")
        db.session.commit()
        return redirect(url_for("student.students"))

    return render_template("edit_student.html", student=student)


@student_bp.route("/delete-student/<int:id>")
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("student.students"))
