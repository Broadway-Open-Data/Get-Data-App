"""
Generate a pretty (and simple) table with a summary of the data
"""
import pandas as pd


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
        # Only get the top 4
        val_counts = df[col].value_counts()
        if len(val_counts)>4:
            val_counts = val_counts[:4]
        # Sort alphabetically
        val_counts = val_counts.sort_index(ascending=True)

        for idx, n in .items():
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
