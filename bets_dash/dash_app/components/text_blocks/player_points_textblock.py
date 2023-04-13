from dash import dcc, html
from django_plotly_dash import DjangoDash


def render(app: DjangoDash, player_points: int, player_nickname: str) -> html.Div:
    return html.Div(
        children=[
            html.Hr(),
            html.H3(f"{player_nickname} obtained:"),
            html.Hr(),
            html.H2(f"{player_points} points"),
            html.H4("for this event"),
        ]
    )
