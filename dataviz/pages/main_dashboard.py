from dash import html
import dash_bootstrap_components as dbc
import dash_draggable
from dataviz.irenderer import IDataStudyRenderer
from dataviz.pages.add_plot_modal import modal_add_plot


def drag_canvas(renderer: IDataStudyRenderer):
    return [
        html.H1(renderer.app.title),
        html.Div(
            children=[
                html.P(renderer.desc),
                dbc.Button(
                    "download", id="download",
                    style={"display": "inline-block"},
                    className="ml-auto"
                ),
                dbc.Button(
                    "add plot", id="add_plot",
                    style={"display": "inline-block"},
                    className="ml-auto"
                ),
            ]
        ),

        html.Hr(),
        dash_draggable.GridLayout(
            className="draggable",
            id='draggable',
            children=list(renderer.plots.values()),
        ),
        html.Hr(),
        modal_add_plot
    ]
