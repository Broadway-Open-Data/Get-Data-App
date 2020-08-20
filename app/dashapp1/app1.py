import dash
import dash_html_components as html
from flask import Flask


def create_dashboard(server):
    app = dash.Dash(
        server=server,
        url_base_pathname='/explore/'
    )
    app.config['suppress_callback_exceptions'] = True
    app.title="Explore"
    app.layout = html.Div("This will be an explore feature. Coming soon!")

    return app
