import dash
from .layout import layout
from .callbacks import register_callbacks

def create_dashboard(server):
    app = dash.Dash(
        server=server,
        url_base_pathname='/explore/'
    )
    app.config['suppress_callback_exceptions'] = True
    app.title="Explore"

    # Set the layout
    app.layout = layout

    # Set the callbacks
    register_callbacks(app)
    
    return app
