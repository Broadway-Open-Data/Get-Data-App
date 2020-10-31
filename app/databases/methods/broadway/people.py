import sys

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



def get_all_people(params, output_format='html'):

    """Returns a list of all people who performed on broadway in a given time period
    Note: We have no clue what the type of data "query_data" is
    """

    assert(isinstance(params, dict))
    assert(isinstance(output_format, str) and output_format in ('html','pandas','dict'))


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

    if output_format=='html':
        return df.to_html(header=True, na_rep='',bold_rows=False, index_names=False, index=False, render_links=True, classes='freeze-header')
    elif output_format=='pandas':
        return df
    elif output_format=='dict':
        return df.to_dict()




# ------------------------------------------------------------------------------

def get_all_directors(params, include_show_data_json=False, output_format='html'):
    """Returns all directors for this given period"""

    assert(isinstance(params, dict))
    assert(isinstance(output_format, str) and output_format in ('html','pandas','dict'))

    # Set defaults
    if not params.get('shows_year_from'):
        params['shows_year_from'] = 1950

    if not params.get('shows_year_to'):
        params['shows_year_to'] = 2020

    if not params.get('role_name'):
        params['role_name'] = 'director'


    # In python 3.8 and on, a "%" does not need special escaping.
    # In versions prior, special escaping ("%%") is needed.

    if sys.version_info.major==3:
        if sys.version_info.minor>=8: dt_format = '%m/%d/%Y'
        else: dt_format = '%%m/%%d/%%Y'
    # Maybe this works... ?
    else: dt_format = '%m/%d/%Y'

    query = f"""
            SELECT
        	person.id AS person_id,
        		 CONCAT_WS(
        			' ',
        			person.name_title,
        			person.f_name,
        			person.m_name,
        			person.l_name,
        			person.name_nickname,
        			person.name_suffix
        		) AS 'full_name',
        	 DATE_FORMAT(person.date_of_birth, '{dt_format}') AS date_of_birth,
             gender_identity.name as 'gender_identity',
             GROUP_CONCAT(DISTINCT racial_identity.name SEPARATOR ', ') as 'racial_identities',
        	 GROUP_CONCAT(JSON_OBJECT('id', shows.id, 'title', shows.title, 'year', shows.year, 'role', role.name)) AS show_data,
        	 COUNT(DISTINCT(shows.id)) AS 'n shows',
             MAX(shows.year)  - MIN(shows.year) AS 'n years directing',
             -- GROUP_CONCAT(DISTINCT role.name ) AS 'all roles',
             -- MIN(shows.year) AS 'earliest show year',
             MAX(shows.year) AS 'most recent show year',
             SUBSTRING_INDEX(GROUP_CONCAT(shows.title ORDER BY shows.opening_date DESC), ',', 1) AS 'most recent show'

        FROM
            shows
                INNER JOIN
            shows_roles_link ON shows_roles_link.show_id = shows.id
                INNER JOIN
            role ON role.id = shows_roles_link.role_id
            INNER JOIN
        		person ON person.id = shows_roles_link.person_id
            LEFT JOIN
        		gender_identity ON gender_identity.id = person.gender_identity_id
        	LEFT JOIN
        		racial_identity_lookup_table ON racial_identity_lookup_table.person_id = person.id
        	LEFT JOIN
        		racial_identity ON racial_identity.id = racial_identity_lookup_table.racial_identity_id

        WHERE(
                shows.year >= {params['shows_year_from']}
                AND shows.year <=  {params['shows_year_to']}
                AND (role.name LIKE '{params['role_name']}%%'
                OR role.name LIKE 'stage {params['role_name']}'
                OR role.name LIKE 'co-{params['role_name']}')
                {"AND role.name NOT LIKE '%%marketing' AND role.name NOT LIKE '%%manager%%'" if params['role_name']=='director' else ""}

        	)
        GROUP BY(person.id)
        ORDER BY  MAX(shows.year) DESC, MIN(shows.year) ASC
        ;
    """


    df = pd.read_sql(query, db.get_engine(bind='broadway'))

    if not include_show_data_json:
        df.drop(columns=['show_data'], inplace=True)

    # df.drop_duplicates(inplace=True) # <---- may not need to drop...

    if output_format=='html':

        # also, fix full name
        df['full_name'] = df['full_name'].str.title()

        # fix column names
        df.columns = df.columns.str.replace('_',' ').str.title()

        # fill in na
        df = df.fillna(value='')

        return df.to_html(header=True, na_rep='', bold_rows=False, index_names=False, index=False, render_links=True, classes=['freeze-header'])


    elif output_format=='pandas':
        return df
    elif output_format=='dict':
        return df.to_dict()






#
