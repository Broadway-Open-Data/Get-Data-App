from flask_mail import Mail, Message
from flask import current_app
from threading import Thread


def send_async_email(app, msg):
    mail = Mail(app)
    with app.app_context():
        mail.send(msg)

def send_email(recipients, subject,html):
    app = current_app._get_current_object()
    msg = Message(recipients=recipients, subject=subject, html=html, sender=app.config['MAIL_DEFAULT_SENDER'])
    app.logger.info(f"Message(to=[{recipients}], from='{msg.sender}')")
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
