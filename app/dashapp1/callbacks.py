from datetime import datetime as dt

import pandas as pd
from dash.dependencies import Input
from dash.dependencies import Output


def register_callbacks(dashapp):
    @dashapp.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):
        df = pd.DataFrame.from_records([
            {"name":"COKE", "value":10},
            {"name":"TSLA", "value":15},
            {"name":"AAPL", "value":20},
            ])
        return {
            'data': [{
                'x': df["name"],
                'y': df["value"]
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }
