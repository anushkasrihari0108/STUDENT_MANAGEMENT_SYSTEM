from flask import Flask, render_template, request, redirect, session
import sqlite3
import re

app = Flask(__name__)
app.secret_key = "secret123"

DB = "students.db"

# ---------- DATABASE ---------- #
def connect_db():
    return sqlite3.connect(DB)

def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll TEXT PRIMARY KEY,
            name TEXT,
            marks INTEGER,
            attendance INTEGER
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- HELPER ---------- #
def calculate_grade(marks):
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 50:
        return "C"
    return "F"

def get_status(marks, attendance):
    if marks < 40 or attendance < 50:
        return "Low ⚠️"
    return "Good"

# ---------- LOGIN ---------- #
@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/dashboard")
        else:
            error = "Invalid Credentials"

    return render_template("login.html", error=error)

# ---------- DASHBOARD ---------- #
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html")

# ---------- ADD STUDENT ---------- #
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if "user" not in session:
        return redirect("/")

    error = None

    if request.method == "POST":
        roll = request.form.get("roll", "").strip()
        name = request.form.get("name", "").strip()
        marks = request.form.get("marks", "").strip()
        attendance = request.form.get("attendance", "").strip()

        # -------- VALIDATION -------- #
        if not roll:
            error = "Roll number is required"

        elif not roll.isdigit():
            error = "Roll must be numeric"

        elif not name:
            error = "Name is required"

        elif not re.match("^[A-Za-z ]+$", name):
            error = "Name must contain only letters"

        elif not marks.isdigit():
            error = "Marks must be numeric"

        elif int(marks) < 0 or int(marks) > 100:
            error = "Marks must be between 0 and 100"

        elif not attendance.isdigit():
            error = "Attendance must be numeric"

        elif int(attendance) < 0 or int(attendance) > 100:
            error = "Attendance must be between 0 and 100"

        else:
            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO students VALUES (?, ?, ?, ?)",
                    (roll, name, int(marks), int(attendance))
                )

                conn.commit()
                conn.close()

                return redirect("/view")

            except sqlite3.IntegrityError:
                error = "Roll already exists"

            except Exception as e:
                error = str(e)

    return render_template("add.html", error=error)

# ---------- VIEW ---------- #
@app.route("/view")
def view():
    if "user" not in session:
        return redirect("/")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    conn.close()

    students = []
    for s in data:
        roll, name, marks, attendance = s
        students.append((
            roll,
            name,
            marks,
            attendance,
            calculate_grade(marks),
            get_status(marks, attendance)
        ))

    return render_template("view.html", students=students)

# ---------- EDIT ---------- #
@app.route("/edit/<roll>", methods=["GET", "POST"])
def edit_student(roll):
    if "user" not in session:
        return redirect("/")

    conn = connect_db()
    cursor = conn.cursor()
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        marks = request.form.get("marks", "").strip()
        attendance = request.form.get("attendance", "").strip()

        if not name:
            error = "Name is required"

        elif not re.match("^[A-Za-z ]+$", name):
            error = "Name must contain only letters"

        elif not marks.isdigit():
            error = "Marks must be numeric"

        elif int(marks) < 0 or int(marks) > 100:
            error = "Marks must be between 0 and 100"

        elif not attendance.isdigit():
            error = "Attendance must be numeric"

        elif int(attendance) < 0 or int(attendance) > 100:
            error = "Attendance must be between 0 and 100"

        else:
            try:
                cursor.execute("""
                    UPDATE students
                    SET name=?, marks=?, attendance=?
                    WHERE roll=?
                """, (name, int(marks), int(attendance), roll))

                conn.commit()
                conn.close()

                return redirect("/view")

            except Exception as e:
                error = str(e)

    cursor.execute("SELECT * FROM students WHERE roll=?", (roll,))
    student = cursor.fetchone()
    conn.close()

    return render_template("edit.html", student=student, error=error)

# ---------- DELETE ---------- #
@app.route("/delete/<roll>")
def delete_student(roll):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE roll=?", (roll,))
    conn.commit()
    conn.close()

    return redirect("/view")


# ---------- GRAPH ---------- #
@app.route("/graph")
def graph():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, marks FROM students")
    data = cursor.fetchall()
    conn.close()

    names = [row[0] for row in data]
    marks = [row[1] for row in data]

    return render_template("graph.html", names=names, marks=marks)

# ---------- LOGOUT ---------- #
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- RUN ---------- #
if __name__ == "__main__":
    app.run(debug=True)