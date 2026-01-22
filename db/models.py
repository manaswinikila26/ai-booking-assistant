import sqlite3

DB_PATH = "booking.db"


def save_booking(data):
    """
    Saves customer and booking details into the database
    and returns the booking ID.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert customer details
    cursor.execute(
        """
        INSERT INTO customers (name, email, phone)
        VALUES (?, ?, ?)
        """,
        (
            data.get("name", ""),
            data.get("email", ""),
            data.get("phone", "")
        )
    )

    customer_id = cursor.lastrowid

    # Insert booking details
    cursor.execute(
        """
        INSERT INTO bookings (customer_id, booking_type, date, time)
        VALUES (?, ?, ?, ?)
        """,
        (
            customer_id,
            data.get("service", ""),
            data.get("date", ""),
            data.get("time", "")
        )
    )

    booking_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return booking_id

