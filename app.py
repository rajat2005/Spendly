from flask import Flask, render_template, request, redirect, url_for, flash, session
from database.db import get_db, init_db, seed_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Validation
        if not name or len(name) > 100:
            flash("Name must be between 1-100 characters.")
            return redirect(url_for("register"))

        if not email or "@" not in email:
            flash("Please enter a valid email address.")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return redirect(url_for("register"))

        # Check for duplicate email
        conn = get_db()
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()

        if existing:
            conn.close()
            flash("An account with this email already exists.")
            return redirect(url_for("register"))

        # Hash password and insert user
        from datetime import datetime
        password_hash = generate_password_hash(password)
        created_at = datetime.now().isoformat()

        conn.execute(
            "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (name, email, password_hash, created_at)
        )
        conn.commit()
        conn.close()

        flash("Account created. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Validation
        if not email or "@" not in email:
            flash("Invalid email or password.")
            return redirect(url_for("login"))

        if not password:
            flash("Invalid email or password.")
            return redirect(url_for("login"))

        # Look up user by email
        conn = get_db()
        user = conn.execute(
            "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()

        if not user:
            conn.close()
            flash("Invalid email or password.")
            return redirect(url_for("login"))

        # Verify password
        if not check_password_hash(user["password_hash"], password):
            conn.close()
            flash("Invalid email or password.")
            return redirect(url_for("login"))

        # Set session
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        conn.close()

        flash(f"Welcome back, {user['name']}!")
        return redirect(url_for("landing"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    # Clear session
    session.pop("user_id", None)
    session.pop("user_name", None)

    flash("You have been logged out.")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
