from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "smart_attendance_key"

# ---------- DATABASE CONNECTION ----------
def get_db():
    return sqlite3.connect("database.db")

# ---------- CREATE TABLES ----------
def init_db():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll_no TEXT,
        department TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        status TEXT
    )
    """)

    con.commit()
    con.close()

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        con = get_db()
        cur = con.cursor()

        # ✅ Fetch user by username only
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        con.close()

        # ✅ Password verification
        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["role"] = user[3]

            if user[3] == "admin":
                return redirect("/admin")
            else:
                return redirect("/student")
        else:
            return "Invalid username or password"

    return render_template("login.html")


# ---------- ADMIN DASHBOARD ----------
@app.route("/admin")
def admin():
    return render_template("admin_dashboard.html")

# ---------- STUDENT DASHBOARD ----------
@app.route("/student")
def student():
    return render_template("student_dashboard.html")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- ADD STUDENT ----------
@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll_no"]
        dept = request.form["department"]

        con = get_db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO students(name, roll_no, department) VALUES (?,?,?)",
            (name, roll, dept)
        )
        con.commit()
        con.close()

        return redirect("/admin")

    return render_template("add_student.html")

# ---------- VIEW STUDENTS ----------
@app.route("/students")
def students():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    con.close()

    return render_template("students.html", students=data)

# ---------- EDIT STUDENT ----------
@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    con = get_db()
    cur = con.cursor()

    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll_no"]
        dept = request.form["department"]

        cur.execute(
            "UPDATE students SET name=?, roll_no=?, department=? WHERE id=?",
            (name, roll, dept, id)
        )
        con.commit()
        con.close()
        return redirect("/students")

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    con.close()

    return render_template("edit_student.html", student=student)


# ---------- DELETE STUDENT ----------
@app.route("/delete_student/<int:id>")
def delete_student(id):
    con = get_db()
    cur = con.cursor()

    cur.execute("DELETE FROM students WHERE id=?", (id,))
    con.commit()
    con.close()

    return redirect("/students")

# ---------- MARK ATTENDANCE ----------
@app.route("/mark_attendance", methods=["GET", "POST"])
def mark_attendance():
    con = get_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    if request.method == "POST":
        today = date.today().isoformat()

        for s in students:
            status = request.form.get(str(s[0]))
            cur.execute(
                "INSERT INTO attendance(student_id, date, status) VALUES (?,?,?)",
                (s[0], today, status)
            )

        con.commit()
        con.close()
        return redirect("/admin")

    con.close()
    return render_template("mark_attendance.html", students=students)

# ---------- ATTENDANCE REPORT ----------
@app.route("/attendance_report")
def attendance_report():
    con = get_db()
    cur = con.cursor()

    cur.execute("""
        SELECT s.id, s.name, s.roll_no,
               COUNT(a.id) AS total,
               SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) AS present
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
        GROUP BY s.id
    """)

    data = cur.fetchall()
    con.close()

    return render_template("attendance_report.html", report=data)

# ---------- RUN SERVER (ALWAYS LAST) ----------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)

