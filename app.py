import os

from cs50 import SQL
from datetime import datetime, timedelta
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_mail import Mail, Message
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

from helper import login_required, conflict

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
# ============ Register ========================================================
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

        # Validate input
        if not username or not password or not confirmation or not email or not phone:
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
            "INSERT INTO users (username, pwd_hash, email, phone) VALUES (?, ?, ?, ?)",
            username, pwd_hash, email, phone
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
        # Note: during registration the hashed password is stored in `pwd_hash`
        if len(rows) != 1 or not check_password_hash(
                rows[0]["pwd_hash"], request.form.get("password")
                ):
            return render_template("login.html", error="Invalid username or password")

        # Remember Logged-In User
        session["user_id"] = rows[0]["id"]

        # Redirect to dashboard
        return redirect("/dashboard")
    else:
        return render_template("login.html")

# ------------------------------------------------------------------------------
# ========== Profile ===========================================================
# ------------------------------------------------------------------------------
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session["user_id"]
    rows = db.execute("SELECT username, email, phone FROM users WHERE id = ?", user_id)
    if not rows:
        return "User not Found", 404
    user_info = rows[0]

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")

        if not name or not price or not description:
            error = "All fields required."
            # Fetch user info and services to render an error template
            services = db.execute("SELECT id, name, description, price FROM services WHERE user_id = ?", user_id)
            return render_template("profile.html", user=user_info, services=services, error=error)

        # Insert new service
        db.execute(
            "INSERT INTO services (user_id, name, description, price) VALUES (?, ?, ?, ?)",
            user_id, name, description, price
        )
        return redirect("/profile")
    
    # GET request: Show Profile
    services = db.execute("SELECT id, name, description, price FROM services WHERE user_id = ?", user_id)

    return render_template("profile.html", user=user_info, services=services)             

# ------------------------------------------------------------------------------
# ======== Dashboard ===========================================================
# ------------------------------------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    services = db.execute("SELECT * FROM services WHERE user_id = ?", user_id)
    
    # Get appointments with client and service details
    appointments = db.execute("""
        SELECT 
            a.id,
            a.status,
            c.name as client_name,
            c.email as client_email,
            c.phone as client_phone,
            s.name as service_name,
            t.date,
            t.time_start,
            t.time_end
        FROM appointments a
        JOIN clients c ON a.client_id = c.id
        JOIN services s ON a.service_id = s.id
        JOIN timeslots t ON a.slot_id = t.id
        WHERE a.user_id = ?
        ORDER BY t.date, t.time_start
    """, user_id)

    return render_template("dashboard.html", 
                         services=services,
                         appointments=appointments)

# ------------------------------------------------------------------------------
# ========= Availability =======================================================
# ------------------------------------------------------------------------------
@app.route("/availability", methods=["GET", "POST"])
@login_required
def availability():
    """Set the available timeslots"""

    user_id = session["user_id"]
    
    if request.method == "POST":
        date = request.form.get("date")
        start = request.form.get("time_start")
        end = request.form.get("time_end")
        duration = request.form.get("duration")

        if not date or not start or not end or not duration:
            return render_template(
                "availability.html",
                error="Please fill all fields",
                    slots=db.execute("SELECT * FROM timeslots where user_id = ? ORDER BY date, time_start", user_id)
            )
        duration = int(duration)

        # Convert to minutes since midnight
        sh, sm = map(int, start.split(":"))
        eh, em = map(int, end.split(":"))
        start_min = sh * 60 + sm
        end_min = eh * 60 + em

        # Handle wrap around midnight
        total_minutes = end_min - start_min if end_min > start_min else (24 * 60 - start_min) + end_min

        # Find existing slots for that date
        existing = db.execute("SELECT time_start, time_end FROM timeslots WHERE user_id = ? AND date = ?", user_id, date)

        existing_ranges = []
        for row in existing:
            sh, sm = map(int, row["time_start"].split(":"))
            eh, em = map(int, row["time_send"].split(":"))
            existing_ranges.append((sh * 60 + sm, eh * 60 + em))

        # Generate slots and check conflicts
        current = start_min 
        created, conflicts = 0, 0 
        while total_minutes > 0:
            next_slot = (current + duration) % (24 * 60)
            slot_start = current
            slot_end = next_slot

            has_conflict = any(conflict(slot_start, slot_end, s, e) for s, e in existing_ranges)
            
            if has_conflict:
                conflicts += 1
            else:
                slot_start_str = f"{slot_start // 60:02d}:{slot_start % 60:02d}"
                slot_end_str = f"{slot_end // 60:02d}:{slot_end % 60:02d}"
                db.execute("INSERT INTO timeslots (user_id, date, time_start, time_end, duration) VALUES (?, ?, ?, ?, ?)",
                    user_id, date, slot_start_str, slot_end_str, duration
                           )
                created += 1
            total_minutes -= duration
            current = next_slot

        slots = db.execute("SELECT * FROM timeslots WHERE user_id = ? ORDER BY date, time_start", user_id)

        message = f"{created} slots created."

        if conflicts > 0:
            message += f"{conflicts} conflicted with existing ones."

        return render_template("availability.html", success=message, slots=slots)
    
    # GET requests
    slots = db.execute("SELECT * FROM timeslots WHERE user_id = ? ORDER BY date, time_start", user_id)
    return render_template("availability.html", slots=slots)

# Route for Form Design ========================================================

# ------------------------------------------------------------------------------
# ========= /username (Booking Page) ===========================================
# ------------------------------------------------------------------------------
@app.route("/book/<username>")
def book(username):
    provider = db.execute("SELECT id, email FROM users WHERE username = ?", username)
    if len(provider) == 0:
        return "Provider not found", 404     # Change later
    return render_template("book.html", username=username, user_id=provider[0]["id"])

# ------------------------------------------------------------------------------
# ======= API Endpoints for JS Form ============================================
# ------------------------------------------------------------------------------
@app.route("/api/services/<int:user_id>")
def api_services(user_id):
    # fixed stray comma in SELECT
    services = db.execute("SELECT id, name, price FROM services WHERE user_id = ?", user_id)
    return jsonify(services)
  
@app.route("/api/dates/<int:user_id>")
def api_date(user_id):
    # Fix SQL syntax: remove stray AND before ORDER BY
    dates = db.execute("SELECT DISTINCT date FROM timeslots WHERE user_id = ? AND status = 'Free' ORDER BY date",
                       user_id)
    return jsonify([d['date'] for d in dates])
    
@app.route("/api/timeslots/<int:user_id>/<date>")
def api_timeslots(user_id, date):
    slots = db.execute("SELECT id, time_start, time_end FROM timeslots WHERE user_id = ? AND status = 'Free' AND date = ? ORDER BY time_start", 
                       user_id, date)
    return jsonify(slots)

# ------------------------------------------------------------------------------
# ======= API Endpoint for Appointment Status Update ==============================
# ------------------------------------------------------------------------------
@app.route("/api/appointment/status", methods=["POST"])
@login_required
def update_appointment_status():
    """Update appointment status (confirm, cancel, finish)"""
    data = request.json
    if not data or "appointment_id" not in data or "status" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    appointment_id = data["appointment_id"]
    new_status = data["status"]
    user_id = session["user_id"]

    # Verify the appointment belongs to this user
    appointment = db.execute(
        "SELECT id FROM appointments WHERE id = ? AND user_id = ?",
        appointment_id, user_id
    )
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404

    # Update appointment status
    db.execute(
        "UPDATE appointments SET status = ? WHERE id = ?",
        new_status, appointment_id
    )

    # If cancelled, free up the timeslot
    if new_status == "cancelled":
        slot_id = db.execute(
            "SELECT slot_id FROM appointments WHERE id = ?",
            appointment_id
        )[0]["slot_id"]
        db.execute(
            "UPDATE timeslots SET status = 'Free' WHERE id = ?",
            slot_id
        )

    return jsonify({"success": True})

@app.route("/api/book", methods=["POST"])
def api_book():
    data = request.json
    user_id = data["user_id"]
    service_id = data["service_id"]
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

    # Insert appointment with pending status and mark slot as booked
    db.execute("""
        INSERT INTO appointments 
        (user_id, client_id, slot_id, service_id, status) 
        VALUES (?, ?, ?, ?, 'pending')
    """, user_id, client_id, slot_id, service_id)
    db.execute("UPDATE timeslots SET status = 'Booked' WHERE id = ?", slot_id)

    # Email the provider with basic details (best-effort; non-fatal if mailing fails)
    try:
        provider = db.execute("SELECT email FROM users WHERE id = ?", user_id)
        user_email = provider[0]["email"] if provider else None

        service = db.execute("SELECT name FROM services WHERE id = ?", service_id)
        service_name = service[0]["name"] if service else "(unknown)"

        timeslot = db.execute("SELECT date, time_start, time_end FROM timeslots WHERE id = ?", slot_id)
        if timeslot:
            date = timeslot[0]["date"]
            time = f"{timeslot[0]['time_start']} - {timeslot[0]['time_end']}"
        else:
            date = "(unknown)"
            time = "(unknown)"

        if user_email:
            msg = Message(
                subject=f"New booking from {client_name}",
                recipients=[user_email],
                body=f"New booking:\n\nClient: {client_name}\nService: {service_name}\nDate: {date} at {time}\nPhone: {client_phone}\nEmail: {client_email}"
            )
            mail.send(msg)
    except Exception:
        # Don't crash the API if email sending fails
        pass

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
