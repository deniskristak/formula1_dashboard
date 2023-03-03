from dash import dcc, html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

from bets_dash.dash_app.components.styles import style_env


def render(app: DjangoDash, player_points, player_nickname) -> html.Div:
    return html.Div(
        children=[
            html.H4(f"{player_nickname} obtained:"),
            html.H2(f"{player_points} points"),
            html.H4("for this race"),
            html.Hr(),
        ]
    )
