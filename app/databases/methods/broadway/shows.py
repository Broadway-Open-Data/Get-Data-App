from databases.models.broadway import Show, Person, GenderIdentity, RacialIdentity, race_table, DataEdits
from databases.methods.broadway import build_query_with_dict
from databases.models import db
import datetime as dt

# from flask_login import current_user

print("this works")

def get_all_shows(params, output_format='html'):

    """Returns a list of all shows on broadway in a given time period.

    Note: We have no clue what the type of data "query_data" is
    """

    assert(isinstance(params, dict))
    assert(isinstance(output_format, str) and output_format in ('html','pandas','dict'))

    # Go through the following steps:
    # 1. Show genre (music/play)
    # 2. Production type (original/revival)
    # 3. Date range
    # 4. Tony award (winner/nominee/none)
    # 5. Theater size (how many seats can it sit?)
    # 6. Cast size (int)
    # 7. Include theater info? (a sql join is all...)


    # --------------------------------------------------------------------------
    # # Query all shows in this selection
    # valid_show_ids = Show.query.with_entities(Show.id, Show.title.label("show_title"), Show.year, Show.theatre_name)
    #
    #
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
    # all_people = build_query_with_dict(all_people, params, Person)   #  <---  magic happens here
    # all_people = all_people.subquery()
    #
    #
    # df = pd.read_sql(all_people, db.get_engine(bind='broadway'))
    # # df.drop_duplicates(inplace=True) # <---- may not need to drop...
    #
    # if output_format=='html':
    #     return df.to_html(header=True, na_rep='',bold_rows=False, index_names=False, index=False, render_links=True, classes='freeze-header')
    # elif output_format=='pandas':
    #     return df
    # elif output_format=='dict':
    #     return df.to_dict()
