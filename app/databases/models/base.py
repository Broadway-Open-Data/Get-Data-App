import json
from databases import db
from sqlalchemy.orm import class_mapper, ColumnProperty


from sqlalchemy.exc import IntegrityError

class dbTable():
    """
    Base class for all objects in a table
    """

    # Lookup by id
    @classmethod
    def get_by_id(self, id):
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
        """
        Updates data.

        Note: for tracking edits, a custom function must be defined. Our approach
        is to create such a function in the child / inhereted class, so that
        edits are stored in the specific database in which they belong.
        """

        # Update info...
        self.query.filter_by(id=self.id).update(kwargs.get('update_dict'), synchronize_session=False)

        # don't save edits when testing
        if kwargs.get('test',False)==False:
            self.save_to_db()



    # --------------------------------------------------------------------------

    def __str__(self):
        """Should this be a class method?"""
        data = self.as_dict()
        return json.dumps(data, default=str)



    def as_dict(self):
        """This method calls all data directly related to `self`, relationships are ignored..."""
        result = {}
        for prop in class_mapper(self.__class__).iterate_properties:
            if isinstance(prop, ColumnProperty):
                result[prop.key] = getattr(self, prop.key)
        return result


    # Define string methods...
    def __data__(self):
        """
        This method calls all data related to `self`, including mapped relationships...
        Note: Don't make this a class method...
        """
        data = {x: getattr(self, x) for x in self.__dict__.keys() if not x.startswith('_')}
        return data



    # --------------------------------------------------------------------------

    @classmethod
    def find_type(self, colname):
        if hasattr(self, '__table__') and colname in self.__table__.c:
            return self.__table__.c[colname].type
        # for base in self.__bases__:
        #     return find_type(base, colname)
        raise NameError(colname)


















#
