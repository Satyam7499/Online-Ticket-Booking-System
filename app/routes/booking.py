import os
import qrcode
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Event, Seat, Booking

booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/event/<int:event_id>/seats")
@login_required
def select_seat(event_id):
    event = Event.query.get_or_404(event_id)
    seats = Seat.query.filter_by(event_id=event_id).order_by(Seat.id).all()
    return render_template("seat_select.html", event=event, seats=seats, now=datetime.utcnow())


@booking_bp.route("/seat/<int:seat_id>/lock", methods=["POST"])
@login_required
def lock_seat(seat_id):
    seat = Seat.query.get_or_404(seat_id)

    if seat.is_booked:
        flash("Sorry, that seat is already booked.", "error")
        return redirect(url_for("booking.select_seat", event_id=seat.event_id))

    if seat.is_locked(current_user.id):
        flash("That seat is currently being booked by someone else. Try another.", "error")
        return redirect(url_for("booking.select_seat", event_id=seat.event_id))

    seat.lock(current_user.id)
    db.session.commit()
    return redirect(url_for("booking.payment", seat_id=seat.id))


@booking_bp.route("/payment/<int:seat_id>", methods=["GET", "POST"])
@login_required
def payment(seat_id):
    from flask import request

    seat = Seat.query.get_or_404(seat_id)
    event = Event.query.get_or_404(seat.event_id)

    if seat.is_booked or seat.is_locked(current_user.id):
        flash("This seat is no longer held for you. Please select again.", "error")
        return redirect(url_for("booking.select_seat", event_id=event.id))

    if request.method == "POST":
        # Simulated payment: always succeeds unless amount tampering etc.
        seat.is_booked = True
        seat.locked_by = None
        seat.locked_until = None

        booking = Booking(
            user_id=current_user.id,
            seat_id=seat.id,
            event_id=event.id,
            payment_status="paid",
        )
        db.session.add(booking)
        db.session.commit()

        generate_ticket_qr(booking)

        flash("Payment successful! Your e-ticket is ready.", "success")
        return redirect(url_for("booking.ticket", booking_id=booking.id))

    return render_template("payment.html", seat=seat, event=event)


def generate_ticket_qr(booking):
    data = f"BOOKING:{booking.id}|USER:{booking.user_id}|EVENT:{booking.event_id}|SEAT:{booking.seat_id}"
    img = qrcode.make(data)
    tickets_dir = os.path.join(current_app.root_path, "static", "tickets")
    os.makedirs(tickets_dir, exist_ok=True)
    img.save(os.path.join(tickets_dir, f"{booking.id}.png"))


@booking_bp.route("/ticket/<int:booking_id>")
@login_required
def ticket(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id and not current_user.is_admin:
        flash("You cannot view this ticket.", "error")
        return redirect(url_for("events.list_events"))
    return render_template("ticket.html", booking=booking)


@booking_bp.route("/my-bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_time.desc()).all()
    return render_template("my_bookings.html", bookings=bookings)
