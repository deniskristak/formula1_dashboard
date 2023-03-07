from dash import dcc, html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

from bets_dash.dash_app.components.styles import style_env


def render(app: DjangoDash, player_bets, bet_was_registered) -> html.Div:
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
    for bet in player_bets:
        bet_rows.append(
            dbc.Row(
                [
                    html.H5(f"P{bet.position} {bet.driver.name}", style=style_env),
                ]
            )
        )
    return html.Div(
        children=[html.Hr(), html.H3("Player's bet"), html.Hr(), html.Div(bet_rows)]
    )
