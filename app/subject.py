from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Subject
from flask_login import login_required

subject_bp = Blueprint("subject", __name__)

@subject_bp.route("/subjects")
@login_required
def subjects():
    all_subjects = Subject.query.all()
    return render_template("subjects.html", subjects=all_subjects)


@subject_bp.route("/add-subject", methods=["GET", "POST"])
@login_required
def add_subject():
    if request.method == "POST":
        subject_name = request.form.get("subject_name")

        new_subject = Subject(subject_name=subject_name)
        db.session.add(new_subject)
        db.session.commit()

        return redirect(url_for("subject.subjects"))

    return render_template("add_subject.html")