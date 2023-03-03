from dash.dependencies import Input, Output
from dash import Dash, html, ClientsideFunction, State
from src.components.styles import style_env, style_all_drivers
from dash_extensions import EventListener
import dash_bootstrap_components as dbc

from src.data.sources import DriversDataSource, RaceBetsDataSource
import src.components.ids as ids


def render(app: Dash, race_bets_data_source: RaceBetsDataSource, drivers_data_source: DriversDataSource) -> html.Div:

    app.config.external_scripts = ["https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"]

    event = {"event": "dropcomplete", "props": ["detail.name"]}


    drivers_ids_order_from_db = race_bets_data_source.current_order_of_drivers(player_id=1, race_id=0)
    drivers_names = []
    for driver_id in drivers_ids_order_from_db:
        drivers_names.append(drivers_data_source.driver_name_by_id(driver_id))
    drivers_buttons_list = []
    # TODO: make it so that there are numbers that stay the same, only names will move
    for driver_name in drivers_names:
        drivers_buttons_list.append(
            dbc.Button(
                id=f"{driver_name}",
                children=f"{driver_name}",
                color="secondary",
            )
        )

    return html.Div(
        id="main",
        children=[
            dbc.Row(html.H2("Expected results")),
            html.Label(id=ids.CURRENT_ORDER_OF_DRIVERS, hidden=True),
            EventListener(
                html.Div(
                    id=ids.DRAG_CONTAINER_DRIVERS,
                    children=drivers_buttons_list,
                    style=style_all_drivers
                ),
                events=[event], logging=True, id="el"),
        ],
        style=style_env
    )
