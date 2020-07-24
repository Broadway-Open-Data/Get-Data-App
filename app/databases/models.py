from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import app

# Import the app from the app
db = SQLAlchemy()

class User(db.Model):
    # id = db.Column(db.Int())
    email = db.Column(db.String(80), primary_key=True, unique=True)
    password = db.Column(db.String(80))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
