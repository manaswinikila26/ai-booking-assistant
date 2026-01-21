import streamlit as st
import re

from db.database import init_db
from db.models import save_booking
from app.tools import send_email
from app.booking_flow import is_email, is_date
from app.admin_dashboard import render_admin_dashboard
from app.rag_pipeline import extract_text_from_pdfs

st.set_page_config(page_title="Booking AI", layout="wide")
init_db()

# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_booking" not in st.session_state:
    st.session_state.chat_booking = {}

if "chat_step" not in st.session_state:
    st.session_state.chat_step = None

# ================= LANDING PAGE =================
if st.session_state.page == "landing":
    st.markdown(
        "<h1 style='text-align:center;'>Smart Booking,<br>Powered by AI</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;'>Automate scheduling with an intelligent assistant.</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([4, 2, 4])
    with col2:
        if st.button("🚀 Try the Demo"):
            st.session_state.page = "chat"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("💬 Natural Conversations")
    with c2:
        st.info("📄 Document Knowledge")
    with c3:
        st.info("⚡ Instant Scheduling")

# ================= CHAT PAGE =================
elif st.session_state.page == "chat":
    left, right = st.columns([6, 2])
    with left:
        st.markdown("## Booking Assistant")
        st.caption("Chat with AI to answer questions or schedule appointments.")
    with right:
        if st.button("📋 Book Appointment Manually"):
            st.session_state.page = "booking"
            st.rerun()

    st.success("🟢 AI Assistant Online")

    if not st.session_state.messages:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! You can chat with me to book an appointment or ask questions."
        })

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        reply = ""

        if "book" in user_input.lower() and st.session_state.chat_step is None:
            reply = "Sure 😊 What is your full name?"
            st.session_state.chat_step = "name"

        elif st.session_state.chat_step == "name":
            st.session_state.chat_booking["name"] = user_input
            reply = "Please enter your email address"
            st.session_state.chat_step = "email"

        elif st.session_state.chat_step == "email":
            if not is_email(user_input):
                reply = "❌ Invalid email. Please enter a valid email."
            else:
                st.session_state.chat_booking["email"] = user_input
                reply = "Please enter your phone number"
                st.session_state.chat_step = "phone"

        elif st.session_state.chat_step == "phone":
            if not user_input.isdigit() or len(user_input) != 10:
                reply = "❌ Phone number must be 10 digits."
            else:
                st.session_state.chat_booking["phone"] = user_input
                reply = "What service would you like to book?"
                st.session_state.chat_step = "service"

        elif st.session_state.chat_step == "service":
            st.session_state.chat_booking["service"] = user_input
            reply = "Enter preferred date (YYYY-MM-DD)"
            st.session_state.chat_step = "date"

        elif st.session_state.chat_step == "date":
            if not is_date(user_input):
                reply = "❌ Invalid date format. Use YYYY-MM-DD."
            else:
                st.session_state.chat_booking["date"] = user_input
                reply = "Enter preferred time (HH:MM)"
                st.session_state.chat_step = "time"

        elif st.session_state.chat_step == "time":
            st.session_state.chat_booking["time"] = user_input
            b = st.session_state.chat_booking
            reply = (
                f"Please confirm your booking:\n\n"
                f"👤 Name: {b['name']}\n"
                f"📧 Email: {b['email']}\n"
                f"📞 Phone: {b['phone']}\n"
                f"🛎 Service: {b['service']}\n"
                f"📅 Date: {b['date']}\n"
                f"⏰ Time: {b['time']}\n\n"
                f"Type YES to confirm or NO to cancel."
            )
            st.session_state.chat_step = "confirm"

        elif st.session_state.chat_step == "confirm":
            if user_input.lower() == "yes":
                booking_id = save_booking(st.session_state.chat_booking)
                send_email(
                    st.session_state.chat_booking["email"],
                    "Booking Confirmation",
                    f"Your booking is confirmed.\nBooking ID: {booking_id}"
                )
                reply = f"✅ Booking confirmed! Your Booking ID is {booking_id}"
            else:
                reply = "❌ Booking cancelled."

            st.session_state.chat_booking = {}
            st.session_state.chat_step = None

        else:
            reply = "I can help you book an appointment or answer your questions."

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

# ================= MANUAL BOOKING PAGE =================
elif st.session_state.page == "booking":
    st.markdown("## Book an Appointment (Manual)")

    uploaded = st.file_uploader("Upload PDF to auto-fill details (optional)", type=["pdf"])
    booking_data = {"name": "", "email": "", "phone": "", "service": "", "date": "", "time": ""}

    if uploaded:
        text = extract_text_from_pdfs([uploaded])
        email = re.search(r"[\w\.-]+@[\w\.-]+", text)
        phone = re.search(r"(?:\+91)?[6-9]\d{9}", text)
        booking_data["email"] = email.group() if email else ""
        booking_data["phone"] = phone.group() if phone else ""
        st.success("Details extracted from PDF")

    with st.form("manual_booking"):
        booking_data["name"] = st.text_input("Full Name", booking_data["name"])
        booking_data["email"] = st.text_input("Email", booking_data["email"])
        booking_data["phone"] = st.text_input("Phone", booking_data["phone"])
        booking_data["service"] = st.text_input("Service")
        booking_data["date"] = st.text_input("Date (YYYY-MM-DD)")
        booking_data["time"] = st.text_input("Time (HH:MM)")
        submit = st.form_submit_button("Confirm Booking")

    if submit:
        booking_id = save_booking(booking_data)
        send_email(
            booking_data["email"],
            "Booking Confirmation",
            f"Your booking is confirmed.\nBooking ID: {booking_id}"
        )
        st.success(f"✅ Booking confirmed! ID: {booking_id}")

# ================= ADMIN PAGE =================
elif st.session_state.page == "admin":
    render_admin_dashboard()
