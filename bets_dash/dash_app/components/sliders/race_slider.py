from dash import dcc, html
from django_plotly_dash import DjangoDash

from bets_dash.dash_app.components.styles import style_env
from bets_dash.dash_app.components import ids
from bets_input.models import Race


def render(app: DjangoDash) -> html.Div:
    races = Race.objects.all()
    races_marks_ids = []
    races_marks_names = []
    for race in races:
        races_marks_ids.append(race.country)
        races_marks_names.append(race.name)
    return html.Div(
        children=[
            html.H2("Weekends", style=style_env),
            dcc.Slider(
                id=ids.RACE_SLIDER,
                step=None,
                marks=races_marks_ids,
                value=0,
                tooltip=races_marks_names
            ),
        ],
    )
