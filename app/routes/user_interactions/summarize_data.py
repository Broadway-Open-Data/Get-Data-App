from flask import Response, request, render_template
from flask_login import login_required

import pandas as pd
import common
import utils

from . import page

# ------------------------------------------------------------------------------

@page.route('/summarize-data')
@login_required
def summarize_data():

    detail_level = int(request.args.get('detail_level'))

    data = common.cache.get("my_data")
    df = pd.DataFrame.from_dict(data)

    print(df)
    summary = utils.summarize_broadway_shows(df, detail_level)

    # Return the response in json format
    return summary
