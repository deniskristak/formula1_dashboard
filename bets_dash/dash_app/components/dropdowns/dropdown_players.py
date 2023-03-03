from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash

from bets_dash.dash_app.components.styles import style_env
from bets_dash.dash_app.components import ids
from bets_input.models import Player
from .dropdown_helper import to_dropdown_options


def render(app: DjangoDash) -> html.Div:
    all_players = Player.objects.all()
    players_nicknames = [player.nickname for player in all_players]
    return html.Div(
        children=[
            html.H3("Who are you?"),
            dcc.Dropdown(
                id=ids.PLAYER_DROPDOWN,
                options=to_dropdown_options(players_nicknames),
                value=players_nicknames[0],
                style=style_env,
            )
        ],
    )
