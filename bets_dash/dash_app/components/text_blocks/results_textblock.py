from dash import dcc, html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

from bets_dash.dash_app.components.styles import style_env


def render(app: DjangoDash, results) -> html.Div:
    result_rows = []
    for result in results:
        result_rows.append(
            dbc.Row(
                [
                    html.H5(
                        f"P{result.position} {result.driver.name}", style=style_env
                    ),
                ]
            )
        )
    return html.Div(
        children=[html.Hr(), html.H3("Results"), html.Hr(), html.Div(result_rows)]
    )
