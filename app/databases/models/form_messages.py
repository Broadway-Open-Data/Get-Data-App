from databases import db, models
from sqlalchemy.orm import validates

import datetime




# Define models


messages_users = db.Table('messages_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('message_id', db.Integer(), db.ForeignKey('message.id')))


# ------------------------------------------------------------------------------

class FormMessage(db.Model, models.dbTable):
    """"""
    __tablename__ = "message"
    # __table_args__ = {'extend_existing': True} # Don't use this...

    # Core
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column('user_id',db.Integer(), db.ForeignKey('user.id'))
    message_type = db.Column(db.String(40), default="generic", nullable=False, unique=False)
    message = db.Column(db.String(400), nullable=False, unique=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Assert is lowercase
    @validates('message_type')
    def convert_lower(self, key, value):
        return value.lower()


    # Class method which finds user from DB by id
    @classmethod
    def get_signup_message(self, user_id):
        """
        Gets the message the user made when signing up
        """
        return self.query.filter_by(user_id=user_id).order_by(self.created_at.asc()).first()
