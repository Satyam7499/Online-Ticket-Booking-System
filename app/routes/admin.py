from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Event, Seat, Booking

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Admin access required.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    total_events = Event.query.count()
    total_bookings = Booking.query.filter_by(payment_status="paid").count()
    revenue = db.session.query(db.func.sum(Event.price)).join(
        Booking, Booking.event_id == Event.id
    ).filter(Booking.payment_status == "paid").scalar() or 0
    return render_template(
        "admin_dashboard.html",
        total_events=total_events,
        total_bookings=total_bookings,
        revenue=revenue,
    )


@admin_bp.route("/events")
@login_required
@admin_required
def manage_events():
    events = Event.query.order_by(Event.id.desc()).all()
    return render_template("admin_events.html", events=events)


@admin_bp.route("/events/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_event():
    if request.method == "POST":
        name = request.form["name"].strip()
        date = request.form["date"].strip()
        venue = request.form["venue"].strip()
        price = float(request.form["price"])
        total_seats = int(request.form["total_seats"])

        event = Event(name=name, date=date, venue=venue, price=price, total_seats=total_seats)
        db.session.add(event)
        db.session.flush()  # get event.id before commit

        for i in range(1, total_seats + 1):
            db.session.add(Seat(event_id=event.id, seat_no=f"S{i}"))

        db.session.commit()
        flash("Event added.", "success")
        return redirect(url_for("admin.manage_events"))

    return render_template("admin_event_form.html", event=None)


@admin_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == "POST":
        event.name = request.form["name"].strip()
        event.date = request.form["date"].strip()
        event.venue = request.form["venue"].strip()
        event.price = float(request.form["price"])
        db.session.commit()
        flash("Event updated.", "success")
        return redirect(url_for("admin.manage_events"))

    return render_template("admin_event_form.html", event=event)


@admin_bp.route("/events/<int:event_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Event deleted.", "success")
    return redirect(url_for("admin.manage_events"))


@admin_bp.route("/bookings")
@login_required
@admin_required
def all_bookings():
    bookings = Booking.query.order_by(Booking.booking_time.desc()).all()
    return render_template("admin_bookings.html", bookings=bookings)
