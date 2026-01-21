import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    try:
        smtp_host = st.secrets["EMAIL_HOST"]
        smtp_port = st.secrets["EMAIL_PORT"]
        sender = st.secrets["EMAIL_USER"]
        password = st.secrets["EMAIL_PASSWORD"]

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        st.error(f"Email Error: {e}")
        return False
