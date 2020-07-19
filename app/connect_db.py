import os
import json
import sys
import datetime
import uuid

# Correct the path
sys.path.append(".")

import pandas as pd
import sqlalchemy
from sqlalchemy import MetaData, Table, select, and_, or_, not_
from sqlalchemy.orm import sessionmaker, scoped_session

# import utils
from utils.data_manipulation import flatten_to_string
from utils.get_db_uri import get_db_uri


# ------------------------------------------------------------------------------

# Use this resource https://www.pythonsheets.com/notes/python-sqlalchemy.html

# Now build the connection
SQLALCHEMY_DATABASE_URI = get_db_uri()
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI)


# build and bind the metadata
metadata = MetaData(bind=engine)
metadata.reflect()

# Use this if you don't want to use pandas...
# conn = engine.connect()

# Build your tables
shows = metadata.tables['shows']
theatres = metadata.tables['theatres']

# ------------------------------------------------------------------------------


def select_data(my_params={}, theatre_data=True):
    """
    Input a dictionary statement in dict format.
    Returns records from db.
    """

    # Must have a start and end year
    if "startYear" not in my_params.keys():
        my_params.update({"startYear":1900})

    if "endYear" not in my_params.keys():
        my_params.update({"endYear":2020})

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Reorganize your query

    query_structure = {
        "lists":{
            "show_type_simple":{
                "musicals":"Musical",
                "plays":"Play",
                "other_show_genre":["Opera","Burleque","Revue","Other","Concert","Special","Unknown",None]
            },
            "production_type":{
                "originals":"Original Production",
                "revivals":"Revival",
                "other_production_type":[
                    "Concert","Premiere", "Revised Production", "Concert Revival","Production", "Motion Picture", None]
                }
            },
        "bool":{

        }
    }

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    query_dict = {}

    # Which values do you want returned for each key?
    for key, value in query_structure["lists"].items():

        # Update to flat values
        flat_vals = flatten_to_string(
            [v for k,v in value.items() if my_params.get(k,True)]
            )
        query_dict.update({key:flat_vals})

    # --------------------------------------------------------------------------

    # Build the select statement

    select_st = select([shows]).\
        where(shows.c.year >= my_params["startYear"]).\
        where(shows.c.year <= my_params["endYear"]).\
        where(shows.c.show_type_simple.in_(query_dict["show_type_simple"])).\
        where(shows.c.production_type.in_(query_dict["production_type"]))

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    theatre_data = False
    if theatre_data:
        join_obj = shows.join(theatres, shows.c.theatre_id == theatres.c.id)

        # Update the select statement
        select_st =  select_st.select_from(join_obj)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Load to a pandas dataframe
    df = pd.read_sql(select_st, engine)
    return df


# ------------------------------------------------------------------------------


# Make an SQL call – using SQL sematic structure
# result = engine.execute('SELECT * FROM shows;')
# print(result.fetchall())


# ------------------------------------------------------------------------------
