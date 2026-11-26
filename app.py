from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
import os
import secrets

app = Flask(__name__)
# No real secret is stored in source control. Set SECRET_KEY in the environment for deployment.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
DB_PATH = Path(__file__).with_name("obe.db")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
def init_db():
    with db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS outcomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            description TEXT NOT NULL,
            target REAL NOT NULL DEFAULT 60,
            FOREIGN KEY(course_id) REFERENCES courses(id)
        );
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            outcome_id INTEGER NOT NULL,
            score REAL NOT NULL,
            max_score REAL NOT NULL DEFAULT 100,
            UNIQUE(student_id, outcome_id),
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(outcome_id) REFERENCES outcomes(id)
        );
        """)
        if con.execute("SELECT COUNT(*) FROM courses").fetchone()[0] == 0:
            cur = con.execute("INSERT INTO courses(code,name) VALUES (?,?)",
                              ("BCA301", "Database Management Systems"))
            course_id = cur.lastrowid
            con.executemany(
                "INSERT INTO outcomes(course_id,code,description,target) VALUES (?,?,?,?)",
                [
                    (course_id, "CO1", "Explain database concepts and data models", 60),
                    (course_id, "CO2", "Design relational schemas using normalization", 65),
                    (course_id, "CO3", "Write SQL queries for data manipulation", 60),
                ])
            con.executemany("INSERT INTO students(roll_no,name) VALUES (?,?)", [
                ("BCA001", "Aarav Demo"), ("BCA002", "Diya Demo"),
                ("BCA003", "Kabir Demo"), ("BCA004", "Meera Demo")
            ])
            students = con.execute("SELECT id FROM students ORDER BY id").fetchall()
            outcomes = con.execute("SELECT id FROM outcomes ORDER BY id").fetchall()
            sample = [(students[0]["id"], outcomes[0]["id"], 78, 100),
                      (students[1]["id"], outcomes[0]["id"], 66, 100),
                      (students[2]["id"], outcomes[0]["id"], 52, 100),
                      (students[3]["id"], outcomes[0]["id"], 85, 100),
                      (students[0]["id"], outcomes[1]["id"], 72, 100),
                      (students[1]["id"], outcomes[1]["id"], 58, 100),
                      (students[2]["id"], outcomes[1]["id"], 67, 100),
                      (students[3]["id"], outcomes[1]["id"], 81, 100),
                      (students[0]["id"], outcomes[2]["id"], 88, 100),
                      (students[1]["id"], outcomes[2]["id"], 73, 100),
                      (students[2]["id"], outcomes[2]["id"], 62, 100),
                      (students[3]["id"], outcomes[2]["id"], 91, 100)]
            con.executemany(
                "INSERT INTO marks(student_id,outcome_id,score,max_score) VALUES (?,?,?,?)",
                sample)

@app.route("/")
def index():
    with db() as con:
        courses = con.execute("SELECT * FROM courses ORDER BY code").fetchall()
        students = con.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        outcomes = con.execute("""
            SELECT o.*, c.code AS course_code, c.name AS course_name
            FROM outcomes o JOIN courses c ON c.id=o.course_id
            ORDER BY c.code, o.code
        """).fetchall()
        results = []
        for o in outcomes:
            rows = con.execute("""
                SELECT score, max_score FROM marks WHERE outcome_id=?
            """, (o["id"],)).fetchall()
            if rows:
                avg = sum((r["score"] / r["max_score"]) * 100 for r in rows) / len(rows)
                achieved = sum(1 for r in rows if (r["score"] / r["max_score"]) * 100 >= o["target"])
                rate = achieved / len(rows) * 100
            else:
                avg, rate = 0, 0
            results.append({"outcome": o, "average": round(avg, 1),
                            "attainment": round(rate, 1), "count": len(rows)})
    return render_template("index.html", courses=courses, students=students,
                           results=results, outcome_count=len(outcomes))

@app.route("/courses", methods=["POST"])
def add_course():
    code = request.form.get("code", "").strip().upper()
    name = request.form.get("name", "").strip()
    if not code or not name:
        flash("Enter both course code and course name.", "error")
    else:
        try:
            with db() as con:
                con.execute("INSERT INTO courses(code,name) VALUES (?,?)", (code, name))
            flash("Course added.", "success")
        except sqlite3.IntegrityError:
            flash("That course code already exists.", "error")
    return redirect(url_for("index"))

@app.route("/outcomes", methods=["POST"])
def add_outcome():
    try:
        course_id = int(request.form["course_id"])
        code = request.form["code"].strip().upper()
        description = request.form["description"].strip()
        target = float(request.form["target"])
        if not code or not description or not 0 <= target <= 100:
            raise ValueError()
        with db() as con:
            con.execute("""INSERT INTO outcomes(course_id,code,description,target)
                           VALUES (?,?,?,?)""", (course_id, code, description, target))
        flash("Course outcome added.", "success")
    except (ValueError, KeyError, sqlite3.IntegrityError):
        flash("Please check the outcome details and target (0–100).", "error")
    return redirect(url_for("index"))

@app.route("/students", methods=["POST"])
def add_student():
    roll = request.form.get("roll_no", "").strip().upper()
    name = request.form.get("name", "").strip()
    if not roll or not name:
        flash("Enter roll number and student name.", "error")
    else:
        try:
            with db() as con:
                con.execute("INSERT INTO students(roll_no,name) VALUES (?,?)", (roll, name))
            flash("Student added.", "success")
        except sqlite3.IntegrityError:
            flash("That roll number already exists.", "error")
    return redirect(url_for("index"))

@app.route("/marks", methods=["POST"])
def add_mark():
    try:
        student_id = int(request.form["student_id"])
        outcome_id = int(request.form["outcome_id"])
        score = float(request.form["score"])
        max_score = float(request.form["max_score"])
        if max_score <= 0 or score < 0 or score > max_score:
            raise ValueError()
        with db() as con:
            con.execute("""INSERT INTO marks(student_id,outcome_id,score,max_score)
                           VALUES (?,?,?,?)
                           ON CONFLICT(student_id,outcome_id)
                           DO UPDATE SET score=excluded.score,max_score=excluded.max_score
                        """, (student_id, outcome_id, score, max_score))
        flash("Marks saved. Existing mark for this student/outcome is updated.", "success")
    except (ValueError, KeyError, sqlite3.IntegrityError):
        flash("Check student, outcome and marks. Score must be between 0 and maximum.", "error")
    return redirect(url_for("index"))

@app.route("/data")
def data():
    with db() as con:
        students = con.execute("SELECT * FROM students ORDER BY roll_no").fetchall()
        outcomes = con.execute("""
            SELECT o.*, c.code AS course_code FROM outcomes o
            JOIN courses c ON c.id=o.course_id ORDER BY c.code,o.code
        """).fetchall()
        marks = con.execute("""
            SELECT s.roll_no,s.name,o.code AS outcome_code,m.score,m.max_score
            FROM marks m JOIN students s ON s.id=m.student_id
            JOIN outcomes o ON o.id=m.outcome_id
            ORDER BY s.roll_no,o.code
        """).fetchall()
    return render_template("data.html", students=students, outcomes=outcomes, marks=marks)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
