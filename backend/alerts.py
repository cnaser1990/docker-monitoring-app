import smtplib
from email.message import EmailMessage
import os
from datetime import datetime

SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
ALERT_EMAIL = os.getenv('ALERT_EMAIL')

alerts = []

def add_alert(message):
    """Add an alert to the list and attempt to send an email if configured."""
    alert = {"timestamp": datetime.utcnow().isoformat(), "message": message}
    alerts.append(alert)
    if len(alerts) > 100:
        alerts.pop(0)
    if SMTP_HOST and SMTP_HOST != 'smtp.example.com' and all([SMTP_USER, SMTP_PASSWORD, ALERT_EMAIL]):
        try:
            send_email("Docker Monitor Alert", message)
        except Exception as e:
            print(f"Failed to send email: {e}")

def get_alerts():
    """Return the list of recent alerts."""
    return alerts

def send_email(subject, body):
    """Send an email using SMTP."""
    print(f"Mock email: Subject: {subject}, Body: {body}")  # Debug log
    if SMTP_HOST == 'smtp.example.com':
        print("Skipping email: Placeholder SMTP host detected")
        return
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = ALERT_EMAIL
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
