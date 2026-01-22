import streamlit as st
import pandas as pd
import sqlite3


DB_PATH = "booking.db"


def get_all_bookings():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT 
        b.id AS booking_id,
        c.name,
        c.email,
        c.phone,
        b.booking_type,
        b.date,
        b.time,
        b.status,
        b.created_at
    FROM bookings b
    JOIN customers c ON b.customer_id = c.customer_id
    ORDER BY b.created_at DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def render_admin_dashboard():
    st.markdown("## 🔐 Admin Dashboard")
    st.caption("View all bookings stored in the system")

    df = get_all_bookings()

    if df.empty:
        st.warning("No bookings found.")
        return

    # Filters
    with st.expander("🔍 Filter Bookings"):
        name_filter = st.text_input("Filter by Name")
        email_filter = st.text_input("Filter by Email")

        if name_filter:
            df = df[df["name"].str.contains(name_filter, case=False, na=False)]

        if email_filter:
            df = df[df["email"].str.contains(email_filter, case=False, na=False)]

    st.dataframe(df, use_container_width=True)

    # Export CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Export Bookings to CSV",
        data=csv,
        file_name="booking_history.csv",
        mime="text/csv"
    )

    st.success(f"Total bookings: {len(df)}")
