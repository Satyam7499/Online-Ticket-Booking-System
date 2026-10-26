"""Create admin account and 20 sample events.
Run:
    python seed.py
"""

from app import create_app, db
from app.models import User, Event, Seat

app = create_app()

with app.app_context():

    # -------------------------------------------------
    # 1. CREATE ADMIN ACCOUNT
    # -------------------------------------------------
    if not User.query.filter_by(email="admin@ticket.com").first():
        admin = User(
            name="Admin",
            email="admin@ticket.com",
            is_admin=True
        )

        admin.set_password("admin123")
        db.session.add(admin)

        print("Created admin: admin@ticket.com / admin123")

    # -------------------------------------------------
    # 2. CREATE 20 EVENTS
    # -------------------------------------------------

    events = [
        {
            "name": "Coldplay Live in Mumbai",
            "date": "2026-10-15",
            "venue": "DY Patil Stadium",
            "price": 2500,
            "total_seats": 20
        },
        {
            "name": "Avengers: Doomsday",
            "date": "2026-09-20",
            "venue": "PVR Nashik",
            "price": 250,
            "total_seats": 15
        },
        {
            "name": "Arijit Singh Live Concert",
            "date": "2026-10-25",
            "venue": "Jio World Garden, Mumbai",
            "price": 1800,
            "total_seats": 30
        },
        {
            "name": "Diljit Dosanjh Live",
            "date": "2026-11-05",
            "venue": "MMRDA Grounds, Mumbai",
            "price": 2200,
            "total_seats": 25
        },
        {
            "name": "Sunburn Music Festival",
            "date": "2026-12-15",
            "venue": "NESCO Grounds, Mumbai",
            "price": 3000,
            "total_seats": 40
        },
        {
            "name": "Mumbai Comedy Night",
            "date": "2026-09-28",
            "venue": "NCPA, Mumbai",
            "price": 800,
            "total_seats": 20
        },
        {
            "name": "Marvel Movie Night",
            "date": "2026-10-02",
            "venue": "INOX, Mumbai",
            "price": 350,
            "total_seats": 30
        },
        {
            "name": "Bollywood Dance Show",
            "date": "2026-10-10",
            "venue": "Shanmukhananda Hall, Mumbai",
            "price": 900,
            "total_seats": 25
        },
        {
            "name": "The Grand Musical Show",
            "date": "2026-10-18",
            "venue": "Royal Opera House, Mumbai",
            "price": 1200,
            "total_seats": 20
        },
        {
            "name": "Rock Night Mumbai",
            "date": "2026-10-30",
            "venue": "Hard Rock Cafe, Mumbai",
            "price": 1500,
            "total_seats": 25
        },
        {
            "name": "Stand Up Comedy Special",
            "date": "2026-11-10",
            "venue": "Bal Gandharva Rang Mandir",
            "price": 700,
            "total_seats": 20
        },
        {
            "name": "Indian Classical Music Night",
            "date": "2026-11-15",
            "venue": "NCPA, Mumbai",
            "price": 1000,
            "total_seats": 20
        },
        {
            "name": "Football Championship",
            "date": "2026-11-20",
            "venue": "Mumbai Football Arena",
            "price": 600,
            "total_seats": 50
        },
        {
            "name": "Cricket Exhibition Match",
            "date": "2026-11-25",
            "venue": "Wankhede Stadium",
            "price": 1500,
            "total_seats": 50
        },
        {
            "name": "New Year Music Festival",
            "date": "2026-12-20",
            "venue": "BKC Grounds, Mumbai",
            "price": 2500,
            "total_seats": 40
        },
        {
            "name": "Hindi Movie Premiere",
            "date": "2026-12-05",
            "venue": "PVR ICON, Mumbai",
            "price": 500,
            "total_seats": 30
        },
        {
            "name": "Tech Conference 2026",
            "date": "2026-10-05",
            "venue": "Jio Convention Centre",
            "price": 1200,
            "total_seats": 35
        },
        {
            "name": "Food & Culture Festival",
            "date": "2026-10-22",
            "venue": "Bandra Kurla Complex",
            "price": 400,
            "total_seats": 40
        },
        {
            "name": "International Dance Festival",
            "date": "2026-11-02",
            "venue": "NCPA, Mumbai",
            "price": 1100,
            "total_seats": 25
        },
        {
            "name": "Christmas Celebration Night",
            "date": "2026-12-24",
            "venue": "Phoenix Marketcity, Mumbai",
            "price": 1000,
            "total_seats": 30
        }
    ]

    # -------------------------------------------------
    # 3. ADD EVENTS AND SEATS
    # -------------------------------------------------

    for event_data in events:

        # Check if event already exists
        existing_event = Event.query.filter_by(
            name=event_data["name"]
        ).first()

        if existing_event:
            print(f"Event already exists: {event_data['name']}")
            continue

        # Create event
        event = Event(
            name=event_data["name"],
            date=event_data["date"],
            venue=event_data["venue"],
            price=event_data["price"],
            total_seats=event_data["total_seats"]
        )

        db.session.add(event)

        # Flush so event gets an ID
        db.session.flush()

        # Create seats
        for i in range(1, event.total_seats + 1):
            seat = Seat(
                event_id=event.id,
                seat_no=f"S{i}"
            )

            db.session.add(seat)

        print(
            f"Created: {event.name} "
            f"({event.total_seats} seats)"
        )

    # -------------------------------------------------
    # 4. SAVE EVERYTHING
    # -------------------------------------------------

    db.session.commit()

    print("--------------------------------")
    print("Seeding completed successfully!")
    print("20 events have been added.")
    print("--------------------------------")