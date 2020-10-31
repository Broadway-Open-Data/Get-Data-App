from databases.models import dbTable


class BaseModel(dbTable):
    __table_args__ = {'schema':'users'}
    __bind_key__ = 'users'
