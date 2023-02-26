import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from django_plotly_dash import DjangoDash
from tips_dash.models import RaceTip

app = DjangoDash('MainDashApp')

race_tips = RaceTip.objects.all()
tip_labels = []
for tip in race_tips:
    tip_labels.append(
        html.Div(
            dbc.Label(str(tip.race))
        )
    )

print(tip_labels)

app.layout = html.Div(
    # tip_labels
    [
    dcc.RadioItems(
        id='dropdown-color',
        options=[{'label': c, 'value': c.lower()} for c in ['Red', 'Green', 'Blue']],
        value='red'
    ),
    html.Div(id='output-color'),
    dcc.RadioItems(
        id='dropdown-size',
        options=[{'label': i, 'value': j} for i, j in [('L','large'), ('M','medium'), ('S','small')]],
        value='medium'
    ),
    html.Div(id='output-size')
    ]
)


@app.callback(
    dash.dependencies.Output('output-color', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value')])
def callback_color(dropdown_value):
    return "The selected color is %s." % dropdown_value

@app.callback(
    dash.dependencies.Output('output-size', 'children'),
    [dash.dependencies.Input('dropdown-color', 'value'),
     dash.dependencies.Input('dropdown-size', 'value')])
def callback_size(dropdown_color, dropdown_size):
    return "The chosen T-shirt is a %s %s one." %(dropdown_size,
                                                  dropdown_color)
