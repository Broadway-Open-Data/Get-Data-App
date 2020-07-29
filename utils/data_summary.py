"""
Things we want to improve:

On the first "count" row, a lot of the data seems to be not useful or accurate - I think that show count, number of performances (seems to be inaccurate in "count" row), limited_run (also confused at this value in the "count" row), and maybe intermissions is helpful info, but the rest seems unnecessary and kind of muddies up the chart
I think it would be interesting to have a summary section listing how many plays vs. musicals vs. other there were and how many originals vs. revivals there were
I like the chart structure overall but would likely recommend blanking out the unnecessary info
Is there any significance to the show or theatre IDs?
The info in the "show_never_opened" column is pretty difficult to understand since such a small number of shows didn't open - I think just listing how many shows didn't open (under given specifications) would be a better way to look at that data


What we definitely want:
– N shows
– Date range
– N Years

– N plays
– N Musicals
– N Originals
– N Revivals
– N Unique Theaters
– Avg intermissions

"""

import pandas as pd
import numpy as np
def diff(s):
    """Gets the diff for a pd series"""
    return s.max() - s.min()

def diff_days(s):
    """Gets the datediff for a pd series"""
    return (s.max() - s.min()).days


def summarize_broadway_shows(df):
    """
    Input a df of the data you want summarized
    """

    my_vals = []
    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    cat = "Date Range Info"
    if "title" in df.columns:
        my_vals.extend([
            {"Category":cat, "Key": "N Shows", "Val":df["title"].count()}
        ])

    if "opening_date" in df.columns:
        my_vals.extend([
            {"Category":cat, "Key":"Days in Range", "Val":df["opening_date"].count()},
            {"Category":cat, "Key":"Earliest Date", "Val":df["opening_date"].min().strftime("%Y-%m-%d")},
            {"Category":cat, "Key":"Latest Date", "Val":df["opening_date"].max().strftime("%Y-%m-%d")},
        ])
    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    cat = "Show Info"
    if "theatre_name" in df.columns:
        my_vals.append(
            {"Category":cat, "Key":"N Unique Theaters", "Val":df["theatre_name"].nunique()}
        )

    if "intermissions" in df.columns:
        my_vals.extend([
            {"Category":cat, "Key":"Avg intermissions", "Val":df["intermissions"].mean().round(2)},
            {"Category":cat, "Key":"N No intermissions", "Val":(df["intermissions"]==0).sum()}
        ])

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    cat = "Production Info"
    iter_cols = ["show_type_simple","production_type"]
    for col in iter_cols:
        for idx, n in df[col].value_counts().sort_index(ascending=True).items():
            my_vals.append(
                {"Category":cat, "Key":f"N {idx}s", "Val": n}
            )

    # ---------------------------------------------------------------------------

    summary_df = pd.DataFrame.from_records(my_vals)

    # Set the index
    summary_df.set_index(["Category","Key"],inplace=True)
    # Remove the index names
    summary_df.rename_axis([None, None], inplace=True)
    # create the html table
    summary = summary_df.to_html(header=False, table_id="summary-table")

    return summary
