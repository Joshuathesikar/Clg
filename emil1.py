import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def end_email(to_email, plate_number):
    sender_email = "joshuathesikar@gmail.com"
    app_password = "gdsa xvym jjzg qzcu"  # Use an App Password from Google

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "Helmet Violation Alert"

    body = f"Violation detected! Vehicle with number {plate_number} was found without a helmet. Please take necessary action."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
