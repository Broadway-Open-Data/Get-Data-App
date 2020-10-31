from databases import db, models
from . import BaseModel
from sqlalchemy.sql import expression

import datetime

# ------------------------------------------------------------------------------



class DataEditsValuesLink(db.Model, BaseModel):
    """Stores values as related by the data edits table"""
    __tablename__ = "data_edits_values_link"

    data_edits_id = db.Column(db.Integer,db.ForeignKey('broadway.data_edits.id'), primary_key=True)
    value_id = db.Column(db.Integer,db.ForeignKey('broadway.data_values.id'), primary_key=True)

    # Alternatively, use this value here to then decide if values are pre or post.... (and drop the extra table...)
    pre_or_post = db.Column(db.Boolean, nullable=False, comment='`0` represents `pre`, `1` represents `post`')

    def __repr__(self):
        return f"id: {self.data_edits_values_id}; value: {self.value_id}; {'PRE' if self.pre_or_post==0 else 'POST'}"


class DataValues(db.Model, BaseModel):
    """Stores values as related by the data edits table"""
    __tablename__ = "data_values"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(300), nullable=True, unique=False)

    def __repr__(self):
        return f"id: {self.id}; value: {self.value}"


# class DataEditsValues(db.Model, models.dbTable):
#     """Stores values as related by the data edits table"""
#     __tablename__ = "data_edits_values"
#     __table_args__ = {'schema':'broadway'}
#     __bind_key__ = "broadway"
#
#     # self
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     pre_or_post = db.Column(db.Boolean, nullable=False, comment='`0` represents `pre`, `1` represents `post`')
#
#     # Parent
#     data_edits_row_id = db.Column(db.Integer, db.ForeignKey('broadway.data_edits.id'), primary_key=True, comment='Primary key from `data_edits` table.')
#
#     # Children
#     data_values = db.relationship(DataValues, secondary='broadway.data_edits_values_link', backref=db.backref('broadway.data_edits_values', lazy='dynamic'), passive_deletes=True)
#
#
#     def __repr__(self):
#         return f"data_edits_row_id: {self.data_edits_row_id}; edit_id: {self.edit_id}, value_id: {self.value_id}"






class DataEdits(db.Model, BaseModel):
    """"""
    __tablename__ = "data_edits"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # can be used to groupby...
    user_edit_id = db.Column(db.Integer, nullable=False, unique=False, primary_key=True)
    edit_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # edit details
    table_name = db.Column(db.String(80), nullable=False, unique=False)
    value_primary_id = db.Column(db.Integer, nullable=False, unique=False) # This is the row referred to in the edit..

    field = db.Column(db.String(40), nullable=False, unique=False)
    field_type = db.Column(db.String(40), default="VARCHAR(40)", nullable=False, unique=False)


    value_pre = db.Column(db.String(300), nullable=True, unique=False)
    value_post = db.Column(db.String(300), nullable=False, unique=False)

    # Who made the edit ?
    edit_by = db.Column(db.String(40), nullable=False, unique=False)
    edit_comment = db.Column(db.String(300), nullable=True, unique=False)
    edit_citation = db.Column(db.String(200), nullable=True, unique=False)

    # who approved the edit?
    approved = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    approved_by = db.Column(db.String(40), nullable=False, unique=False)
    approved_comment = db.Column(db.String(300), nullable=True, unique=False)


    # Not including values here just yet...
    # data_values = db.relationship(DataValues, secondary='broadway.data_edits_values_link', backref=db.backref('broadway.data_edits_values', lazy='dynamic'), passive_deletes=True)










    # the basics
