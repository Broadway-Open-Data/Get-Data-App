# from databases import db
from sqlalchemy.orm import load_only
import sqlalchemy.sql.functions as func

from sqlalchemy import select
from databases.models.broadway import Person, Show, ShowsRolesLink, Role, GenderIdentity, RacialIdentity, race_table
from databases.models import db
import datetime as dt

import pandas as pd

# define a lambda to convert to datetime
year_to_dt = lambda x: dt.datetime(year=x, month=1, day=1)

def build_query_with_dict(base_query, params, myClass):
    """Assumes the objects are being entered correctly..."""

    table_name = myClass.__tablename__ + "_"
    numerical_fields = ['year','year_from','year_to','id']
    for key, value in params.items():

        # Only choose keys relevant to this table
        if key.startswith(table_name):

            # Get the field name
            field_name = key.replace(table_name,'')

            # convert int values
            if any([key.endswith(x) for x in numerical_fields]):
                value = int(value)

            # query strings with like
            if isinstance(value, str):
                base_query = base_query.filter(getattr(myClass, field_name).like(f"%%{value}%%"))

            # query numbers
            elif isinstance(value, int):

                # This would be helpful for mapping: https://stackoverflow.com/questions/10342700/tool-for-generating-sqlalchemy-queries-from-json-esque-values

                # perform grater or less than
                if '_from' in field_name:
                    field_name = field_name.replace('_from','')
                    base_query = base_query.filter(getattr(myClass, field_name) >= value)
                elif '_to' in field_name:
                    field_name = field_name.replace('_to','')
                    base_query = base_query.filter(getattr(myClass, field_name) <= value)

                # All others are equal to
                else:
                    base_query = base_query.filter(getattr(myClass, field_name)==value)

            else:
                # no clue what type this is...
                continue
    # finally return
    return base_query



def get_all_people(params):

    """Returns a list of all people who performed on broadway in a given time period
    Note: We have no clue what the type of data "query_data" is
    """

    # Query all shows in this selection
    valid_show_ids = Show.query.with_entities(Show.id, Show.title.label("show_title"), Show.year, Show.theatre_name)


    # Apply filters through subqueries...
    valid_show_ids = build_query_with_dict(valid_show_ids, params, Show)   #  <---  magic happens here
    valid_show_ids = valid_show_ids.subquery(with_labels=False)

    valid_roles = Role.query
    valid_roles = build_query_with_dict(valid_roles, params, Role) #  <---  magic happens here
    valid_roles = valid_roles.subquery(with_labels=False)


    # Get all people id...
    people_role_ids = ShowsRolesLink.query.filter(
        ShowsRolesLink.show_id.in_([valid_show_ids.c.id]),
        ShowsRolesLink.role_id.in_([valid_roles.c.id])
        )\
        .with_entities(
            ShowsRolesLink.person_id,
            ShowsRolesLink.role_id,
            ShowsRolesLink.show_id,
            valid_show_ids.c.show_title,
            valid_show_ids.c.year,
            valid_show_ids.c.theatre_name,
            ShowsRolesLink.extra_data.label("role_details"),
            valid_roles.c.name.label("role_name")
            )\
        .subquery()


    all_people = db.session.query(
            people_role_ids.c.show_id,
            people_role_ids.c.show_title,
            people_role_ids.c.year,
            people_role_ids.c.theatre_name,
            people_role_ids.c.role_name,
            people_role_ids.c.role_details,
            Person,
            GenderIdentity.name.label('gender_identity'),
            func.concat(RacialIdentity.name).label('racial identities'),
        )\
        .filter(Person.id.in_([people_role_ids.c.person_id]))\
        .join(
            people_role_ids,
            people_role_ids.c.person_id==Person.id,
            isouter=True
            )\
        .join(
            GenderIdentity,
            GenderIdentity.id==Person.gender_identity_id,
            isouter=True
            )\
        .join(
            race_table,
            race_table.c.person_id==Person.id,
            isouter=True
            )\
        .join(
            RacialIdentity,
            RacialIdentity.id==race_table.c.racial_identity_id,
            isouter=True
            )\
        .order_by(
            people_role_ids.c.year.asc(),
            people_role_ids.c.show_title.asc(),
            Person.l_name.asc(),
            Person.f_name.asc()
        )

    all_people = build_query_with_dict(all_people, params, Person)   #  <---  magic happens here
    all_people = all_people.subquery()


    df = pd.read_sql(all_people, db.get_engine(bind='broadway'))
    # df.drop_duplicates(inplace=True) # <---- may not need to drop...

    return df.to_html(header=True)













#
