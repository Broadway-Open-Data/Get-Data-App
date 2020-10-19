from sqlalchemy.ext.declarative import declarative_base
base = declarative_base()


from .changes import *
from .people import *
from .shows import *
from .theatres import *
