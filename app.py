from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your-secret-key"

@app.before_request
def require_login():
    if request.endpoint != "login" and request.endpoint != "register":
        if session.get("user_id") is None:
            return redirect("/login")

@app.route("/")
def index():

    connection = sqlite3.connect("shipsafe.db")

    projects = connection.execute("SELECT * FROM projects WHERE user_id = ?", (session["user_id"],)).fetchall()
    connection.close()

    return render_template("index.html", projects=projects)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        connection = sqlite3.connect("shipsafe.db")
        connection.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password))

        connection.commit()

        user = connection.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)).fetchone()
        
        connection.close()

        session["user_id"] = user[0]

        return redirect("/")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        connection = sqlite3.connect("shipsafe.db")
        user = connection.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()

        if user is None:
            connection.close()
            return render_template("login.html", error="Invalid username or password")

        connection.close()

        session["user_id"] = user[0]

        return redirect("/")

    return render_template("login.html")

@app.route("/projects", methods=["GET", "POST"])
def projects():
    if request.method == "POST":
        project_name = request.form.get("project_name")

        connection = sqlite3.connect("shipsafe.db")

        connection.execute(
            "INSERT INTO projects (name, user_id) VALUES (?, ?) ",
            (project_name, session["user_id"])
        )
        connection.commit()
        project_id = connection.execute("SELECT id FROM projects WHERE name = ? AND user_id = ?", (project_name, session["user_id"])).fetchone()[0]

        connection.close()

        return redirect(f"/projects/{project_id}")

    return render_template("projects.html")


@app.route("/projects/<int:project_id>")
def project(project_id):
    connection = sqlite3.connect("shipsafe.db")

    project = connection.execute(
        "SELECT * FROM projects WHERE id = ? AND user_id = ?",
        (project_id, session["user_id"])
    ).fetchone()

    flags = connection.execute(
    "SELECT * FROM flags WHERE project_id = ?",
    (project_id,)
    ).fetchall()

    connection.close()

    return render_template("project.html", project=project, flags=flags)

@app.route("/projects/<int:project_id>/flags", methods=["POST"])
def create_flag(project_id):
    flag_name = request.form.get("flag_name")

    connection = sqlite3.connect("shipsafe.db")
    project = connection.execute("SELECT id FROM projects WHERE id = ? AND user_id = ?", (project_id, session["user_id"])).fetchone()
    
    if project is None:
        return render_template("projects.html", error="Project not found or you do not have permission to access it.")
    
    connection.execute("INSERT INTO flags (name, project_id) VALUES (?, ?)", (flag_name, project_id))
    connection.commit()
    connection.close()

    return redirect(f"/projects/{project_id}")

@app.route("/projects/<int:project_id>/flags/<int:flag_id>/toggle", methods=["POST"])
def toggle_flag(project_id, flag_id):
    connection = sqlite3.connect("shipsafe.db")

    status = connection.execute("SELECT enabled FROM flags JOIN projects ON flags.project_id = projects.id WHERE flags.id = ? AND projects.id = ? AND projects.user_id = ?", (flag_id, project_id, session["user_id"])).fetchone()

    if status is None:
        connection.close()
        return render_template("projects.html", error="Flag not found or you do not have permission to access it.")

    if status[0] == 0:
        connection.execute("UPDATE flags SET enabled = 1 WHERE id = ? AND project_id = ?", (flag_id, project_id))

    else:
        connection.execute("UPDATE flags SET enabled = 0 WHERE id = ? AND project_id = ?", (flag_id, project_id))

    connection.commit()
    connection.close()

    return redirect(f"/projects/{project_id}")

@app.route("/projects/<int:project_id>/flags/<int:flag_id>/delete", methods=["POST"])
def delete_flag(project_id, flag_id):
    connection = sqlite3.connect("shipsafe.db")
    deleted = connection.execute("DELETE FROM flags WHERE flags.id = ? AND flags.project_id = ? AND flags.project_id IN (SELECT id FROM projects WHERE user_id = ?)", (flag_id, project_id, session["user_id"]))
    if deleted.rowcount == 0:
        connection.close()
        return render_template("projects.html", error="Flag not found or you do not have permission to access it.")
    
    connection.commit()
    connection.close()

    return redirect(f"/projects/{project_id}")
    