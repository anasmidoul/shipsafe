from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import secrets
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

@app.before_request
def require_login():
    if request.endpoint != "login" and request.endpoint != "register" and request.endpoint != "get_flag":
        if session.get("user_id") is None:
            return redirect("/login")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
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

        if not username or not password:
            return render_template("register.html", error="Username and password are required")

        password = generate_password_hash(password)

        connection = sqlite3.connect("shipsafe.db")

        name = connection.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchone()

        if name is not None:
            connection.close()
            return render_template("register.html", error="Username already exists")

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

        if not username or not password:
            return render_template("login.html", error="Username and password are required")

        connection = sqlite3.connect("shipsafe.db")

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if user is None:
            connection.close()
            return render_template("login.html", error="Invalid username or password")

        if not check_password_hash(user[2], password):
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

        if not project_name:
            return render_template("projects.html", error="Project name is required")

        connection = sqlite3.connect("shipsafe.db")

        project = connection.execute("SELECT * FROM projects WHERE name = ? AND user_id = ?", (project_name, session["user_id"])).fetchone()

        if project:
            connection.close()
            return render_template("projects.html", error="Project already exists")

        api_key = secrets.token_urlsafe(32)

        connection.execute(
            "INSERT INTO projects (name, user_id, api_key) VALUES (?, ?, ?)",
            (project_name, session["user_id"], api_key)
        )
        connection.commit()
        project = connection.execute("SELECT * FROM projects WHERE name = ? AND user_id = ?", (project_name, session["user_id"])).fetchone()

        connection.close()

        return redirect(f"/projects/{project[0]}")

    return render_template("projects.html")


@app.route("/projects/<int:project_id>")
def project(project_id):
    connection = sqlite3.connect("shipsafe.db")

    project = connection.execute(
        "SELECT * FROM projects WHERE id = ? AND user_id = ?",
        (project_id, session["user_id"])).fetchone()

    if project is None: 
        connection.close()
        return render_template("projects.html", error="Project not found or you do not have permission to access it.")

    flags = connection.execute(
    "SELECT * FROM flags WHERE project_id = ?",
    (project_id,)
    ).fetchall()

    connection.close()

    return render_template("project.html", project=project, flags=flags, api_key=project[3])

@app.route("/projects/<int:project_id>/flags", methods=["POST"])
def create_flag(project_id):
    flag_name = request.form.get("flag_name")

    connection = sqlite3.connect("shipsafe.db")

    project = connection.execute("SELECT id FROM projects WHERE id = ? AND user_id = ?", (project_id, session["user_id"])).fetchone()

    if project is None:
        connection.close()
        return render_template("projects.html", error="Project not found or you do not have permission to access it.")
    
    flags = connection.execute(
        "SELECT * FROM flags WHERE project_id = ?",
        (project_id,)
        ).fetchall()

    if not flag_name:
        connection.close()
        return render_template("project.html", flags=flags, project=project, error="Flag name is required")

    
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

@app.route("/api/projects/<int:project_id>/flags/<flag_name>")
def get_flag(project_id, flag_name):

    api_key = request.headers.get("X-API-Key")

    if not api_key:
        return {"error": "API key is required"}, 401

    if not project_id or not flag_name:
        return {"error": "Project ID and flag name are required"}, 400

    connection = sqlite3.connect("shipsafe.db")

    project_api_key = connection.execute(
    "SELECT api_key FROM projects WHERE id = ?", (project_id,)).fetchone()

    if not project_api_key:
        connection.close()
        return {"error": "Project not found"}, 404

    if api_key != project_api_key[0]:
        connection.close()
        return {"error": "Invalid API key"}, 403

    result = connection.execute("SELECT enabled FROM flags WHERE project_id = ? AND name = ?", (project_id, flag_name)).fetchone()

    if not result:
        connection.close()
        return {"error": "Flag not found"}, 404

    connection.close()
    return {"enabled": result[0]}

if __name__ == "__main__":
    app.run(debug=True)