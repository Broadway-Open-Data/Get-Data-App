
# This is the currently existing method...
def select_data_from_simple(my_params={}, theatre_data=True):
    """
    Input a dictionary statement in dict format.
    Returns records from db.
    """



    # Must have a start and end year
    if "startYear" not in my_params.keys():
        my_params.update({"startYear":1900})

    if "endYear" not in my_params.keys():
        my_params.update({"endYear":2020})

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Reorganize your query

    query_structure = {
        "lists":{
            "show_type_simple":{
                "musicals":"Musical",
                "plays":"Play",
                "other_show_genre":["Opera","Burleque","Revue","Other","Concert","Special","Unknown",None]
            },
            "production_type":{
                "originals":"Original Production",
                "revivals":"Revival",
                "other_production_type":[
                    "Concert","Premiere", "Revised Production", "Concert Revival","Production", "Motion Picture", None]
                }
            },
        "bool":{

        }
    }

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    query_dict = {}

    # Which values do you want returned for each key?
    for key, value in query_structure["lists"].items():

        # Update to flat values
        flat_vals = flatten_to_string(
            [v for k,v in value.items() if my_params.get(k,True)]
            )
        query_dict.update({key:flat_vals})

    # --------------------------------------------------------------------------

    # Build the select statement

    select_st = select([Show]).\
        where(Show.year >= my_params["startYear"]).\
        where(Show.year <= my_params["endYear"]).\
        where(Show.show_type_simple.in_(query_dict["show_type_simple"])).\
        where(Show.production_type.in_(query_dict["production_type"]))

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # If theatre info is requested
    if my_params.get("theatre_info"):

        join_obj = shows.join(Theatre, Show.theatre_id == Theatre.id, isouter=True)

        # Update the select statement
        select_st =  select_st.column(Theatre).select_from(join_obj)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Load to a pandas dataframe
    df = pd.read_sql(select_st, db.get_engine(bind='broadway'))
    return df
