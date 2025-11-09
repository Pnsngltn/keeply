import os

from cs50 import SQL
from datetime import datetime, timedelta
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_mail import Mail, Message
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from helper import *

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

# ------------------------------------------------------------------------------
# Route for Homepage ===========================================================
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# ========= Register ( FIX ) ===========================================================
# ------------------------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    """User Registration"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")
        phone = request.form.get("phone")
        duration = request.form.get("duration")  # in minutes

        # Validate input
        if not username or not password or not confirmation or not email or not phone or not duration:
            return render_template("register.html", error="All fields are required")

        if password != confirmation:
            return render_template("register.html", error="Passwords do not match")

        # Check if username or email already exists
        if db.execute("SELECT * FROM users WHERE username = ?", username):
            return render_template("register.html", error="Username already taken")
        if db.execute("SELECT * FROM users WHERE email = ?", email):
            return render_template("register.html", error="Email already registered")

        # Hash password
        pwd_hash = generate_password_hash(password)

        # Insert user
        db.execute(
            "INSERT INTO users (username, pwd_hash, email, phone, duration) VALUES (?, ?, ?, ?, ?)",
            username, pwd_hash, email, phone, duration
        )

        # Automatically log in new user
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        session["user_id"] = user_id

        return redirect("/dashboard")

    return render_template("register.html")




# ------------------------------------------------------------------------------
# ========= Login ==============================================================
# ------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------
# ======== Dashboard ===========================================================
# ------------------------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    user_id = session["user_id"]
    services = db.execute("SELECT * FROM services WHERE user_id = ?", user_id)
    slots = db.execute("SELECT * FROM timeslots WHERE user_id = ?", user_id)
    appointments = db.execute("SELECT * FROM appointments WHERE user_id = ?", user_id)

    return render_template("dashboard.html", 
                           services=services, slots=slots, appointments=appointments)

# ------------------------------------------------------------------------------
# ========= Availability =======================================================
# ------------------------------------------------------------------------------
@app.route("/availability", methods=["GET", "POST"])
def availability():
    if "user_id" not in session:
        return redirect("login")
    user_id = session["user_id"]
    duration = db.execute("SELECT duration FROM users WHERE id = ?", user_id)[0]["duration"]
    
    if request.method == "POST":
        date = request.form.get("date")
        start_time = request.form.get("time_start")
        h, m = map(int, start_time.split(":"))
        end_minutes = h * 60 + m + duration
        end_time = f"{end_minutes // 60 : 02d}:{end_minutes % 60 : 02d}"
        db.execute("INSERT INTO timeslots (user_id, date, time_start, time_end) VALUES (?, ?, ?, ?)",
                   user_id, date, start_time, end_time)

    slots = db.execute("SELECT * FROM timeslots WHERE user_id = ?", user_id)
    return render_template("availability.html", slots=slots)

# Route for Form Design ========================================================

# ------------------------------------------------------------------------------
# ========= /username (Booking Page) ===========================================
# ------------------------------------------------------------------------------
@app.route("/book/<username>")
def book(username):
    provider = db.execute("SELECT id, email, duration FROM users WHERE username = ?", username)
    if len(provider) == 0:
        return "Provider not found", 404     # Change later
    return render_template("book.html", username=username, user_id=provider[0]["id"], duration=provider[0]["duration"])

# ------------------------------------------------------------------------------
# ======= API Endpoints for JS Form ============================================
# ------------------------------------------------------------------------------
@app.route("/api/services/<int:user_id>")
def api_services(user_id):
    services = db.execute("SELECT id, name, price, FROM services WHERE user_id = ?", user_id)
    return jsonify(services)
  
@app.route("/api/dates/<int:user_id>")
def api_date(user_id):
    dates = db.execute("SELECT DISTINCT date FROM timeslots WHERE user_id = ? AND status = 'Free' AND ORDER BY date",
                       user_id)
    return jsonify([d['date'] for d in dates])
    
@app.route("/api/timeslots/<int:user_id>/<date>")
def api_timeslots(user_id, date):
    slots = db.execute("SELECT id, time_start, time_end FROM timeslots WHERE user_id = ? AND status = 'Free' AND date = ? ORDER BY time_start", 
                       user_id, date)
    return jsonify(slots)

@app.route("/api/book", methods=["POST"])
def api_book():
    data = request.json
    user_id = data["user_id"]
    servive_id = data["service_id"]
    slot_id = data["slot_id"]
    client_name = data["name"]
    client_email = data["email"]
    client_phone = data["phone"]

    # Check/create client
    client = db.execute("SELECT id FROM clients WHERE email = ? AND phone = ?", client_email, client_phone)
    if len(client) == 0:
        db.execute("INSERT INTO clients (name, email, phone) VALUES (?, ?, ?)", client_name, client_email, client_phone)
        client_id = db.execute("SELECT id FROM clients WHERE email = ? AND phone = ?", client_email, client_phone)[0]["id"]
    else:
        client_id = client[0]["id"]

    # Create appointments
    db.execute("INSER INTO appointments (user_id, client_id, slot_id, service_id) VALUES (?, ?, ?, ?)", user_id, client_id, slot_id, service_id)
    db.execute("UPDATE timeslots SET status = 'Booked' WHERE id = ?", slot_id)


    # Email the admin
    msg = Message(
            subject=f"Nova marcação de {client}!",
            recipients=[user_email],
            body=f"""
                Novo agendamento recebido:

                Cliente: {client}
                Serviço: {service}
                Data: {date} às {time}

                Telefone: {phone}
                Email: {email}
                """
    )
    mail.send(msg)

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
