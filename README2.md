# Keeply
#### Video Demo: <>

## Description

**Keeply** is a comprehensive web-based appointment booking system built with Flask that enables service providers to manage their schedules and allows clients to book appointments directly through personalized booking pages.

### Project Origin and Purpose

This project began with a practical need: my girlfriend required a professional booking page for her body piercing business where clients could view available time slots and book appointments independently. The goal was to create a self-service booking system that would reduce administrative overhead while providing a professional client experience.

The project evolved into a multi-tenant SaaS-style application where:
- Multiple service providers can register for independent accounts
- Each provider gets their own booking interface and dashboard
- Clients can book appointments through personalized URLs (e.g., `/username`)
- Providers have complete control over their services, availability, and appointments

### Current Deployment

The application is currently running on Ubuntu Server via Docker containers, hosted on a custom domain (keeply.bitwerk.dev). This setup provides a real-world production environment for testing and development while maintaining scalability for future growth.

---

## Core Features

### User Management & Authentication
- **User Registration**: Complete account creation with email validation and secure password hashing
- **Secure Login System**: Session-based authentication with CSRF protection
- **Profile Management**: Users can update personal information and manage account settings

### Service Management
- **Service Creation**: Providers can define multiple services with custom names, descriptions, and pricing
- **Service Catalog**: Each provider maintains their own service menu for client selection
- **Pricing Control**: Flexible pricing structure per service type

### Availability Management
- **Time Slot Generation**: Bulk creation of available time slots with customizable duration
- **Conflict Detection**: Automatic prevention of overlapping time slots using mathematical interval overlap detection
- **Visual Interface**: Interactive form with real-time preview of generated slots
- **Smart Validation**: Prevents time slot creation without associated services

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
- **Password Security**: Werkzeug-based password hashing with salt
- **Session Management**: Secure filesystem-based sessions with automatic expiration
- **SQL Injection Prevention**: Easy parameterized queries throughout the application with CS50's SQL library

### Communication System
- **Email Notifications**: Asynchronous email sending for new appointments
- **Provider Alerts**: Automatic email notifications when clients book appointments

---

## Technical Architecture

### Backend Technology Stack
- **Python 3.11**: Core programming language with modern features
- **Flask 2.3.3**: Lightweight web framework with extensive ecosystem
- **SQLite**: File-based database system for simplicity and portability
- **CS50 SQL Library**: Educational SQL wrapper with security features

# Note: Python 3.12+ users may need to install setuptools first:
# pip install setuptools
# This fixes CS50 compatibility with newer Python versions

### Flask Extensions & Libraries
- **Flask-Session 0.5.0**: Server-side session management with filesystem storage
- **Flask-Mail 0.9.1**: Asynchronous email sending with SMTP support
- **Flask-WTF 1.1.1**: CSRF protection and secure form handling
- **Werkzeug 2.3.7**: WSGI utilities and security functions (password hashing)
- **python-dotenv 1.0.0**: Environment variable management for configuration
- **Gunicorn 23.0.0**: Production WSGI server for deployment

### Frontend Technology Stack
- **HTML5**: Semantic markup with modern web standards
- **CSS3**: Custom styling with responsive design principles
- **JavaScript (ES6+)**: Modern JavaScript with async/await and fetch API
- **Bootstrap 5.3**: Professional UI framework with responsive grid system

### Database Design
- **Relational Model**: Five interconnected tables with foreign key relationships
- **Data Integrity**: Foreign key constraints and cascade deletion rules
- **Normalization**: Proper separation of concerns (users, services, clients, appointments, timeslots)

---

## Project Structure

```
keeply/
│
├─ Core Application Files
│ ├─ app.py              # Main Flask application with all routes and API endpoints
│ ├─ helper.py            # Utility functions (login_required decorator, conflict detection)
│ ├─ wsgi.py              # WSGI entry point for production deployment
│ ├─ schema.sql           # Complete database schema with table definitions
│ └─ requirements.txt      # Python dependencies with version pinning
│
├─ Configuration & Deployment
│ ├─ .env                 # Environment variables (not in version control)
│ ├─ .gitignore           # Git ignore rules for sensitive files
│ ├─ Dockerfile            # Container configuration for production deployment
│ └─ docker-compose.yml    # Multi-service orchestration with Cloudflare tunnel
│
├─ Templates/ (HTML Views)
│ ├─ layout.html          # Base template with Bootstrap and common structure
│ ├─ header.html           # Navigation component with authentication state
│ ├─ index.html           # Landing page with application overview
│ ├─ login.html           # User authentication form
│ ├─ register.html        # New user registration with validation
│ ├─ dashboard.html        # Main admin interface with appointment management
│ ├─ profile.html         # User profile and service management
│ ├─ availability.html     # Time slot creation with conflict detection
│ ├─ book.html            # Client booking wizard with multi-step process
│ └─ success.html         # Booking confirmation page
│
├─ Static/ (Client-Side Assets)
│ ├─ stylesheet.css       # Custom CSS styling and responsive design
│ └─ js/
│    ├─ helpers.js        # Availability form interactivity and validation
│    ├─ book.js           # Client booking wizard with API integration
│    └─ dashboard.js      # Dashboard functionality and status updates
│
├─ Documentation
│ └─ README.md            # This File
└─ Data
   └─ books.db            # SQLite database file (created from schema.sql)
```
---

## Detailed File Descriptions

### Core Application Files

#### `app.py` - Main Flask Application
This is the heart of the Keeply application containing all HTTP routes, API endpoints, and business logic.

**Key Components:**
- **Flask Configuration**: Application setup with SECRET_KEY, CSRF protection, session management, and database connection
- **Authentication Routes**: Complete user registration, login, logout system with secure password handling
- **User Management**: Profile management and service creation functionality
- **Dashboard System**: Comprehensive appointment management with status tracking
- **Availability Management**: Time slot generation with conflict detection and validation
- **Booking API**: RESTful endpoints for client-side booking process
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
  - Preserves function signatures and arguments
- **`conflict(s1, e1, s2, e2)`**: Mathematical time overlap detection function
  - Determines if two time ranges intersect using interval arithmetic
  - Returns True if ranges overlap, False if they don't
  - Used in availability management to prevent double-booking

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

#### `requirements.txt` - Python Dependencies
Defines all required Python packages with exact version pinning for reproducible deployments.

**Key Dependencies:**
- **Flask 2.3.3**: Core web framework
- **Flask extensions**: Session, Mail, WTF for security and functionality
- **CS50 9.2.5**: Educational SQL library with security features
- **Gunicorn 23.0.0**: Production WSGI server

**Python 3.12+ Compatibility Note:**
- **CS50 Issue**: CS50 9.2.5 may require `setuptools` for Python 3.12+
- **Fix**: Run `pip install setuptools` before installing requirements
- **Alternative**: Use Python 3.11 or wait for CS50 update

#### `.env` - Environment Variables
Configuration file for sensitive data and deployment settings (not in version control).

**Variables:**
- **SECRET_KEY**: Flask session security and CSRF token generation
- **Mail Configuration**: SMTP settings for email notifications
- **Database Settings**: Connection parameters and security options

#### `Dockerfile` - Container Configuration
Docker container definition for consistent deployment environments.

**Features:**
- Multi-stage build for optimized image size
- Python 3.11-slim base image for efficiency
- Gunicorn production server configuration
- Security best practices with non-root execution

#### `docker-compose.yml` - Multi-Service Orchestration
Defines complete application stack with external access via Cloudflare tunnel.

**Services:**
- **app**: Main Flask application with database persistence
- **cloudflared**: External access tunnel for public availability
- Network isolation and service dependencies

### Frontend Templates

#### `templates/layout.html` - Base Template
Foundation template providing consistent HTML structure across all pages.

**Components:**
- **Bootstrap 5.3 Integration**: CSS framework for responsive design
- **CSRF Token Meta Tag**: Security for AJAX requests
- **Template Inheritance**: Block system for page-specific content
- **Navigation Integration**: Header component inclusion

#### `templates/header.html` - Navigation Component
Dynamic navigation that adapts based on user authentication state.

**Features:**
- **Authentication-Aware**: Shows different options for logged-in vs. logged-out users
- **Bootstrap Navigation**: Responsive navbar with mobile support
- **Route Links**: Direct access to dashboard, profile, and logout

#### `templates/index.html` - Landing Page
Main landing page providing application overview and user onboarding.

**Purpose:**
- **Marketing Content**: Application features and benefits
- **Call-to-Action**: Registration and login prompts
- **Professional Presentation**: First impression for potential users

#### `templates/login.html` - Authentication Form
User login interface with security features and validation.

**Features:**
- **CSRF Protection**: Hidden token field for security
- **Form Validation**: Client and server-side validation
- **Error Handling**: Clear feedback for authentication failures
- **Responsive Design**: Mobile-friendly form layout

#### `templates/register.html` - User Registration
Complete new user registration with comprehensive validation.

**Validation:**
- **Required Fields**: Username, email, phone, password, confirmation
- **Uniqueness Checks**: Server-side validation for username and email
- **Password Matching**: Client and server-side confirmation validation
- **CSRF Protection**: Secure form submission

#### `templates/dashboard.html` - Admin Interface (Complex)
Main administrative interface for appointment and service management.

**Features:**
- **Appointment Table**: Comprehensive view with client details and service information
- **Status Management**: Interactive buttons for confirm, cancel, finish operations
- **Service Overview**: Quick access to service management
- **AJAX Integration**: Real-time status updates without page reload

#### `templates/profile.html` - User Profile Management
User information display and service creation interface.

**Functionality:**
- **Profile Display**: Shows username, email, phone (read-only)
- **Service Creation**: Form for adding new services with validation
- **Service List**: Display of existing services with management options
- **Error Handling**: Form validation with user feedback

#### `templates/availability.html` - Time Slot Management
Interactive interface for creating and managing available time slots.

**Advanced Features:**
- **Conditional Display**: Shows form only if user has services (prevents confusion)
- **Real-time Preview**: JavaScript-powered preview of slots to be created
- **Conflict Prevention**: Backend validation against existing slots
- **Visual Feedback**: Color-coded duration warnings and slot previews
- **Bulk Operations**: Multiple slot creation and deletion capabilities

#### `templates/book.html` - Client Booking Wizard
Multi-step booking process for client appointments.

**Booking Flow:**
1. **Service Selection**: Dynamic loading of provider's services with pricing
2. **Date Selection**: Available dates with free time slots only
3. **Time Selection**: Specific available time slots for chosen date
4. **Client Information**: Contact details collection with validation
5. **Confirmation**: Success message with booking details

**Technical Features:**
- **Progressive Enhancement**: Works without JavaScript, enhanced with it
- **API Integration**: Real-time data loading via REST endpoints
- **CSRF Protection**: Secure AJAX form submission
- **Responsive Design**: Mobile-friendly booking interface

#### `templates/success.html` - Booking Confirmation
Simple confirmation page displayed after successful appointment booking.

**Purpose:**
- **Success Feedback**: Clear confirmation of completed booking
- **Professional Presentation**: Maintains application branding
- **User Guidance**: Options for next actions

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
- **Error Prevention**: Blocks invalid selections before form submission

#### `static/js/book.js` - Booking Wizard Controller
Manages the complete client booking process with API integration.

**Process Management:**
- **Step-by-Step Navigation**: Controls visibility of booking stages
- **State Management**: Tracks selected service, date, and time slot
- **API Communication**: Fetches data from backend endpoints
- **Form Submission**: Secure booking submission with CSRF protection

**Security Features:**
- **CSRF Token Handling**: Reads token from meta tag for AJAX requests
- **Data Validation**: Client-side validation before submission
- **Error Handling**: Graceful handling of network failures

#### `static/js/dashboard.js` - Dashboard Interactivity
Handles administrative functions in the dashboard interface.

**Functionality:**
- **Status Updates**: AJAX calls for appointment status changes
- **Bulk Operations**: Multiple appointment management
- **User Feedback**: Real-time updates without page refresh
- **Confirmation Dialogs**: User verification for destructive actions

#### `static/stylesheet.css` - Application Styling
Custom CSS providing application-specific styling beyond Bootstrap defaults.

**Design Principles:**
- **Responsive Design**: Mobile-first approach with breakpoints
- **Professional Appearance**: Business-appropriate color scheme and typography
- **Accessibility**: Proper contrast ratios and keyboard navigation
- **Brand Consistency**: Unified visual language across all pages
