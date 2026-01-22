# 🤖 AI Booking Assistant

An AI-powered web application that automates appointment booking through chat-based and manual options. The system supports PDF-based detail extraction, secure data storage, email confirmation, and an admin dashboard.

---

## 🚀 Key Features

- 💬 Chat-based appointment booking  
- 📝 Manual booking with optional PDF upload  
- 📄 Auto-fill details from PDFs (RAG-style)  
- 📧 Email confirmation using SMTP  
- 🗄️ SQLite database for booking storage  
- 🔐 Admin dashboard with CSV export  
- ☁️ Deployed on Streamlit Cloud  

---

## 🛠️ Tech Stack

- Frontend: Streamlit  
- Backend: Python  
- Database: SQLite  
- Email Service: SMTP (Gmail App Password)  
- Deployment: Streamlit Cloud  

---

## ▶️ Run Locally

git clone https://github.com/manaswinikila26/ai-booking-assistant.git
cd ai-booking-assistant
python -m pip install -r requirements.txt
python -m streamlit run app/main.py


## 🔐 Email Configuration

The application uses SMTP for sending booking confirmation emails.
Create a file at .streamlit/secrets.toml and add the following configuration:

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "yourgmail@gmail.com"
EMAIL_PASSWORD = "your_app_password"
Note:
  Use a Gmail App Password, not your regular Gmail password
  Do not commit this file to GitHub
  The same values must be added in Streamlit Cloud → App Settings → Secrets

## 🧪 Booking Flow
- User selects chat or manual booking
- Details are collected and validated
- Booking is saved in the database
- Confirmation email is sent
- Admin can view and export bookings

## 🔮 Future Improvements
- Advanced RAG processing
- Booking edit and cancellation
- Authentication and analytics

## 👤 Author
Kotha Venkata Manaswi Nikila
