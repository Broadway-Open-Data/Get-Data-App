import os

def is_aws():
    if os.environ.get("AWS_OVERRIDE"):
        return False
    my_user = os.environ.get("USER")
    return True if "ec2" in my_user else False
