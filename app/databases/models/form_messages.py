from databases import db, models
from sqlalchemy.orm import validates

import datetime



# ------------------------------------------------------------------------------

class FormMessage(db.Model, models.dbTable):
    """"""
    __tablename__ = "message"
    # Core
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column('user_id',db.Integer(), db.ForeignKey('user.id'))
    message = db.Column(db.String(400), nullable=False, unique=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -


    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Class method which finds user from DB by id
    @classmethod
    def get_form_message(self, user_id):
        """
        Gets the message the user made when signing up
        """
        return self.query.filter_by(user_id=user_id).first()
