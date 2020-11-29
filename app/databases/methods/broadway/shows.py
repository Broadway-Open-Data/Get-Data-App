from databases.models.broadway import Show, ShowsRolesLink, Role, Person, GenderIdentity, RacialIdentity, race_table, DataEdits
from databases.methods.broadway import build_query_with_dict
from databases.models import db
from sqlalchemy import func, Integer
from sqlalchemy.sql.expression import cast

import datetime as dt

import pandas as pd
# from flask_login import current_user

def get_all_shows(params, output_format='pandas'):

    """Returns a list of all shows on broadway in a given time period.

    Note: We have no clue what the type of data "query_data" is
    """
    assert(isinstance(params, dict))
    assert(isinstance(output_format, str) and output_format in ('html','pandas','dict'))

    # To do:
    # 1. Rename params to include prefix connoting the field and value
    # 2. Dynamically loop over fields and filter for values
    # What we're working with:
    #   {'musicals': True, 'plays': True, 'originals': True, 'revivals': True, 'shows_year_from': 1990, 'shows_year_to': 2020}


    # Go through the following steps:
    # 1. Show genre (music/play)
    # 2. Production type (original/revival)
    # 3. Date range
    # 4. Tony award (winner/nominee/none)
    # 5. Theater size (how many seats can it sit?)
    # 6. Cast size (int)
    # 7. Include theater info? (a sql join is all...)

    # --------------------------------------------------------------------------

    # Query all shows in this selection
    valid_shows = db.session.query(
            Show.id.label("Show ID"),
            Show.title.label("Show Title"),
            Show.year.label("Year"),
            Show.previews_date.label("Previews Date"),
            Show.opening_date.label("Opening Date"),
            Show.closing_date.label("Closing Date"),
            Show.theatre_name.label("Theatre Name"),
            Show.production_type.label("Production Type"),
            Show.show_type.label("Show Type"),
            Show.show_type_simple.label("Show Type (Simple)"),
            Show.intermissions.label("Intermissions"),
            Show.n_performances.label("N Performances"),
            Show.run_time.label("Run Time"),
            Show.show_never_opened.label("Show Not Opened"),
            Show.revival.label("Revival"),
            Show.other_titles.label("Other Titles"),
            Show.official_website.label("Official Website"),
            func.COUNT(func.DISTINCT(ShowsRolesLink.person_id)).cast(Integer).label('N People'),
            func.SUM(func.IF(Role.name == 'performer', 1, 0)).cast(Integer).label('N Performers'),
            func.SUM(func.IF(Role.name != 'performer', 1, 0)).cast(Integer).label('N Creative Team'),
        )\
        .join(
            ShowsRolesLink,
            Show.id == ShowsRolesLink.show_id,
        )\
        .join(
            Role,
            Role.id == ShowsRolesLink.role_id,
        )\
        .filter(
            Show.year >= params['shows_year_from'],
            Show.year <= params['shows_year_from']
            )\
        .group_by(
            Show.id
        )\
        .subquery()



    # Now, apply filters to subquery as needed...
    # valid_shows = db.session.query(
    #         valid_shows,
    #
    #     )\
    #     .group_by(
    #         valid_shows.c['Show ID']
    #     )\
    #     .subquery()



    df = pd.read_sql(valid_shows, db.get_engine(bind='broadway'))
    # df.drop_duplicates(inplace=True) # <---- may not need to drop...

    if output_format=='html':
        return df.to_html(header=True, na_rep='',bold_rows=False, index_names=False, index=False, render_links=True, classes='freeze-header')

    elif output_format=='pandas':
        return df

    elif output_format=='dict':
        return df.to_dict()





    # # Apply filters through subqueries...
    # valid_show_ids = build_query_with_dict(valid_show_ids, params, Show)   #  <---  magic happens here
    # valid_show_ids = valid_show_ids.subquery(with_labels=False)
    #
    # valid_roles = Role.query
    # valid_roles = build_query_with_dict(valid_roles, params, Role) #  <---  magic happens here
    # valid_roles = valid_roles.subquery(with_labels=False)
    #
    #
    # # Get all people id...
    # people_role_ids = ShowsRolesLink.query.filter(
    #     ShowsRolesLink.show_id.in_([valid_show_ids.c.id]),
    #     ShowsRolesLink.role_id.in_([valid_roles.c.id])
    #     )\
    #     .with_entities(
    #         ShowsRolesLink.person_id,
    #         ShowsRolesLink.role_id,
    #         ShowsRolesLink.show_id,
    #         valid_show_ids.c.show_title,
    #         valid_show_ids.c.year,
    #         valid_show_ids.c.theatre_name,
    #         ShowsRolesLink.extra_data.label("role_details"),
    #         valid_roles.c.name.label("role_name")
    #         )\
    #     .subquery()
    #
    #
    # all_people = db.session.query(
    #         people_role_ids.c.show_id,
    #         people_role_ids.c.show_title,
    #         people_role_ids.c.year,
    #         people_role_ids.c.theatre_name,
    #         people_role_ids.c.role_name,
    #         people_role_ids.c.role_details,
    #         Person,
    #         GenderIdentity.name.label('gender_identity'),
    #         func.concat(RacialIdentity.name).label('racial identities'),
    #     )\
    #     .filter(Person.id.in_([people_role_ids.c.person_id]))\
    #     .join(
    #         people_role_ids,
    #         people_role_ids.c.person_id==Person.id,
    #         isouter=True
    #         )\
    #     .join(
    #         gender_table,
    #         gender_table.c.person_id==Person.id,
    #         isouter=True
    #         )\
    #     .join(
    #         GenderIdentity,
    #         GenderIdentity.id==gender_table.c.gender_identity_id,
    #         isouter=True
    #         )\
    #     .join(
    #         race_table,
    #         race_table.c.person_id==Person.id,
    #         isouter=True
    #         )\
    #     .join(
    #         RacialIdentity,
    #         RacialIdentity.id==race_table.c.racial_identity_id,
    #         isouter=True
    #         )\
    #     .order_by(
    #         people_role_ids.c.year.asc(),
    #         people_role_ids.c.show_title.asc(),
    #         Person.l_name.asc(),
    #         Person.f_name.asc()
    #     )
    #
