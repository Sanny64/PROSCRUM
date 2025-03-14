import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="app/.env")

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SERVER = os.getenv("EMAIL_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")

SEND_EMAILS = True

def send_email(receiver, name, round_date):

    if not SEND_EMAILS:
        print("E-Mail-Versand deaktiviert")
        return

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = receiver
    msg["Subject"] = f"Rundenupdate vom {round_date}"
    msg.attach(MIMEText(f"Hallo {name}, \nvon einem Spielführer wurde Ihre Runde am {round_date} geupdatet.\nDies hat Auswirkungen auf Ihren akutellen Handicap-Index, bitte überprüfen sie diesen auf unserer Website. \n\nMit freundlichen Grüßen\nIhr Golf-Handicap-Rechner Team", "plain"))

    try:
        server = smtplib.SMTP(EMAIL_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, receiver, msg.as_string())
        print(f"Email an {receiver} erfolgreich gesendet")
    except Exception as e:
        print(f"Fehler beim Senden {e}")