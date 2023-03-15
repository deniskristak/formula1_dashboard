from collections import defaultdict

import pandas as pd
from dash import dcc, html
import plotly.express as px
from django_plotly_dash import DjangoDash

from bets_dash.dash_app.components import ids
from bets_dash.models import PlayerPoint
from bets_input.models import Race, RaceBet, Player
from bets_dash.dash_app.components.styles import style_env


def render(app: DjangoDash) -> html.Div:
    df = playerpoints_to_dataframe()
    fig = px.line(df.cumsum())

    return html.Div(
        children=[
            html.H3("Final results overview"),
            dcc.Graph(figure=fig, style=style_env, id=ids.RESULTS_OVERVIEW),
        ],
    )


def playerpoints_to_dataframe() -> pd.DataFrame:
    players = Player.objects.all()
    races = Race.objects.all()
    data = defaultdict(lambda: defaultdict(dict))
    for player in players:
        for race in races:
            player_points = PlayerPoint.objects.filter(player=player, race=race)
            if player_points.exists():
                data[player.nickname][race.name] = player_points.first().points_race
            else:
                data[player.nickname][race.name] = 0

    return pd.DataFrame(data)
