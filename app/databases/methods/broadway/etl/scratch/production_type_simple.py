import sys
import os
import json
import sys
import datetime
import uuid


# Correct the path
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, '/Users/yaakov/Documents/Broadway-Open-Data/MVP-FrontEnd/app')

# Internal stuff
from databases.create_db import db
from databases.models.broadway import Person, DataEdits, RacialIdentity, GenderIdentity
from databases.methods.broadway import update_person_identities
from utils.get_db_uri import get_db_uri


# Flask Stuff
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# sqlalchemy stuff
from sqlalchemy import create_engine, Column, func, and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Data stuff
# import pandas as pd



# # Define args
# import argparse
#
# parser = argparse.ArgumentParser(description='describe the name of the operation you want to do -- using the function name / class method.')
# parser.add_argument('function_name', nargs='*', help='name of the class method you want to run')
DB_URI = get_db_uri("broadway")


engine = create_engine(DB_URI)
Base = declarative_base(engine)

class Show(Base):
    __tablename__ = 'shows'
    __table_args__ = {'autoload':True}



Session = sessionmaker(bind=engine)
session = Session()



all_shows = session.query(Show).all()
    # .filter(
    #     Show.production_type_simple.is_(None)
    # )\
    # .all()

production_type_mapper = {
    'Original Production':'Original',
    'Premiere':'Original',
    'Production':'Original',
    'Revised Production':'Revival',
    'Revival':'Revival'

}
for i, show in enumerate(all_shows):

    if i%50==0:
        print(f'Beginning {i:,} of {len(all_shows):,}')

    if i%1_000==0:
        session.commit()
        
    # Pass on empties
    if not show.production_type:
        continue

    #Update your values...
    show.production_type_simple = production_type_mapper.get(show.production_type,'Other')

# That's it...
session.commit()




# ------------------------------------------------------------------------------









#
