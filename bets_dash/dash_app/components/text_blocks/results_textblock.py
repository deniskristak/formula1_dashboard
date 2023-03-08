from dash import dcc, html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

from bets_dash.models import Results
from bets_dash.dash_app.components.styles import style_env


def render(app: DjangoDash, race, racetype) -> html.Div:
    result_rows = []
    if racetype == "quali":
        results = Results.objects.filter(race=race).order_by("position_quali")
    elif racetype == "sprint":
        results = Results.objects.filter(race=race).order_by("position_sprint")
    else:
        results = Results.objects.filter(race=race).order_by("position")

    for result in results:
        dnf = False
        fastest_lap = False
        dotd = False
        if racetype == "quali":
            position = result.position_quali
        elif racetype == "sprint":
            position = result.position_sprint
            dnf = result.dnf_sprint
        else:
            position = result.position
            dnf = result.dnf
            fastest_lap = result.fastest_lap
            dotd = result.dotd
        fastest_lap_string = f" (FL)" if fastest_lap is True else ""
        dotd_string = f" (DOTD)" if dotd is True else ""
        dnf_string = f" (DNF)" if dnf is True else ""
        result_rows.append(
            dbc.Row(
                [
                    html.H5(
                        f"P{position} {result.driver.name}{dnf_string}{fastest_lap_string}{dotd_string}",
                        style=style_env,
                    ),
                ]
            )
        )
    return html.Div(
        children=[html.Hr(), html.H3("Results"), html.Hr(), html.Div(result_rows)]
    )
