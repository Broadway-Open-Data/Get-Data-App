# from databases import db
from sqlalchemy.orm import load_only
from databases.models.broadway import Person, Show, ShowsRolesLink
import datetime as dt

# define a lambda to convert to datetime
year_to_dt = lambda x: dt.datetime(year=x, month=1, day=1)

def build_query_with_dict(base_query, params, myClass):
    """Assumes the objects are being entered correctly..."""

    table_name = myClass.__tablename__ + "_"
    numerical_fields = ['year','id']
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


    # No more override
    # params = {"shows_year_from":2000, "shows_title":"into the woods"} # override


    # Query all shows in this selection
    valid_show_ids = Show.query.with_entities(Show.id)
    # Add filters
    valid_show_ids = build_query_with_dict(valid_show_ids, params, Show)
    valid_show_ids = valid_show_ids.subquery()


    # Get all people id...
    all_people_ids = ShowsRolesLink.query.filter(
        ShowsRolesLink.show_id.in_(valid_show_ids))\
        .with_entities(ShowsRolesLink.person_id)\
        .subquery()

    # Get all people
    all_people = Person.query.filter(
        Person.id.in_(all_people_ids)
        )
    # Add filters
    all_people = build_query_with_dict(all_people, params, Person)
    all_people = all_people.all()


    print(f"There are {len(all_people):,} people on Broadway within the params of {params}")
    return [r.__dict__ for r in all_people]







#
