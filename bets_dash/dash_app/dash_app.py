from dash import Output, Input, State, html, ClientsideFunction
from dash_bootstrap_components.themes import BOOTSTRAP
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc

from bets_input.models import Race, RaceBet, Player, PlayerPlacedBet
from bets_dash.models import Results, PlayerPoints, PlayerPointsTotal
from .components import ids
from .components.sliders import race_slider
from .components.dropdowns import dropdown_players, dropdown_helper, dropdown_race_type
from .components.text_blocks import (
    race_type_textblock,
    results_textblock,
    player_bets_textblock,
    player_points_textblock,
    player_points_total_textblock,
)
from .components.graphs import results_overview
from .components.styles import style_env

app = DjangoDash("MainDashApp", external_stylesheets=[BOOTSTRAP])
app.title = "F1 2022 - Result Dashboard"

app.layout = html.Div(
    className="app-div",
    children=[
        html.Hr(),
        html.Div(
            children=[
                race_slider.render(app=app),
            ],
        ),
        html.Hr(),
        # # this is rendered by race_slider's callback function
        html.Div(id="race-details"),
        html.Hr(),
        html.Div(
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dropdown_players.render(app=app),
                        ],
                    ),
                    # placeholder column
                    dbc.Col(""),
                    # placeholder column
                    dbc.Col(id="race-types"),
                    # placeholder column
                    dbc.Col(""),
                ]
            )
        ),
        html.Hr(),
        html.Div(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(id="player-points-total"),
                        dbc.Col(id="show-points"),
                        dbc.Col(id="results"),
                        dbc.Col(id="player_bets"),
                    ]
                )
            ]
        ),
        html.Hr(),
        html.Div(results_overview.render(app=app)),
        html.Hr(),
    ],
    style=style_env,
)


@app.callback(
    Output("race-details", component_property="children"),
    Input(ids.RACE_SLIDER, component_property="value"),
)
def selected_race_textblock(selected_race_index):
    # selections in dash index from 0
    race_id = selected_race_index + 1
    selected_race_obj = Race.objects.get(id=race_id)
    return race_type_textblock.render(app=app, selected_race_obj=selected_race_obj)


@app.callback(
    Output("race-types", component_property="children"),
    Input(ids.RACE_SLIDER, component_property="value"),
)
def race_types(selected_race_index):
    # selections in dash index from 0
    race_id = selected_race_index + 1
    selected_race_obj = Race.objects.get(id=race_id)
    race_types = [
        {"label": "Qualification", "value": "quali"},
        {"label": "Race", "value": "race"},
    ]
    if selected_race_obj.is_sprint:
        race_types.append({"label": "Sprint", "value": "sprint"})

    return [dropdown_race_type.render(app=app, race_types=race_types)]


# todo following 3 methods should apply for sprint and quali
# for that, we need to think about a suitable layout
# and also we need to assess each race event (quali/sprint/race) separately
# todo we also have new table - palyerplacedbet - which we can use when calculating points
@app.callback(
    Output("player_bets", component_property="children"),
    Input(ids.RACE_SLIDER, component_property="value"),
    Input(ids.RACETYPE_DROPDOWN, component_property="value"),
)
def results(selected_race_index, racetype):
    # selections in dash index from 0
    race_id = selected_race_index + 1
    selected_race_obj = Race.objects.get(id=race_id)
    results = Results.objects.filter(race=selected_race_obj)

    return results_textblock.render(app=app, results=results)


@app.callback(
    Output("results", component_property="children"),
    Input(ids.RACE_SLIDER, component_property="value"),
    Input(ids.RACETYPE_DROPDOWN, component_property="value"),
    Input(ids.PLAYER_DROPDOWN, component_property="value"),
)
def player_bets(selected_race_index, racetype, player):
    # selections in dash index from 0
    race_id = selected_race_index + 1
    selected_race_obj = Race.objects.get(id=race_id)
    selected_player_obj = Player.objects.get(nickname=player)
    player_bets = RaceBet.objects.filter(
        race=selected_race_obj, player=selected_player_obj
    )
    bet_was_registered = (
        False
        if PlayerPlacedBet.objects.filter(
            race=selected_race_obj, player=selected_player_obj, race_type=racetype
        ).count()
        == 0
        else True
    )

    return player_bets_textblock.render(
        app=app, player_bets=player_bets, bet_was_registered=bet_was_registered
    )


@app.callback(
    Output("show-points", component_property="children"),
    Input(ids.RACE_SLIDER, component_property="value"),
    Input(ids.RACETYPE_DROPDOWN, component_property="value"),
    Input(ids.PLAYER_DROPDOWN, component_property="value"),
)
def player_points(selected_race_index, racetype, player):
    # selections in dash index from 0
    race_id = selected_race_index + 1
    selected_race_obj = Race.objects.get(id=race_id)

    player_points_obj = PlayerPoints.objects.get(
        race=selected_race_obj, player=Player.objects.get(nickname=player)
    )

    if racetype == "quali":
        player_points = player_points_obj.points_quali
    elif racetype == "sprint":
        player_points = player_points_obj.points_sprint
    else:
        player_points = player_points_obj.points_race

    return player_points_textblock.render(
        app=app, player_points=player_points, player_nickname=player
    )


@app.callback(
    Output("player-points-total", component_property="children"),
    Input(ids.PLAYER_DROPDOWN, component_property="value"),
)
def player_points_total(player):
    # selections in dash index from 0
    selected_player_obj = Player.objects.get(nickname=player)
    player_points = PlayerPointsTotal.objects.get(
        player=selected_player_obj
    ).points_total

    return player_points_total_textblock.render(
        app=app, player_points=player_points, player_nickname=player
    )
