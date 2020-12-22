import sys
import os

# from databases import db
from sqlalchemy import select, and_
from databases.models.broadway import Person, Show, ShowsRolesLink, Role
from databases.models import db
import datetime as dt

import pandas as pd


# define a lambda to convert to datetime
year_to_dt = lambda x: dt.datetime(year=x, month=1, day=1)




def person_add_show_credit(**kwargs):
    """
    Some shows don't include all the people who worked on them. We want to fix that.

    -----
    Use as follows:
        my_params = dict(
            # show_id = 330662,
            show_name='Tuck Everlasting',
            show_year=2016,
            person_name='Mary Michell Campbell',
            role_name='Music Director'
        )
        person_add_show_credit(**my_params)
        >> success

    """
    show_id = kwargs.get('show_id')
    show_name = kwargs.get('show_name')
    show_year = kwargs.get('show_year')

    # You need show_id OR show name & year
    assert show_id or (show_name and show_year)

    person_id = kwargs.get('person_id')
    person_name = kwargs.get('person_name')
    assert person_id or person_name

    role_id = kwargs.get('role_id')
    role_name = kwargs.get('role_name')
    assert role_id or role_name

    # Step 1. Get the show
    if show_id:
        my_show = Show.get(show_id)
    else:
        my_show = Show.query.filter_by(title=show_name, year=show_year).first()

    # Step 2. Get "my_person"
    my_person = None; # remove when you're done debugging
    if person_id:
        my_person = Person.get(person_id)
    else:
        None
        # my_person = Person.query.filter_by( ... ).first()

    # Step 3. Is this person in this show?
    is_in_show = my_person in my_show.people
    print(f'My person is in my show: {is_in_show}')


    # Print all the people
    # for x in my_show.people:
    #     print(x.full_name)
    #     print(x.roles)

    # Step 4. Has this person had this role in this show?
    #   If they had a diff role, that would have been checked in step 3


    # Step 5. If not, add them...


    # Step 6. Commit
    db.session.rollback()












#
