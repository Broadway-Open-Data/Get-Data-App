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

def get_secret_creds(c_type):
    """returns the credentials for email usage"""

    # get the credentials
    creds_path = Path(f"secret/{c_type}_CREDENTIALS.json")
    # if os.environ['append_path']:
    #     creds_path = os.path.join("..", creds_path)

    if os.path.isfile(creds_path):
        with open(creds_path, "r") as f:
            creds = json.load(f)
            username = creds.get(f"{c_type}_USER")
            password = creds.get(f"{c_type}_PASSWORD")
    else:
        username = os.environ[f"{c_type}_USER"]
        password = os.environ[f"{c_type}_PASSWORD"]

    # ------------------------------------------------------------------------------
    return username, password
# ------------------------------------------------------------------------------
