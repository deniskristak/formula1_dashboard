from dash import Dash, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from bets_dash.dash_app.components import ids

def render(app: Dash) -> html.Div:

    return html.Div(
        children=[
            dbc.Button(
                id=ids.SAVE_TO_DB_BUTTON,
                color='secondary',
                children=[
                    html.H1(
                        children="Save choices to database",
                    )
                ]
            ),
            html.Label(
                id='placeholder-output-div',
                hidden=True,
            ),
            html.Label(
                id='placeholder-output-div2',
                hidden=True,
            ),
        ]
    )
