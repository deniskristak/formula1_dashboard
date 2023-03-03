from dash import dcc, html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

from bets_dash.dash_app.components.styles import style_env


def render(app: DjangoDash, selected_race_obj) -> html.Div:
    return html.Div(
        children=[
            dbc.Row(
                [
                    dbc.Col(html.H5(f"Circuit:", style=style_env)),
                    dbc.Col(html.H5(f"Date and time (UK timezone):", style=style_env)),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.H4(f"{selected_race_obj.name}", style=style_env)),
                    dbc.Col(html.H4(f"{selected_race_obj.datetime_of_race_gmt}", style=style_env)),
                ]
            ),
        ]
    )
