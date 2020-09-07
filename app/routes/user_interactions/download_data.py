from flask import Response, request, jsonify
from flask_login import login_required

import pandas as pd

# flasks stuff
from common.extensions import cache


# ------------------------------------------------------------------------------

from . import page


@page.route('/download-data/<file_format>')
@login_required
def download_data(file_format):
    """Download the data to the user..."""

    # Retrieve the data from  user's request
    data = cache.get("my_data")

    if not data:
        return jsonify({
            "ERROR": "data not found."
        })

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    df = pd.DataFrame.from_records(data)

    if file_format == "csv":
        data_out = df.to_csv(index=False, encoding='utf-8')
    elif file_format == "json":
        data_out = df.to_json(orient='records')

    # Send the data out
    now = datetime.datetime.today().strftime("%Y-%m-%d")

    response = Response(
        data_out,
        mimetype=f"text/{file_format}",
        headers={"Content-Disposition": f"attachment; filename=open-broadway-data {now}.{file_format}"})

    return response
