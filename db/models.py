import sqlite3

def save_booking(data):
    conn = sqlite3.connect("bookings.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
        (data["name"], data["email"], data["phone"])
    )
    customer_id = cur.lastrowid

    cur.execute(
        """
        INSERT INTO bookings (customer_id, booking_type, date, time)
        VALUES (?, ?, ?, ?)
        """,
        (customer_id, data["service"], data["date"], data["time"])
    )

    booking_id = cur.lastrowid
    conn.commit()
    conn.close()
    return booking_id
