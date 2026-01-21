import re
from datetime import datetime

def is_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False

def next_question(data):
    if not data["name"]:
        return "May I know your full name?"
    if not data["email"]:
        return "Please provide your email address."
    if not data["phone"]:
        return "Please provide your phone number."
    if not data["service"]:
        return "What service would you like to book?"
    if not data["date"]:
        return "Enter preferred date (YYYY-MM-DD)."
    if not data["time"]:
        return "Enter preferred time (HH:MM)."
    return None