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
from databases.models.broadway import Theatre
from utils.get_db_uri import get_db_uri


# sqlalchemy stuff
from sqlalchemy import create_engine, Column, func, and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# Data stuff
import pandas as pd
import re
theatre_data_path = '/Users/yaakov/Documents/Open Broadway Data (All)/DB Backups/theatre_id_and_name.csv'
df = pd.read_csv(theatre_data_path, index_col='id')
df['theatre_name'] = df['theatre_name'].astype(str).str.replace('\u2018','')

theatre_name_mapper = df['theatre_name'].to_dict()


DB_URI = get_db_uri("broadway")


engine = create_engine(DB_URI)
Base = declarative_base(engine)

class Theatre(Base):
    __tablename__ = 'theatres'
    __table_args__ = {'autoload':True}

Session = sessionmaker(bind=engine)
session = Session()



all_theatres = session.query(Theatre).all()


for i, theatre in enumerate(all_theatres):

    if i%50==0:
        print(f'Beginning {i:,} of {len(all_theatres):,}')
        session.commit()

    if i%1_000==0:
        session.commit()

    #Update your values...
    if theatre_name_mapper[theatre.id]:
        theatre.name = theatre_name_mapper[theatre.id]


# That's it...
session.commit()




# ------------------------------------------------------------------------------









#
