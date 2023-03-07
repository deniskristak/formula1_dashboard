import pandas as pd
from dash import dcc, html
import plotly.express as px
from django_plotly_dash import DjangoDash

from bets_dash.dash_app.components import ids
from bets_dash.models import PlayerPoints
from bets_input.models import Race, RaceBet, Player
from bets_dash.dash_app.components.styles import style_env


def render(app: DjangoDash) -> html.Div:
    df = playerpoints2df()
    fig = px.line(df.cumsum())

    return html.Div(
        children=[
            html.H3("Results overview"),
            dcc.Graph(figure=fig, style=style_env, id=ids.RESULTS_OVERVIEW),
        ],
    )


def playerpoints2df():
    players = Player.objects.all()
    races = Race.objects.all()
    d = {
        player.nickname: {
            race.name: PlayerPoints.objects.get(player=player, race=race).points_race
            for race in races
        }
        for player in players
    }
    return pd.DataFrame(d)
