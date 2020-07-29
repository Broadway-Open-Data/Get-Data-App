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


def format_dt(x):
    if isinstance(x, datetime.date):
        return x.strftime("%Y-%m-%d %H:%M:%S")

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
    # Core
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False, unique=False)
    website = db.Column(db.String(200), nullable=True, unique=False)
    instagram = db.Column(db.String(40), nullable=True, unique=False)

    # Internal stuff
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    approved = db.Column(db.Boolean, unique=False, default=False)
    approved_at = db.Column(db.DateTime)
    unapproved_at = db.Column(db.DateTime)
    authenticated = db.Column(db.Boolean, unique=False, default=False)
    authenticated_at = db.Column(db.DateTime)


    current_login_at = db.Column(db.DateTime, nullable=True)
    current_login_ip = db.Column(db.String(100), nullable=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    last_login_ip = db.Column(db.String(100), nullable=True)

    # Counts
    login_count = db.Column(db.Integer, default=0)
    request_pw_reset_count = db.Column(db.Integer, default=0)

    # Additional
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    # --------------------------------------------------------------------------
    # STRING METHODS

    # Let the user see themselves
    def __repr__(self):
        return '<User {}>'.format(self.email)

    # Define string method
    def __str__(self):
        return json.dumps({
            "id":self.id,
            "created_at":format_dt(self.created_at),
            "email":self.email,
            "website":self.website,
            "instagram":self.instagram,
            "approved":self.approved,
            "approved_at":format_dt(self.approved_at),
            "unapproved_at":format_dt(self.unapproved_at),
            "authenticated":self.authenticated,
            "authenticated_at":format_dt(self.authenticated_at),
            "login_count":self.login_count,
            "request_pw_reset_count":self.request_pw_reset_count,
        })

    # Get data for adding to df
    def __data__(self):
        return {
            "id":self.id,
            "created_at":self.created_at,
            "email":self.email,
            "website":self.website,
            "instagram":self.instagram,
            "approved":self.approved,
            "approved_at":self.approved_at,
            "unapproved_at":self.unapproved_at,
            "authenticated":self.authenticated,
            "authenticated_at":self.authenticated_at,
            "login_count":self.login_count,
            "request_pw_reset_count":self.request_pw_reset_count,
        }


    # --------------------------------------------------------------------------
    # Lookup methods

    # Class method which finds user from DB by email
    @classmethod
    def find_user_by_email(self, email):
        return self.query.filter_by(email=email).first()

    # Class method which finds user from DB by id
    @classmethod
    def find_user_by_id(self, _id):
        return self.query.filter_by(id=_id).first()


    # --------------------------------------------------------------------------
    # PASSWORD METHODS

    # Create a password...
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


    # --------------------------------------------------------------------------
    # UPDATE METHODS

    # Method to save user to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove user from DB
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Udate info
    def update_info(self, update_dict):
        self.query.filter_by(id=self.id).update(update_dict, synchronize_session=False)
        self.save_to_db()


    # --------------------------------------------------------------------------
    # INCREASE COUNTERS

    # Increase n times logged in
    def login_counter(self):
        if not self.login_count:
            self.login_count = 0
        self.login_count += 1
        self.save_to_db()

    # Increase n times requested password reset
    def request_pw_reset_counter(self):
        if not self.request_pw_reset_count:
            self.request_pw_reset_count = 0
        self.request_pw_reset_count += 1
        self.save_to_db()


    # --------------------------------------------------------------------------
    # GENERATE SECRET TOKEN

    # Allow a user to get a reset token
    def get_secret_token(self, n_minutes=30):
        """Expires in n minutes"""
        token = {'user_email': self.email, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=n_minutes)}
        encoded_jwt = jwt.encode(token, algorithm='HS256', key=os.getenv('FLASK_SECRET_KEY'))
        return encoded_jwt


    @classmethod
    def verify_secret_token(self, token):
        # Automatically checks if password hasnt expires
        try:
            reset_token = jwt.decode(token, algorithm=['HS256'], verify=True, key=os.getenv('FLASK_SECRET_KEY'))
            return self.query.filter_by(email=reset_token["user_email"]).first()

        except Exception as e:
            print(e)
            return

    # --------------------------------------------------------------------------
    # ADMIN ROLES
    def is_admin(self):
        """Will soon allow admin users with privelages"""
        if self.email in ["yaakovgs@gmail.com", "jocelynshek@gmail.com", "kamat2003@gmail.com", "stanislavlevitt@gmail.com"]:
            return True
        else:
            return False


    def approve(self):
        """Approve the user"""

        # Only update unapproved
        if self.approved:
            return
        else:
            self.approved = True
            self.approved_at = datetime.datetime.now()
            self.save_to_db()
            return True

    def unapprove(self):
        """Approve the user"""

        # Only update approved
        if self.approved:
            self.approved = False
            self.unapproved_at = datetime.datetime.now()
            self.save_to_db()
            return True
        else:
            return


    def authenticate(self):
        """Approve the user"""

        # Only update unapproved
        if not self.authenticated:
            self.authenticated = True
            self.authenticated_at = datetime.datetime.now()
            self.save_to_db()




# ==============================================================================
#                            BATCH METHODS
# ==============================================================================

def get_all_nonapproved_users(self):
    """Gets all users who aren't approved"""
    return User.query.filter_by(approved=False)




#
