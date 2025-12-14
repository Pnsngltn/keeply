# ***TODO***:

## Front-End

#### Landing Page (Index):
- [X] Simple Register and Login buttons
- [ ] Show app description
- [ ] Make/Add Keeply logo
- [ ] User Finder ?

#### Dashboard:
- [X] Show available services
- [X] Show Appointments (Pending, Confirmed, Finished)
- [X] Allow for status updates on appointments
- [ ] Services Table to include "Description"
- [ ] Change 'Manage Availability' position
- [ ] Don't show past appointments
- [ ] Optimize UI

#### Profile:
- [X] Add User Info table
- [X] Allow for service creation
- [X] Show all created services
- [ ] Allow for service deletion
- [ ] Add fields for service provider info (Description/About me, Location, Profile Picture)
- [ ] Add placeholder text to text boxes
- [ ] Optimize UI

#### Availability:
- [X] Prompt to selct time interval
    [X] Make duration field only show durations that equally divide the time interval

- [X] Preview of Generated Slots
    - [ ] Allow to deselect individual slots
    - [ ] Only show if list > 0

- [X] Existing Timeslots
    - [ ] Don't show past slots
    - [ ] Fix 'Detele' position and functionality

- [ ] Optimize UI

#### Register:
- [X] Add register form
- [ ] Make it a guided multi-step register process

#### Login:
- [X] Add Login form

#### Book/<username>:
- [X] Use API endpoints to create a multi-step form 
- [ ] Use bootstrap to improve UI
- [ ] Add in-app payments

#### [ ] 'Apology' Template:

#### [ ] Booking Form Designing:
- [ ] Allow user to design how their booking page is presented

## Back-End

#### App Config
- [X] Flask application configuration
- [X] CSRF Protection
- [X] App Session Config
- [X] CS50's SQL library 
- [ ] Migrate to PostgreSQL
- [X] Configure Flask-Mail

#### [X] Async Email Sending

#### Routes
- [X] /
- [X] /register
- [X] /login
- [X] /logout
- [X] /book/<username>
- [X] /availability
- [X] /dashboard
- [X] /profile

#### API Endpoints
- [X] /api/appointment/status
- [X] /api/timeslots/delete
- [X] /api/book
- [ ]
