from dash import dcc, html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc


def render(app: DjangoDash, event_in_future: bool) -> html.Div:
    # if the event didn't finish yet, we display a message
    if event_in_future:
        return html.Div(
            dbc.Row(
                children=[
                    dbc.Col(id="player-points-total"),
                    dbc.Col(
                        html.Div(
                            children=[
                                html.Hr(),
                                html.H3("Too soon for the results :-)"),
                                html.Hr(),
                            ]
                        ),
                    ),
                    dbc.Col(html.Hr()),
                    dbc.Col(id="player_bets"),
                ]
            )
        )
    # if the event is finished, we display the results
    return html.Div(
        dbc.Row(
            children=[
                dbc.Col(id="player-points-total"),
                dbc.Col(id="show-points"),
                dbc.Col(id="results"),
                dbc.Col(id="player_bets"),
            ]
        )
    )
