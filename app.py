import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_auth
import pandas as pd
import datetime

from pages import explore, relationships, home, experiment

from dash.dependencies import Input, Output

from users import USERNAME_PASSWORD_PAIRS

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SANDSTONE,
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    }],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

auth = dash_auth.BasicAuth(
    app,
    USERNAME_PASSWORD_PAIRS
)

server = app.server

app.config.suppress_callback_exceptions = True

app.title = "Uncountable Dashboard (Take Home Assignment)"

# df read json from data.json


navBar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                 html.Img(
                    src=app.get_asset_url("logo.png"),
                    height="30px",

                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.Row(
                [
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Collapse(
                        dbc.Nav(
                            [
                                dbc.NavItem(dbc.NavLink("Explore Data by Time", href="/explore")),
                                dbc.NavItem(dbc.NavLink("Explore Relationships", href="/relationships")),
                                dbc.NavItem(
                                    dbc.NavLink("Explore Data by Experiment Number", href="/experiment"),
                                    className="me-auto",
                                ),
                            ],
                            # make sure nav takes up the full width for auto
                            # margin to get applied
                            className="w-100",
                        ),
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                    ),
                ],
                # the row should expand to fill the available horizontal space
                className="flex-grow-1",
            ),
        ],
        fluid=True,
    ),
    dark=True,
    color="grey",
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navBar,
    html.Div(id='page-content', children=[]), 
    ]
)

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/explore':
        return explore.layout
    elif pathname == '/relationships':
        return relationships.layout
    elif pathname == '/experiment':
        return experiment.layout
    else:
        return home.layout

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)