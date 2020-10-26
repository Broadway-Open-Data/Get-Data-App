from databases import db, models

from sqlalchemy.orm import validates
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref

from .roles import Role

import os
import datetime

# Password stuff
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

# ------------------------------------------------------------------------------




# ==============================================================================

class User(db.Model, UserMixin, models.dbTable):
    """"""
    __tablename__ = "user"
    __table_args__ = {'schema':'users'}
    __bind_key__ = "users"

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

    # Allow api keys
    api_key = db.Column(db.String(2400), nullable=True, unique=False)

    current_login_at = db.Column(db.DateTime, nullable=True)
    current_login_ip = db.Column(db.String(100), nullable=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    last_login_ip = db.Column(db.String(100), nullable=True)

    # Counts
    login_count = db.Column(db.Integer, default=0)
    request_pw_reset_count = db.Column(db.Integer, default=0)
    api_key_count = db.Column(db.Integer, default=0)
    n_api_requests = db.Column(db.Integer, default=0)

    # Allow different types of viewing modes – score as integers
    view_mode = db.Column(db.Integer, nullable=False, unique=False, default=0)

    # Additional
    roles = db.relationship(Role, secondary='users.roles_users',
                            backref=db.backref('users.users', lazy='dynamic'), passive_deletes=True)

    # Additional
    messages = db.relationship('FormMessage', secondary='users.messages_users',
                            backref=db.backref('users.users', lazy='dynamic'), passive_deletes=True)

    # --------------------------------------------------------------------------
    # STRING METHODS

    # Let the user see themselves
    def __repr__(self):
        return '<User {}>'.format(self.email)


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

    # Signup message
    def save_signup_message(self, message):
        """Set the message in the db."""
        message = models.users.FormMessage(
            user_id = self.id,
            message_type='signup',
            message = message
        )
        print(message.__dict__)
        message.save_to_db()

    # On signup
    def get_signup_message(self):
        """Access the message from the db."""
        return models.users.FormMessage.get_signup_message(self.id)
        # return models.users.FormMessage.query.filter_by(user_id=self.id).order_by(models.users.FormMessage.created_at.asc()).first()

    # --------------------------------------------------------------------------
    # INCREASE COUNTERS

    # Increase n times logged in
    def login_counter(self):
        if not self.login_count:
            self.login_count = 0
        self.login_count += 1
        self.save_to_db()

    # Increase n times logged in
    def save_ip(self, ip_address):
        self.ip_address = ip_address
        self.save_to_db()

    # Increase n times requested password reset
    def request_pw_reset_counter(self):
        if not self.request_pw_reset_count:
            self.request_pw_reset_count = 0
        self.request_pw_reset_count += 1
        self.save_to_db()


    def api_key_counter(self):
        if not self.api_key_count:
            self.api_key_count = 0
        self.api_key_count += 1
        self.save_to_db()

    def used_api_counter(self):
        if not self.n_api_requests:
            self.n_api_requests = 0
        self.n_api_requests += 1
        self.save_to_db()


    # def get_view_mode(self):
    #     return self.view_mode

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

    # Allow a user to get an api key
    def generate_api_key(self):
        """
        Expires in 180 days

        Look into this tool as a way of tightening security: https://gist.github.com/jpf/1e860e5ea70c0a70fd5e
        """

        token = {
            'user_email': self.email,
            'iat':datetime.datetime.utcnow(),
            'user_hashed_pw':self.password,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(days=180)
            }
        encoded_jwt = jwt.encode(token, algorithm='HS256', key=os.getenv('FLASK_SECRET_KEY'))

        # Update the db values
        self.api_key_counter()
        self.api_key = encoded_jwt
        self.save_to_db()
        return encoded_jwt

    # Allow a user to get an api key
    @classmethod
    def validate_api_key(self, token):
        """Unpacks the token -> then decodes it"""
        try:
            token = jwt.decode(token, algorithm=['HS256'], verify=True, key=os.getenv('FLASK_SECRET_KEY'))
            _user = self.find_user_by_email(token["user_email"])
            if _user.password == token["user_hashed_pw"]:
                _user.used_api_counter()
                return True

        except Exception as e:
            print(e)
            return

    # --------------------------------------------------------------------------

    def has_role(self, role_name):
        """Does this user have this permission?"""
        my_role = models.users.Role.get_by_name(name=role_name)
        if my_role in self.roles:
            return True
        else:
            return False

    def assign_role(self, role_name, assign_or_unassign='assign'):
        """Add this role to the user."""
        my_role = models.users.Role.get_by_name(name=role_name)

        # Only if you have a role...
        if my_role:

            # Add the role
            if assign_or_unassign=='assign':
                if my_role in self.roles:
                    None
                else:
                    self.roles.append(my_role)
                    self.save_to_db()

            # Remove the role
            elif assign_or_unassign=='unassign':
                if my_role in self.roles:
                    self.roles.remove(my_role)
                    self.save_to_db()
                else:
                    None

            # Option for continuing here.

    # --------------------------------------------------------------------------

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


    def delete_from_db(self):
        db.engine.execute(f"DELETE FROM roles_users WHERE user_id={self.id}")
        db.engine.execute(f"DELETE FROM message WHERE user_id={self.id}")
        db.engine.execute(f"DELETE FROM user WHERE id={self.id}")
