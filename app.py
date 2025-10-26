import os

from cs50 import SQL
from datetime import datetime, timedelta
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_mail import Mail, Message
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from helpers import *

# Configure application
app = Flask(__name__)

# Configure session to use filesystem
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

# Configure CS50's SQL Library
db = SQL("sqlite:///books.db")

# Configure Flask-Mail
mail = Mail(app)

# Clear Cached Information
@app.after_request
def after_request(response):
    """Ensure Inputs aren't cached"""
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# ==============================================================================
# # Routes
# ==============================================================================

# Route for Homepage ===========================================================

# Route for Login ==============================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login Route"""

    # Forget Cached User ID's
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", error="Username is required")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", error="Password is required")

        # Query database for username
        rows = db.execute(
                "SELECT * FROM users WHERE username = ?", request.form.get("username")
                )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
                rows[0]["password"], request.form.get("password")
                ):
            return render_template("login.html", error="Invalid username or password")

        # Remember Logged-In User
        session["user_id"] = rows[0]["id"]

        # Redirect to dashboard
        return redirect("/dashboard")
    else:
        return render_template("login.html")

# Route for Dashboard ==========================================================

# Route for Availability =======================================================

# Route for Form Design ========================================================

# Route for /username (Booking Page) ===========================================


if __name__ == "__main__":
    app.run(debug=True)
