from databases import db
from databases.models import dbTable
from databases.models import broadway as broadway_models

import datetime


def convert_to_tuple(value):
    """Helpful function"""
    # Single value
    if isinstance(value, (str,int)):
        return (value,)

    if isinstance(value, list):
        return tuple(value)

    if isinstance(value, tuple):
        return value




class BaseModel(dbTable):
    __table_args__ = {'schema':'broadway'}
    __bind_key__ = 'broadway'



    # Create highly specific function...
    def update_info_and_track(self, **kwargs):
        """Updates data and tracks edits"""

        self.track_change(**kwargs)

        if kwargs.get('test',False)==True:
            return
        if kwargs.get('track_changes_but_dont_update',False)==True:
            return
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
        #   --> using as_dict method because it's explicit, even though it's more "brutal"
        _data = self.as_dict()


        for key, value in kwargs.get('update_dict').items():

            # If no edit, then don't store
            if _data[key] == value:
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
                print(my_edit.as_dict())


            # Don't save edit when testing.
            if kwargs.get('test',False)==False:
                my_edit.save_to_db()



            # ======== Save edit values ========


            all_values_pre = convert_to_tuple(_data[key])
            all_values_post = convert_to_tuple(value)


            def add_edit_values(values, pre_or_post:int):
                """Add values, pre or post..."""
                for val in all_values_pre:
                    my_value = broadway_models.DataValues(value=val, pre_or_post=pre_or_post)
                    my_value.save_to_db()

                    # Now save
                    if pre_or_post==0:
                        my_edit.data_values_pre.append(my_value)
                    else:
                        my_edit.data_values_post.append(my_value)



            # Now save them!
            add_edit_values(all_values_pre, 0)
            add_edit_values(all_values_post, 1)

            my_edit.save_to_db()













#
