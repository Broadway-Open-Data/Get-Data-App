import os
from databases import db
from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph

def get_db_ERD(engine_name='broadway', save_path=None):
    engine = db.get_engine(bind=engine_name)
    metadata = MetaData(engine)


    graph = create_schema_graph(
        metadata=metadata,
        show_datatypes=True,
        show_indexes=True,
        rankdir='TB', # From left to right (instead of top to bottom)
        concentrate=True, # Don't try to join the relation lines together

        )
    # If no save path, set it...
    if not save_path:
        save_path = f'app/static/images/databases-ERD/{engine_name}.png'
    # Make the dir if you need to
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    graph.write_png(save_path)
