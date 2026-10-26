from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Event

events_bp = Blueprint("events", __name__)


@events_bp.route("/")
@events_bp.route("/events")
@login_required
def list_events():
    events = Event.query.order_by(Event.date).all()
    return render_template("events.html", events=events)
