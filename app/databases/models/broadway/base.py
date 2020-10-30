from databases import db
from databases.models import dbTable


class BaseModel(dbTable):
    __table_args__ = {'schema':'broadway'}
    __bind_key__ = 'broadway'
