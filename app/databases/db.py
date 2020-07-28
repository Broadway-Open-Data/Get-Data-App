import os
import enum
import json
import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import expression
from sqlalchemy.schema import Sequence
from flask_login import UserMixin
from flask_security import RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

db = SQLAlchemy()


#  USE THIS NEXT: https://github.com/smonagh/flask-password-reset/tree/master/app
#  AND THIS: https://exploreflask.com/en/latest/users.html

# ------------------------------------------------------------------------------
# Define your model
# ------------------------------------------------------------------------------

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# ------------------------------------------------------------------------------

class User(UserMixin, db.Model):
    """"""
    __tablename__ = "user"
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False, unique=False)
    website = db.Column(db.String(200), nullable=True, unique=False)
    instagram = db.Column(db.String(40), nullable=True, unique=False)

    # Internal stuff
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)

    current_login_at = db.Column(db.DateTime, nullable=True)
    current_login_ip = db.Column(db.String(100), nullable=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    last_login_ip = db.Column(db.String(100), nullable=True)

    login_count = db.Column(db.Integer, default=0)
    reset_password_count = db.Column(db.Integer, default=0)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    # ==========================================================================

    # Create a password...
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Let the user see themselves
    def __repr__(self):
        return '<User {}>'.format(self.email)


    # Define string method
    def __str__(self):
        return json.dumps({
            "id":self.id,
            "created_at":self.created_at.strftime("%Y-%m-%d %H:%M:%s"),
            "email":self.email,
            "website":self.website,
            "instagram":self.instagram,
            "login_count":self.login_count,
            "reset_password_count":self.reset_password_count,
        })

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Method to save user to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove user from DB
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Udate info
    def increase_login_count(self):
        if not self.login_count:
            self.login_count = 0
        self.login_count += 1
        self.save_to_db()

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    def increase_reset_password_count(self):
        if not self.reset_password_count:
            self.reset_password_count = 0
        self.reset_password_count += 1
        self.save_to_db()

    # Udate info
    def update_info(self, update_dict):
        self.query.filter_by(id=self.id).update(update_dict, synchronize_session=False)
        self.save_to_db()

    # Class method which finds user from DB by email
    @classmethod
    def find_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    # Class method which finds user from DB by id
    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Allow a user to get a reset token
    def get_reset_token(self, n_minutes=30):
        """Expires in n minutes"""
        reset_token = {'user_email': self.email, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=n_minutes)}
        encoded_jwt = jwt.encode(reset_token, algorithm='HS256', key=os.getenv('FLASK_SECRET_KEY'))
        return encoded_jwt

    @classmethod
    def verify_reset_token(cls, token):

        # Automatically checks if password hasnt expires
        try:
            reset_token = jwt.decode(token, algorithm=['HS256'], verify=True, key=os.getenv('FLASK_SECRET_KEY'))
            return cls.query.filter_by(email=reset_token["user_email"]).first()

        except Exception as e:
            print(e)
            return









#
