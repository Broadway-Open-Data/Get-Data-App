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


def summarize_broadway_shows(df, detail_level=3):
    """
    Input a df of the data you want summarized

    Detail level is 1,2 or 3 --> higher number is higher level of detail.
    """

    my_vals = []
    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    cat = "Date Range Info"
    for COL in ['title', 'Show Title']:
        if "title" in df.columns:
            my_vals.extend([
                {"Category":cat, "Key": "N Shows", "Val":df[COL].count()}
            ])

    for COL in ['opening_date', 'Opening Data']:
        if COL in df.columns:
            my_vals.append(
                {"Category":cat, "Key":"Days in Range", "Val":df[COL].count()},
                )
            if detail_level>1:
                my_vals.extend([
                {"Category":cat, "Key":"Earliest Date", "Val":df[COL].min().strftime("%Y-%m-%d")},
                {"Category":cat, "Key":"Latest Date", "Val":df[COL].max().strftime("%Y-%m-%d")},
            ])

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    cat = "Show Info"
    for COL in ['theatre_name', 'Theatre Name']:
        if COL in df.columns:
            my_vals.append(
                {"Category":cat, "Key":"N Unique Theaters", "Val":df[COL].nunique()}
            )

    # User chooses the level of detail

    for col in ["n_performances", "N Performances", "intermissions", "Intermissions"]:
        continue
        # Only proceed if relevant
        if col not in df.columns or detail_level<2:
            continue

        # Otherwise
        col_clean = col.replace("n_","").title()

        col_vals = [
            {"Category":col_clean, "Key":f"Median {col_clean}", "Val":df[col].median().round(2)},
            {"Category":col_clean, "Key":f"Max {col_clean}", "Val":df[col].max()},
        ]

        # Add in a specific order
        if detail_level>2:
            col_vals.insert(0,
                {"Category":col_clean, "Key":f"Avg {col_clean}", "Val":df[col].mean().round(2)})

            col_vals.append(
                {"Category":col_clean, "Key":f"N {col_clean} is NA", "Val":(df[col].isna()).sum()}
            )
            # Only include if there are 0's
            if (df[col]==0).sum() >0:
                col_vals.insert(-2,
                    {"Category":col_clean, "Key":f"N {col_clean} eq. 0", "Val":(df[col]==0).sum()},
                )

        # add to the list
        my_vals.extend(col_vals)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    iter_cols = ["show_type_simple", "Show Type (Simple)", "production_type", "Production Type"]
    for col in iter_cols:

        if col not in df.columns:
            continue

        # modify col for category
        cat = col.replace("simple","(simple)").replace("_"," ").title()

        # Only get the top 4
        val_counts = df[col].value_counts()
        if len(val_counts)>3:
            val_counts = val_counts[:3]
        # Sort alphabetically
        val_counts = val_counts.sort_index(ascending=True)

        for idx, n in val_counts.items():
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
