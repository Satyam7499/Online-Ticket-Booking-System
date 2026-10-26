from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    venue = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    seats = db.relationship("Seat", backref="event", cascade="all, delete-orphan")


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    seat_no = db.Column(db.String(10), nullable=False)
    is_booked = db.Column(db.Boolean, default=False)
    locked_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    locked_until = db.Column(db.DateTime, nullable=True)

    def is_locked(self, current_user_id=None):
        if self.locked_until and self.locked_until > datetime.utcnow():
            if current_user_id and self.locked_by == current_user_id:
                return False
            return True
        return False

    def lock(self, user_id, minutes=3):
        self.locked_by = user_id
        self.locked_until = datetime.utcnow() + timedelta(minutes=minutes)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey("seat.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    payment_status = db.Column(db.String(20), default="pending")
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User")
    seat = db.relationship("Seat")
    event = db.relationship("Event")
