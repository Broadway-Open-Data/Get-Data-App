from databases import db, models
from . import BaseModel
import datetime

from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property

# import custom stuff
from nameparser import HumanName

# --------------------------------------------------------------------------------



class ShowsRolesLink(db.Model, BaseModel):
    __tablename__ = "shows_roles_link"

    person_id = db.Column(db.Integer, db.ForeignKey('broadway.person.id'), primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('broadway.shows.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('broadway.role.id'), primary_key=True)
    extra_data = db.Column(db.String(256))
    url = db.Column(db.String(120), unique=False, nullable=True)



class Role(db.Model, BaseModel):
    __tablename__ = "role"

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
        db.Column('person_id', db.Integer(),db.ForeignKey('broadway.person.id')),
        db.Column('racial_identity_id', db.Integer(), db.ForeignKey('broadway.racial_identity.id')),
        info={'bind_key': 'broadway'},
        schema='broadway'
        )


class RacialIdentity(db.Model, BaseModel):
    __tablename__ = "racial_identity"


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

class GenderIdentity(db.Model, BaseModel):
    __tablename__ = "gender_identity"


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    # person = db.relationship('Person', backref="broadway.gender_identity",lazy="joined",join_depth=3)


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


class Person(db.Model, BaseModel):
    """"""
    __tablename__ = "person"


    id = db.Column(db.Integer,primary_key=True)
    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Regular name
    name_title =  db.Column(db.String(10), nullable=True, unique=False)
    f_name = db.Column(db.String(40), nullable=True, unique=False)
    m_name = db.Column(db.String(40), nullable=True, unique=False)
    l_name = db.Column(db.String(40), nullable=True, unique=False)
    name_suffix = db.Column(db.String(10), nullable=True, unique=False)
    name_nickname = db.Column(db.String(40), nullable=True, unique=False)

    @hybrid_property
    def full_name(self):
        """Return proper casing too"""
        name_list = [self.name_title, self.f_name, self.m_name, self.l_name, self.name_suffix, self.name_nickname]
        name_string = " ".join(map(str, name_list))
        full_name = HumanName(name_string)
        full_name.capitalize(force=True)
        return str(full_name)

    # Phonetic pronounciation
    phonetic_pronunciation_f_name = db.Column(db.String(60), nullable=True, unique=False)
    phonetic_pronunciation_m_name = db.Column(db.String(60), nullable=True, unique=False)
    phonetic_pronunciation_l_name = db.Column(db.String(60), nullable=True, unique=False)
    phonetic_pronunciation_nickname = db.Column(db.String(60), nullable=True, unique=False)

    @hybrid_property
    def phonetic_pronunciation(self):
        """Return full phonetic pronounciation"""
        name_list = [self.phonetic_pronunciation_f_name, self.phonetic_pronunciation_m_name, self.phonetic_pronunciation_l_name, self.phonetic_pronunciation_nickname]
        name_string = " ".join(map(str, name_list))
        return name_string


    url = db.Column(db.String(120), unique=False, nullable=True)
    date_of_birth = db.Column(db.DateTime, nullable=True) #  We should blur this -- or apply some anonymization technique

    # --------------------------------------------------------------------------
    # Here's where I need help with...
    # Convert this to a one to many...
    gender_identity_id = db.Column(db.Integer, db.ForeignKey('broadway.gender_identity.id'))
    gender_identity = db.relationship('GenderIdentity', backref="broadway.person",lazy="joined",join_depth=3)

    # --------------------------------------------------------------------------

    # one to many
    roles = relationship(Role, secondary='broadway.shows_roles_link', backref=db.backref('broadway.person', lazy='dynamic'), passive_deletes=True)
    shows = relationship('Show', secondary='broadway.shows_roles_link', backref=db.backref('broadway.person', lazy='dynamic'), passive_deletes=True)


    racial_identity = db.relationship('RacialIdentity', secondary='broadway.racial_identity_lookup_table', backref=db.backref('broadway.person', lazy='joined', join_depth=4), passive_deletes=True)


    # Additional fields
    country_of_birth = db.Column(db.String(40), nullable=True, unique=False)
    fluent_languages = db.Column(db.String(80), nullable=True, unique=False)


    # Assert is lowercase
    @validates(
        'f_name',
        'm_name',
        'l_name',
        # 'full_name',
        'phonetic_pronunciation_f_name',
        'phonetic_pronunciation_m_name',
        'phonetic_pronunciation_l_name',
        'phonetic_pronunciation_nickname',
        'country_of_birth',
        'fluent_languages',
        )
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
