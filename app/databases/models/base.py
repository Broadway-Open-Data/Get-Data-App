import json
from databases import db


from sqlalchemy.exc import IntegrityError

class dbTable():
    """
    Base class for all objects in a table
    """
    # def __init__(self, **kwargs):
    #     self.__bind_key__=kwargs['bind_key']

    # Lookup by id
    @classmethod
    def get_by_id(self, id):
        """Get the id, name, description of a role based on the role name"""
        return self.query.filter_by(id=id).first()

    # Method to save role to DB
    def save_to_db(self, skip_errors=False, verbose=True):
        db.session.add(self)

        try:
            db.session.commit()

        except IntegrityError as err:
            db.session.rollback()
            if skip_errors:
                if verbose:
                    print(f"{err}")
            else:
                raise IntegrityError

    # Method to remove role from DB
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Udate info
    def update_info(self, **kwargs):
        # Track changes? --> DO THIS IN THE INHERETED INSTANCE
        # if kwargs.get('track_changes',False)==True:
        #     self.before_update(**kwargs)
        # Update info...
        self.query.filter_by(id=self.id).update(kwargs.get('update_dict'), synchronize_session=False)

        if kwargs.get('debug',False)==True:
            None
        else:
            self.save_to_db()




    # Define string methods...
    @classmethod
    def __data__(self):
        data = {x: getattr(self, x) for x in self.__dict__.keys() if not x.startswith('_')}
        # data = {x: getattr(self, x) for x in self.__mapper__.columns.keys()}
        return data

    @classmethod
    def __str__(self):
        data = self.__data__()
        return json.dumps(data, default=str)



    @classmethod
    def find_type(self, colname):
        if hasattr(self, '__table__') and colname in self.__table__.c:
            return self.__table__.c[colname].type
        for base in self.__bases__:
            return find_type(base, colname)
        raise NameError(colname)


















#
