from databases.models.broadway import Show, Theatre, ShowsRolesLink, Role, Person, GenderIdentity, RacialIdentity, race_table, DataEdits
from databases.methods.broadway import build_query_with_dict
from databases.models import db
from sqlalchemy import func, Integer, and_, or_
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

    # Sometimes we use diff names than the db...
    field_name_mapper = {
        'show':{
            'genre':'show_type_simple',
            'type':'production_type_simple'
        }
    }

    # Filter with these queries...
    my_filters = {
        'show':{'classObject':Show},
        'theatre':{'classObject':Theatre, 'query':Theatre.query},
        'person':{'classObject':Person, 'query':Person.query}
    }

    for key, value in params.items():
        # skip these guys
        if key in ['show_year_from', 'show_year_to'] or key.endswith('ADVANCED'):
            continue

        rich_key = key.split('_')

        # These are all boolean...
        if len(rich_key)==3:
            # Unpack
            class_name, field_name, field_value = rich_key
            # Try to update if you can...
            field_name = field_name_mapper.get(class_name,{}).get(field_name, field_name)

            if class_name not in my_filters.keys():
                my_filters[class_name] = {}

            if field_name not in my_filters[class_name].keys():
                my_filters[class_name][field_name] = []

            r = {
                'field_name':field_name,
                'field_value':field_value.title(),
                'operator':'=='
            }

            my_filters[class_name][field_name].append(r)

    # Now build the filters
    for class_name, class_values in my_filters.items():

        myClassObject = class_values['classObject']

        my_filters[class_name]['query'] = myClassObject.query\
            .filter(
            and_(*[
                or_(*[getattr(myClassObject, field_name) == x['field_value'] for x in field_values
                ]) # action for total level 2
                for field_name, field_values in class_values.items() if isinstance(field_values, list) # logic level 1
                ]) # action for total level 1
            )


    # Get this
    Show_q = my_filters['show']['query'].subquery(with_labels=False)
    # Theatre_q = my_filters['theatre']['query'].subquery(with_labels=False)
    # Person_q = my_filters['person']['query'].subquery(with_labels=False)


    my_query = db.session.query(
            Show.id.label("show_id"),
            Show.title.label("Show Title"),
            Show.year.label("Year"),
            Show.previews_date.label("Previews Date"),
            Show.opening_date.label("Opening Date"),
            Show.closing_date.label("Closing Date"),
            Show.theatre_name.label("Theatre Name"),
            Show.production_type.label("Production Type"),
            Show.show_type.label("Show Type"),
            Show.show_type_simple.label("Show Type (Simple)"),
            Show.intermissions.cast(Integer).label("Intermissions"),
            Show.n_performances.cast(Integer).label("N Performances"),
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
            isouter=True
        )\
        .join(
            Role,
            Role.id == ShowsRolesLink.role_id,
            isouter=True
        )\
        .filter(
            and_(
                Show.year >= params['show_year_from'],
                Show.year <= params['show_year_to'],
                Show.id == Show_q.c.id,
                )
            )\
        .group_by(
            Show.id
        )\
        .order_by(
            Show.year,
            Show.opening_date
        )\
        .subquery(with_labels=False)

    # Perform a union (or an inner join?)


    # my_query = db.session.query(my_query)\
    #     .join(
    #         Show_q,
    #         Show_q.c.id == my_query.c.show_id,
    #     )

    # my_query = my_query.subquery(with_labels=False)
    # Now, apply filters to subquery as needed...
    # valid_shows = db.session.query(
    #         valid_shows,
    #
    #     )\
    #     .group_by(
    #         valid_shows.c['Show ID']
    #     )\
    #     .subquery()


    df = pd.read_sql(my_query, db.get_engine(bind='broadway'))
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
