from flask_mail import Mail, Message
from flask import current_app

def send_email(recipients, subject,html):
    app = current_app._get_current_object()
    mail = Mail(app)
    msg = Message(recipients=recipients, subject=subject, html=html)
    app.logger.info(f"Message(to=[{recipients}], from='{msg.sender}')")
    mail.send(msg)
