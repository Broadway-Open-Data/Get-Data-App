from databases.models.broadway import Show, Theatre, ShowsRolesLink, Role, Person, GenderIdentity, RacialIdentity, race_table, DataEdits
from databases.methods.broadway import build_query_with_dict
from databases.models import db
from sqlalchemy import func, Integer, and_, or_
from sqlalchemy.sql.expression import cast
from sqlalchemy.dialects.mysql import JSON

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
        },
        'person':{
            'name':'full_name'
        }
    }


    new_params = {}
    for key, value in params.items():
        # These are required for each query...
        if key in ['show_year_from', 'show_year_to']:
            continue

        if key.endswith('_include'):
            continue

        # Always have 3 values
        k1, k2, k3 = key.replace('_ADVANCED','').split('_')

        # Try to update k2:
        k2 = field_name_mapper.get(k1,{}).get(k2,k2)

        if k1 not in new_params.keys():
            new_params[k1] = {}

        if k2 not in new_params[k1].keys():
            new_params[k1][k2] = []
        # ex: show_genre_musical: True
        if isinstance(value, bool):
            new_params[k1][k2].append(k3)
        # ex: 'show_title_str': 'red'
        elif isinstance(value, str) and k3=='str':
            new_params[k1][k2] = value


    # done...
    q_cols = [
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
    ]
    # --------------------------------------------------------------------------
    # Include additional info?
    if params.get('person_info_include'):
        q_cols.extend([
            func.json_arrayagg(
                func.json_object(
                    'person_id', Person.id,
                    'role_name', Role.name,
                    'f_name', Person.f_name,
                    'm_name', Person.m_name,
                    'l_name', Person.l_name,
                    'name_suffix',Person.name_suffix,
                    'name_title', Person.name_title,
                    'name_nickname', Person.name_nickname,
                    'url', Person.url,
                    )
                )\
                .label('Person Data')
        ])

    # --------------------------------------------------------------------------
    if params.get('theatre_info_include'):
        q_cols.extend([
            Theatre.id.label('theatre_id'),
            Theatre.name.label('Theatre Name'),
            func.CONCAT_WS(' ',
                Theatre.street_address,
                Theatre.address_locality,
                Theatre.address_region,
                Theatre.postal_code
                )\
                .label('Theatre Full Address'),
            Theatre.street_address.label('Theatre Street Address'),
            Theatre.address_locality.label('Theatre Address Locality'),
            Theatre.address_region.label('Theatre Address Region'),
            Theatre.postal_code.label('Theatre Postal Code'),
            Theatre.year_closed.label('Theatre Year Closed'),
            Theatre.year_demolished.label('Theatre Year Demolished'),
            Theatre.capacity.label('Theatre Capacity'),
        ])


    # --------------------------------------------------------------------------

    my_query = db.session.query(
        *q_cols
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
        .join(
            Person,
            Person.id == ShowsRolesLink.person_id,
            isouter=True
        )\
        .join(
            Theatre,
            Theatre.id == Show.theatre_id,
            isouter=True
        )\
        .group_by(
            Show.id
        )\
        .order_by(
            Show.year,
            Show.opening_date
        )\
        .filter(
            Show.year.between(params['show_year_from'],params['show_year_to'])
        )


    # Now, iterate over the new params...
    my_class_objects = {
        'show':Show,
        'theatre':Theatre,
        'person':Person
    }

    # chain query...
    for key, value in new_params.items():
        ClassObject = my_class_objects[key]
        # Will either be a list or a str value:
        for k,v in value.items():
            # string lookup
            if isinstance(v, str):
                # if its a full name...
                if key=='person' and k == 'name':
                    my_query = my_query.filter(
                        func.lower(func.CONCAT_WS(
                            ' ',
                            Person.f_name,
                            Person.m_name,
                            Person.l_name,
                            )
                        ).like('%' + value.lower() + '%')
                    )
                else:
                    my_query = my_query.filter(
                        func.lower(
                            getattr(ClassObject, k)
                        ).like('%' + v.lower() + '%')
                    )
            # otherwise, check if in this list...
            elif isinstance(v, list):
                my_query = my_query.filter(
                    getattr(ClassObject, k).in_(v)
                )



    # finally
    my_query = my_query.subquery(with_labels=False)


    df = pd.read_sql(my_query, db.get_engine(bind='broadway'))
    # df.drop_duplicates(inplace=True) # <---- may not need to drop...
    # styles = [dict(selector='.col3', props=[('min-width', '300px')]), dict(selector='.data', props=[('min-width', '6em')])]



    if output_format=='html':
        # if 'Person Data' in df.columns:
        #     df = df.style.set_properties(
        #         subset=['Person Data'],
        #         **{
        #             'width': '100px',
        #             'max-width': '100px',
        #             'overflow':'hidden',
        #             'text-overflow':'ellipsis',
        #             'white-space':'nowrap',
        #         }
        #     )
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
