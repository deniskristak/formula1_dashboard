from dash import dcc, html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from bets_input.models import RaceBet, Race, Player
from bets_dash.dash_app.components.styles import style_env


def render(app: DjangoDash, race: Race, player: Player, bet_was_registered: bool, racetype: str) -> html.Div:
    if not bet_was_registered:
        return html.Div(
            children=[
                html.Hr(),
                html.H3("Player's bet"),
                html.Hr(),
                html.H4("This player didn't make a bet."),
            ],
        )
    bet_rows = []
    if racetype == "quali":
        player_bets = RaceBet.objects.filter(race=race, player=player).order_by("position_quali")
    elif racetype == "sprint":
        player_bets = RaceBet.objects.filter(race=race, player=player).order_by("position_sprint")
    else:
        player_bets = RaceBet.objects.filter(race=race, player=player).order_by("position")

    for bet in player_bets:
        if racetype == "quali":
            position = bet.position_quali
        elif racetype == "sprint":
            position = bet.position_sprint
        else:
            position = bet.position
        bet_rows.append(
            dbc.Row(
                [
                    html.H5(f"P{position} {bet.driver.name}", className=bet.driver.team.lc_name),
                ]
            )
        )
    return html.Div(children=[html.Hr(), html.H3("Player's bet"), html.Hr(), html.Div(bet_rows)])
