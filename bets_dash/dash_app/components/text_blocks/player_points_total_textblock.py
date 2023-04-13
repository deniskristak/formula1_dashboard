from dash import dcc, html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

from bets_dash.dash_app.components.styles import style_env


def render(app: DjangoDash, player_points: int, player_nickname: str) -> html.Div:
    return html.Div(
        children=[
            html.Hr(),
            html.H3(f"Total points ({player_nickname}):"),
            html.Hr(),
            html.H2(f"{player_points}"),
        ]
    )
