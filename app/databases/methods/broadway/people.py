# from databases import db
from sqlalchemy.orm import load_only
from databases.models.broadway import Person, Show, ShowsRolesLink
import datetime as dt

# define a lambda to convert to datetime
year_to_dt = lambda x: dt.datetime(year=x, month=1, day=1)

def get_all_people(params={"from":1920, "to":1975}):
    """Returns a list of all people who performed on broadway in a given time period"""

    # Query all the shows in this time period
    valid_show_ids = Show.query.filter(
        Show.opening_date>=year_to_dt(params['from']),
        Show.opening_date>=year_to_dt(params['to']))\
        .with_entities(Show.id)\
        .subquery()


    all_people_ids = ShowsRolesLink.query.filter(
        ShowsRolesLink.show_id.in_(valid_show_ids))\
        .with_entities(ShowsRolesLink.person_id)\
        .subquery()


    all_people = Person.query.filter(
        Person.id.in_(all_people_ids)
        )\
        .all()


    print(f"There are {len(all_people):,} people on Broadway in the years between {params['from']}:{params['to']}")