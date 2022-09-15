import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

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

layout = dbc.Navbar(
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
