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

# Routes


