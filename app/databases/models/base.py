import json
import datetime
from databases import db, models


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
        # Track changes?
        if kwargs.get('track_changes',False)==True:
            self.before_update(**kwargs)
        # Update info...
        self.query.filter_by(id=self.id).update(kwargs.get('update_dict'), synchronize_session=False)

        if kwargs.get('debug',False)==True:
            None
        else:
            self.save_to_db()




    # Define string methods...
    @classmethod
    def __data__(self):
        data = {x: getattr(self, x) for x in self.__mapper__.columns.keys()}
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


    # Let's see if it works...
    # @staticmethod
    def before_update(self, **kwargs):

        # Consult this to get the column dtypes?
        # state = db.inspect(self)


        # Get edit meta info
        edit_date = datetime.datetime.utcnow()
        edit_id = db.session.query(models.broadway.DataEdits.edit_id).order_by(-models.broadway.DataEdits.edit_id.asc()).first()

        # Unpack the tuple to a result
        if edit_id:
            edit_id = edit_id[0] + 1
        else:
            edit_id = 1


        # Who made the edit ? – This will have to be built as a wrapper I guess...
        edit_by = kwargs.get('edit_by', '__obd_application__')
        edit_comment = kwargs.get('edit_comment', 'Automated edit made through the open broadway data backend interface.')
        approved =  kwargs.get('approved', True)
        approved_by = kwargs.get('approved_by', '__obd_application__')
        approved_comment = kwargs.get('approved_comment', 'Automated edit made through the open broadway data backend interface.')

        # Get reference stuff
        table_name = self.__tablename__

        # Get the data
        _data = self.__dict__

        for key, value in kwargs.get('update_dict').items():

            # If no edit, then don't store
            if _data[key] == value:
                # No edit
                print("no edit needed")
                continue

            my_edit = models.broadway.DataEdits(
                edit_date=edit_date,
                edit_id=edit_id,
                edit_by=edit_by,
                edit_comment=edit_comment,
                approved=approved,
                approved_by=approved_by,
                approved_comment=approved_comment,
                table_name=table_name,
                value_primary_id=self.id,
                field = key,
                field_type = str(self.find_type(key)),
                value_pre = _data[key],
                value_post = value
            )
            if kwargs.get('debug',False)==True:
                print(my_edit.__dict__)
            else:
                my_edit.save_to_db()












#
