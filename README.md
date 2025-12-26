
  ░██     ░██                                  ░██
  ░██    ░██                                   ░██
  ░██   ░██    ░███████   ░███████  ░████████  ░██ ░██    ░██
  ░███████    ░██    ░██ ░██    ░██ ░██    ░██ ░██ ░██    ░██
  ░██   ░██   ░█████████ ░█████████ ░██    ░██ ░██ ░██    ░██
  ░██    ░██  ░██        ░██        ░███   ░██ ░██ ░██   ░███
  ░██     ░██  ░███████   ░███████  ░██░█████  ░██  ░█████░██
                                    ░██                   ░██
  ╻ ╻╻╺┳╸╻ ╻   ┏━╸┏━┓┏━╸┏━┓         ░██              ░███████
  ┃╻┃┃ ┃ ┣━┫   ┃  ┗━┓┗━┓┃┃┃
  ┗┻┛╹ ╹ ╹ ╹   ┗━╸┗━┛┗━┛┗━┛

#### Video Demo: <>

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-orange?logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Project Overview

**Keeply** is a simple web-based appointment booking system built with Flask that enables service providers to manage their schedules and allows clients to book appointments directly through personalized booking links.

### Project Origin and Purpose

This project began with a practical need: my girlfriend required a professional booking page for her body piercing business where clients could view available time slots and book appointments independently. The goal was to create a booking system that would reduce administrative overhead while providing a professional client experience.

The idea eventually evolved into a SaaS-style application where:
- Multiple service providers can register for independent accounts
- Each provider gets their own booking interface and dashboard
- Clients can book appointments through personalized URLs (e.g., `/username`)
- Providers have complete control over their services, availability, and appointments

The application is still in it's infancy when it comes to design. There is still a lot of front-end to test, implement and polish. 
I wanted it to at least show what the basic idea was. This should be a continuous process to be continued after CS50.

### Current Deployment

The application is currently running on Ubuntu Server via Docker containers, hosted on a custom domain (keeply.bitwerk.dev). I'm using Gunicorn to serve my flask app (with 4 workers at the moment). Then to actually give it internet exposure i was trying to just open ports on my home router, but then Chatgpt told me about Cloudflare and their tunnels. It makes thing safer, and a lot simpler. It provides me with a bit of abstraction so that i don't have to do this the harder way.
This setup provides me with a more realistic production environment for testing and development while, hopefuly, maintaining scalability and a path for future growth.

---

## Core Features

### User Management & Authentication
- **User Registration**: A simple account creation with email validation and basic password hashing
- **Secure Login System**: Session-based authentication with CSRF protection

### Service Management
- **Service Creation**: Providers can define multiple services with custom names, descriptions, and pricing
- **Service Catalog**: Each provider maintains their own service menu for client selection
- **Pricing Control**: Flexible pricing structure per service type

### Availability Management
- **Time Slot Generation**: Bulk creation of available time slots with customizable duration
- **Conflict Detection**: Slot overlap detection
- **Visual Interface**: Interactive form with real-time preview of generated slots

### Client Booking System
- **Multi-Step Booking Wizard**: Guided 4-step process (Service → Date → Time → Client Info)
- **Real-time Availability**: Live loading of available dates and time slots via REST API
- **Service Selection**: Dynamic loading of provider's services with pricing display
- **Client Information Collection**: Secure form with CSRF protection for data submission

### Appointment Management
- **Dashboard Interface**: Comprehensive view of all appointments with status tracking
- **Status Workflow**: Pending → Confirmed → Finished appointment lifecycle
- **Client Details**: Complete client information including contact details and service booked
- **Bulk Operations**: Multiple time slot deletion and status updates

### Security Features
- **CSRF Protection**: Cross-Site Request Forgery protection on all forms and API endpoints
- **Password Security**: Werkzeug-based password hashing
- **Session Management**: Secure filesystem-based sessions
- **SQL Injection Prevention**: Parameterized queries throughout the application

### Communication System
- **Email Notifications**: Asynchronous email sending for new appointments
- **Provider Alerts**: Automatic email notifications when clients book appointments

---

## Tech Stack

### Backend Stack

Here i used the same tools used in the Finance problem-set.

- **Python 3.11**
- **Flask 2.3.3**
- **SQLite**
- **CS50 SQL Library** 

I want to migrate my database to PostgreSQL in the future. For now, SQLite does what i require.

# Note: I have found compatibility issues with Python 3.12+ 

### Flask Extensions & Libraries
- **Flask-Session 0.5.0**
- **Flask-Mail 0.9.1**
- **Flask-WTF 1.1.1**
- **Werkzeug 2.3.7**
- **python-dotenv 1.0.0**
- **Gunicorn 23.0.0**

### Frontend Technology Stack
- **HTML5**
- **CSS3**
- **JavaScript (ES6+)**
- **Bootstrap 5.3**

### Database Design
- **Relational Model**: Five interconnected tables with foreign key relationships
- **Data Integrity**: Foreign key constraints and cascade deletion rules
- **Normalization**: Proper separation of concerns (users, services, clients, appointments, timeslots)

---

## Project Structure

```
keeply/
│
├─ app.py
├─ helper.py
├─ wsgi.py
├─ schema.sql
├─ requirements.txt
├─ README.md
├─ TODO.md
├─ Dockerfile
├─ docker-compose.yml
├─ .gitignore
├─ .env
│
├─ static/
│ ├─ stylesheet.css
│ └─ js/
│    ├─ helpers.js
│    ├─ book.js
│    └─ dashboard.js
│
└─ templates/
   ├─ layout.html
   ├─ header.html
   ├─ index.html
   ├─ login.html
   ├─ register.html
   ├─ dashboard.html
   ├─ profile.html
   ├─ availability.html
   ├─ book.html
   └─ success.html
```
---

## Detailed File Descriptions

### Core Application Files

#### `app.py` - Main Flask Application
This is the heart of the Keeply application containing all HTTP routes, API endpoints, and appointment/booking logic.

**Key Components:**
- **Flask Configuration**: Application setup with SECRET_KEY, CSRF protection, session management, and database connection
- **Authentication Routes**: User registration, login, logout system with secure password handling
- **User Management**: Profile management and service creation functionality
- **Dashboard System**: Comprehensive appointment management with status tracking
- **Availability Management**: Time slot generation with mathematical conflict detection and validation
- **Booking API**: RESTful endpoints for client-facing booking process
- **Email System**: Asynchronous email sending with background threading for provider notifications
- **Security Implementation**: CSRF protection, SQL injection prevention, and session security

**Technical Details:**
- Uses parameterized SQL queries via CS50 library for security
- Implements time conflict detection using mathematical interval overlap algorithms
- Handles both HTML form submissions and JSON API requests
- Includes comprehensive error handling and user feedback

#### `helper.py` - Utility Functions
Contains reusable helper functions that support the main application logic.

**Functions:**
- **`login_required(f)`**: Python decorator that protects routes by requiring user authentication
  - Wraps route functions to check session for valid user_id
  - Redirects unauthenticated users to login page

- **`conflict(s1, e1, s2, e2)`**: Mathematical time overlap detection function
  - Determines if two time ranges intersect using interval arithmetic
  - Returns True if ranges overlap, False if they don't

#### `wsgi.py` - Production Server Entry Point
WSGI (Web Server Gateway Interface) configuration for production deployment.

**Purpose:**
- Provides entry point for Gunicorn production server
- Imports Flask application instance from app.py
- Enables deployment behind reverse proxies (nginx, Apache)
- Standard Python WSGI pattern for scalable deployments

#### `schema.sql` - Database Schema Definition
Complete SQLite database structure with normalized relational design.

**Tables:**
- **`users`**: Service provider accounts with authentication data
- **`services`**: Service definitions linked to users (name, description, price)
- **`clients`**: Client information for appointments (name, email, phone)
- **`timeslots`**: Available time slots with conflict prevention
- **`appointments`**: Central booking records linking all entities

**Design Features:**
- Foreign key constraints with CASCADE deletion for data integrity
- Proper indexing for performance optimization
- Status fields for workflow management

### Configuration & Deployment Files

#### `requirements.txt` - Python Dependencies (18 lines)
Defines all required Python packages with exact version pinning for reproducible deployments.

**Key Dependencies:**
- **Flask 2.3.3**: Core web framework
- **Flask extensions**: Session, Mail, WTF for security and functionality
- **CS50 9.2.5**: Educational SQL library with security features
- **Gunicorn 23.0.0**: Production WSGI server

#### `.env` - Environment Variables
Configuration file for sensitive data and deployment settings (not in version control). I will still need to find a better way to keep this information. This is not the best, safest, way.

**Variables:**
- **SECRET_KEY**: Flask session security and CSRF token generation
- **Mail Configuration**: SMTP settings for email notifications
- **Database Settings**: Connection parameters and security options

#### `Dockerfile` - Container Configuration
Docker container definition for consistent deployment environments.
To be honest, Copilot (i think) wrote the Dockerfile and all files related to Docker.  

### Client-Side JavaScript

#### `static/js/helpers.js` - Availability Form Enhancement
Provides interactive functionality for the time slot creation form.

**Key Functions:**
- **Time Conversion**: Utilities for converting between time strings and minutes
- **Duration Calculation**: Smart generation of valid duration options
- **Real-time Preview**: Live table showing slots that will be created
- **Visual Feedback**: Color-coded warnings for long time periods
- **Input Validation**: Prevents invalid time range selections

**User Experience:**
- **Instant Feedback**: Real-time updates as user types
- **Smart Defaults**: Intelligent duration suggestions based on time range

#### `static/js/book.js` - Booking Wizard Controller
Manages the complete client booking process with API integration. At first i was just using a multi-step form using javascript to hide or show certain stages of the process. But then i read about API endpoints, and realized (with some artificial guidance) that i could use this to make my booking form more robust.

**Process Management:**
- **Step-by-Step Navigation**: Controls visibility of booking stages
- **State Management**: Tracks selected service, date, and time slot
- **API Communication**: Fetches data from backend endpoints
- **Form Submission**: Secure booking submission with CSRF protection

**Security Features:**
- **CSRF Token Handling**: Reads token from meta tag for AJAX requests
- **Data Validation**: Client-side validation before submission

#### `static/js/dashboard.js` - Dashboard Interactivity
Handles administrative functions in the dashboard interface.

**Functionality:**
- **Status Updates**: AJAX calls for appointment status changes
- **Bulk Operations**: Multiple appointment management
- **User Feedback**: Real-time updates without page refresh

#### `static/stylesheet.css` - Application Styling
Custom CSS providing application-specific styling beyond Bootstrap defaults.

**Design Principles:**
- **Responsive Design**: Mobile-first approach with breakpoints
- **Professional Appearance**: Business-appropriate color scheme and typography
- **Accessibility**: Proper contrast ratios and keyboard navigation
- **Brand Consistency**: Unified visual language across all pages

