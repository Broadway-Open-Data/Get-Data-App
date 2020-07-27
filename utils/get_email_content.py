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


def get_email_content(emailName="Forgot Password", varDict={}):
    """
    Get the content for emails to be sent.
    Input a dictionary of values to be used mailmerge style
    """

    # get the credentials
    email_path = Path(f"app/emails/main_emails.json")
    if not os.path.isfile(email_path):
        return None

    # Continue
    with open(email_path, "r") as f:
        email_dict = json.load(f)

    # here's the emails you want
    my_email = email_dict.get(emailName)

    # Update the items in the email if necessary
    if len(varDict)>=1:
        for key, value in my_email.items():
            if key in ["emailSubject", "emailBody"]:
                # update the format if necessary
                value = value.format(**varDict)
                my_email.update({key:value})

    return my_email
