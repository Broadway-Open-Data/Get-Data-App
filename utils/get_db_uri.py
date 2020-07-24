"""
Broadway Database
"""
import os
import json
import sqlalchemy
import sys
from pathlib import Path

# set the path to the root
sys.path.append(".")



# ------------------------------------------------------------------------------
# make the url to be used for the sql engine

def get_db_uri(which_db="broadway"):
    """returns the uri for connecting to the db"""

    # get the credentials
    creds_path = Path(f"secret/{which_db.upper()}_CREDENTIALS.json")
    if os.path.isfile(creds_path):
        with open(creds_path, "r") as f:
            creds = json.load(f)
            username = creds.get("USERNAME")
            password = creds.get("PASSWORD")
    else:
        username = os.environ[f"{which_db.upper()}_USERNAME"]
        password = os.environ[f"{which_db.upper()}_PASSWORD"]

    # ------------------------------------------------------------------------------

    if which_db=="broadway":
        host = "open-broadway-data.cmftsskrmemn.us-east-1.rds.amazonaws.com"
    elif which_db=="users":
        host = "mvp-app-users.cmftsskrmemn.us-east-1.rds.amazonaws.com"

    # ------------------------------------------------------------------------------

    # Access the path and stuff
    drivername="mysql+pymysql"
    port = 3306
    dbname = which_db

    # ------------------------------------------------------------------------------
    connection_string = sqlalchemy.engine.url.URL(
        drivername=drivername,
        username=username,
        password=password,
        host=host,
        port=port,
        database=dbname
        )

    return connection_string
# ------------------------------------------------------------------------------
