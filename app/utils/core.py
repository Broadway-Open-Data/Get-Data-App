import os

def is_aws():
    my_user = os.environ.get("USER")
    return True if "ec2" in my_user else False
