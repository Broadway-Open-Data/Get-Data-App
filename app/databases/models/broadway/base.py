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

        if kwargs.get('test',False)==False:
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
            # if kwargs.get('test',False)==False:
            #     my_edit.save_to_db()

            # Sample here, add values pre and post to corresponding link tables...
            # Start where the values are a string:
            # CONTINUE FROM HERE --> ON EDIT, ADD "PRE" AND "POST" VALUES TO LINK TABLE
            # THEN REMOVE PRE AND POST AS FIELDS FROM DATAEDITS....

            # ======== PRE ========
            # Single value
            if isinstance(_data[key], (str,int)):

                # Hopefully this is it...
                # Though, I'll need to make sure the value has "pre" or "post" in it...
                # my_edit.data_values_pre.append(_data[key])
                print(my_edit)
                # my_value = broadway_models.DataValues(
                #     value=_data[key]
                #     )
                # my_value.save_to_db()
                #
                # my_value_link = broadway_models.DataEditsValuesLink(
                #     data_edits_id=my_edit.id, # primary key for DataEdits
                #     value_id=my_value.id, # primary key for DataValues
                #     pre_or_post=0,
                # )
                # my_value_link.save_to_db()
                # print("Value link: ", my_value_link)



            # Multiple values
            if isinstance(_data[key], (tuple,list)):
                # Do something...
                print(_data[key])







            # ======== POST ========

            # if type(value)==list:
            #     for v in value:
            #         # Add each value
            #         None
            # else:
            #     # Add the value...
            #     None





















#
