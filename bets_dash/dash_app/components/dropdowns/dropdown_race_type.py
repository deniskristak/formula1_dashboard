from dash import dcc, html
from django_plotly_dash import DjangoDash

from bets_dash.dash_app.components.styles import style_env
from bets_dash.dash_app.components import ids


def render(app: DjangoDash, race_types) -> html.Div:
    return html.Div(
        children=[
            html.H3("Quali / Race?"),
            dcc.Dropdown(
                id=ids.RACETYPE_DROPDOWN,
                options=race_types,
                value=race_types[1]["value"],
                style=style_env,
            ),
        ],
    )
