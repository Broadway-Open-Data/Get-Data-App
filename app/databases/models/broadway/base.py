from databases import db
from databases.models import dbTable
from databases.models import broadway as broadway_models

import datetime



class BaseModel(dbTable):
    __table_args__ = {'schema':'broadway'}
    __bind_key__ = 'broadway'



    # Create highly specific function...
    def update_info_and_track(self, **kwargs):
        """Updates data and tracks edits"""

        self.track_change(**kwargs)
        self.update_info(**kwargs)



    # This works! Store values here...
    def track_change(self, **kwargs):

        # Get edit meta info
        edit_date = datetime.datetime.utcnow()
        user_edit_id = db.session.query(broadway_models.DataEdits.user_edit_id).order_by(-broadway_models.DataEdits.user_edit_id.asc()).first()

        # Unpack the tuple to a result
        if user_edit_id: user_edit_id = user_edit_id[0] + 1
        else: user_edit_id = 1


        # Who made the edit ? – This will have to be built as a wrapper I guess...
        edit_by = kwargs.get('edit_by', '__obd_application__')
        edit_comment = kwargs.get('edit_comment', 'Automated edit made through the open broadway data backend interface.')
        approved =  kwargs.get('approved', True)
        approved_by = kwargs.get('approved_by', '__obd_application__')
        approved_comment = kwargs.get('approved_comment', 'Automated edit made through the open broadway data backend interface.')


        # Get reference stuff
        table_name = self.__tablename__

        # Get the data
        _data = {x: getattr(self, x) for x in self.__dict__.keys() if not x.startswith('_')}
        # _data = self.__data__()

        for key, value in kwargs.get('update_dict').items():

            # If no edit, then don't store
            if _data[key] == value:
                # No edit
                if kwargs.get('debug',False)==True:
                    print("no edit needed")
                continue

            my_edit = broadway_models.DataEdits(
                edit_date=edit_date,
                user_edit_id=user_edit_id,
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
