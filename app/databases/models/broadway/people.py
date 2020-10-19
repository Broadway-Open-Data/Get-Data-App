from databases import db, models
from . import Base

import datetime

from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

# import custom stuff
from nameparser import HumanName



# --------------------------------------------------------------------------------



class ShowsRolesLink(db.Model, models.dbTable, Base):
    __tablename__ = "shows_roles_link"
    __bind_key__ = "broadway"
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    extra_data = db.Column(db.String(256))
    url = db.Column(db.String(120), unique=False, nullable=True)



class Role(db.Model, models.dbTable, Base):
    __tablename__ = "role"
    __bind_key__ = "broadway"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False) # All actors will be classified as "Performer"
    description = db.Column(db.String(255), unique=False, nullable=True)

    # models
    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Assert is lowercase
    @validates('name')
    def convert_lower(self, key, value):
        return value.lower()

    # Methods
    @classmethod
    def get_by_name(self, name):
        """Get the id, name, description of a role based on the role name"""
        return self.query.filter_by(name=name).first()

    def __repr__(self):
        return f"{self.id}: {self.name}"


# --------------------------------------------------------------------------------

race_table = db.Table('racial_identity_lookup_table',
        db.Column('person_id', db.Integer(),db.ForeignKey('person.id')),
        db.Column('racial_identity_id', db.Integer(), db.ForeignKey('racial_identity.id')),
        info={'bind_key': 'broadway'})


class RacialIdentity(db.Model, models.dbTable, Base):
    __tablename__ = "racial_identity"
    __bind_key__ = "broadway"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Assert is lowercase
    @validates('name')
    def convert_lower(self, key, value):
        return value.lower()

    # Methods
    @classmethod
    def get_by_name(self, name):
        """Get the id, name, description of a role based on the role name"""
        return self.query.filter_by(name=name).first()

    def __repr__(self):
        return f"{self.id}: {self.name}"

# --------------------------------------------------------------------------------

class GenderIdentity(db.Model, models.dbTable, Base):
    __tablename__ = "gender_identity"
    __bind_key__ = "broadway"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Assert is lowercase
    @validates('name')
    def convert_lower(self, key, value):
        return value.lower()

    # Methods
    @classmethod
    def get_by_name(self, name):
        """Get the id, name, description of a role based on the role name"""
        return self.query.filter_by(name=name).first()

    def __repr__(self):
        return f"{self.id}: {self.name}"


# --------------------------------------------------------------------------


class Person(db.Model, models.dbTable, Base):
    """"""
    __tablename__ = "person"
    __bind_key__ = "broadway"
    id = db.Column(db.Integer,primary_key=True)
    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


    name_title =  db.Column(db.String(10), nullable=True, unique=False)
    f_name = db.Column(db.String(40), nullable=True, unique=False)
    m_name = db.Column(db.String(40), nullable=True, unique=False)
    l_name = db.Column(db.String(40), nullable=True, unique=False)
    name_suffix = db.Column(db.String(10), nullable=True, unique=False)
    name_nickname = db.Column(db.String(40), nullable=True, unique=False)

    @hybrid_property
    def full_name(self):
        """Return proper casing too"""
        name_string = " ".join(list(filter(None, [self.name_title, self.f_name, self.m_name, self.l_name, self.name_suffix, self.name_nickname])))
        full_name = HumanName(name_string)
        full_name.capitalize()
        return str(full_name)


    url = db.Column(db.String(120), unique=False, nullable=True)
    #  Date of birth (or something blurred).
    date_of_birth = db.Column(db.DateTime, nullable=True)



    # --------------------------------------------------------------------------
    # Here's where I need help with...
    gender_identity_id = db.Column(db.Integer, db.ForeignKey('gender_identity.id'))
    gender_identity = db.relationship('GenderIdentity', backref="person")

    # --------------------------------------------------------------------------

    # one to many
    # roles = db.relationship('Role', secondary=roles_table, backref=db.backref('person', lazy='dynamic'), passive_deletes=True)
    roles = relationship('Role', secondary='shows_roles_link', backref=db.backref('person', lazy='dynamic'), passive_deletes=True)
    shows = relationship('Show', secondary='shows_roles_link', backref=db.backref('person', lazy='dynamic'), passive_deletes=True)

    racial_identity = db.relationship('RacialIdentity', secondary='racial_identity_lookup_table', backref=db.backref('person', lazy='dynamic'), passive_deletes=True)


    # Additional fields
    country_of_birth = db.Column(db.String(40), nullable=True, unique=False)
    fluent_languages = db.Column(db.String(80), nullable=True, unique=False)


    # Assert is lowercase
    @validates('f_name', 'm_name', 'l_name', 'full_name', 'country_of_birth', 'fluent_languages')
    def convert_lower(self, key, value):
        if isinstance(value, str):
            return value.lower()
        else:
            return value


    def edit_gender_identity(self, value):

        if self.gender_identity ==value:
            # Do nothing
            None
        else:
            my_gender = GenderIdentity.get_by_name(value)
            if not my_gender:
                my_gender = GenderIdentity(name=value)
                my_gender.save_to_db()

            # Now update
            self.update_info(update_dict={'gender_identity_id':my_gender.id})









#
