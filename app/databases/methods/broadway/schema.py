from databases import db
import pandas as pd

def get_db_schema(format="html"):
    query = """
        SELECT
        	TABLE_NAME as 'Table',
            COLUMN_NAME as 'Field',
            COLUMN_TYPE as 'Type',
            IS_NULLABLE  as 'Null',
        	COLUMN_KEY as 'Key',
            COLUMN_DEFAULT as 'Default',
            EXTRA  as 'Extra'
        FROM information_schema.columns

        WHERE(
        	table_schema = 'broadway'
            AND
            TABLE_NAME not in ('alembic_version', 'data_edits')
            )
        ORDER BY TABLE_NAME, COLUMN_NAME;
        """

    df = pd.read_sql(query, db.get_engine(bind='broadway'))

    if format=="html":
        df.set_index(['Table','Field'],inplace=True, drop=True)
        return df.to_html(header="true", table_id="show-data")

    # Need to make this into a properly nested json
    if format=="dict":
        return df.groupby(by=['Table','Field'], sort=False).apply(lambda x: x.to_dict(orient='records'))
