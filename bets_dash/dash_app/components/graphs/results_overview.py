import pandas as pd
from dash import dcc
import plotly.express as px
from bets_dash.models import PlayerPoints
from bets_input.models import Race, RaceBet, Player

def playerpoints2df():
    players =  Player.objects.all()
    races = Race.objects.all()
    d = {player.nickname : 
            {race.name :PlayerPoints.objects.get(player=player, race=race).points
                for race in races}
                for player in players}
    return pd.DataFrame(d)

df = playerpoints2df()
fig = px.line(df.cumsum()) 
main_graph = dcc.Graph(figure=fig) 


