import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = "golf.handicap.rechner@gmail.com"
EMAIL_PASSWORD = "dpchtqbcnxyqxyva"
EMAIL_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SEND_EMAILS = False

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