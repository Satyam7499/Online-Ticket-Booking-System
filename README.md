# Online Ticket Booking System

A Flask-based web app for booking event/movie tickets: browse events, pick a seat in real time, pay (simulated), and get an e-ticket with a QR code. Built as a college mini-project.

## Features
- User signup/login (hashed passwords)
- Event listing (movies/events/shows)
- Interactive seat selection with 3-minute hold to prevent double-booking
- Simulated payment flow
- Instant e-ticket generation with QR code
- Admin panel: add/edit/delete events, view bookings and revenue stats

## Tech Stack
Flask, Flask-SQLAlchemy, Flask-Login, SQLite, qrcode, HTML/CSS/JS

## Setup

```bash
# 1. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Seed the database with an admin user + sample events
python seed.py

# 4. Run the app
python run.py
```

Open **http://127.0.0.1:5000** in your browser.

## Demo Logins
- **Admin:** admin@ticket.com / admin123
- Or sign up as a new user from the app.

## Project Structure
```
ticket-booking/
├── app/
│   ├── __init__.py       # app factory
│   ├── models.py         # User, Event, Seat, Booking
│   ├── routes/           # auth, events, booking, admin blueprints
│   ├── templates/        # Jinja2 HTML templates
│   └── static/           # CSS + generated ticket QR images
├── run.py                # entry point
├── seed.py                # creates admin + sample events
└── requirements.txt
```
