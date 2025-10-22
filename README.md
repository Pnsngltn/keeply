# Keeply

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-orange?logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**Keeply** is a simple web app for booking appointments with clients.
It allows clients to book directly and admins to manage schedules efficiently.

---

## Demo
![Keeply Dashboard Placeholder](screenshots/dashboard.png)
*Placeholder screenshot: Dashboard showing appointments and availability.*

---

## Features
- Personalized booking pages for users (e.g., `/username`)
- Client-side appointment booking with service selection
- Admin dashboard for managing Pending, Confirmed, Finished appointments
- Availability management (set timeslots)
- Clean, responsive design

---

## Tech Stack
- Python 3, Flask
- SQLite
- HTML / CSS / JavaScript
- Optional: Bootstrap for styling

---

## Project Structure

keeply/
│
├─ app.py # Flask app routes
├─ helpers.py # Python helper functions
├─ schema.sql # Database schema
├─ books.db # SQLite database
├─ requirements.txt # Python dependencies
│
├─ templates/ # HTML templates
│ ├─ layout.html
│ ├─ login.html
│ ├─ dashboard.html
│ ├─ success.html
│ └─ book.html
│
├─ static/ # Static files
│ ├─ styles.css
│ └─ helpers.js
│
├─ README.md
├─ LOG.md / PROGRESS.md # Optional development tracking

---

## Installation / Setup

```bash
# Clone repo
git clone https://github.com/Pnsngltn/keeply.git
cd keeply

# Create virtual environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run Flask app
flask run

