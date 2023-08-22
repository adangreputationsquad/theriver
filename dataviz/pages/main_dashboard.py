from dash import html, Output, Input, State, ALL
import dash_bootstrap_components as dbc
import dash_draggable
from dataviz.irenderer import IDataStudyRenderer
from dataviz.pages.add_plot_modal import modal_add_plot
from dataviz.plot_types import name_to_plot


def drag_canvas(renderer: IDataStudyRenderer):
    out = [
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
        modal_add_plot(renderer)
    ]

    @renderer.app.callback(
        [Output("draggable", "children"),
         Output("select_plot_dropdown", "value"),
         Output("select_view_dropdown", "value")],
        [Input("validate_add_plot", "n_clicks"),
         Input({"type": "close_plot", "index": ALL}, "id"),
         Input({"type": "close_plot", "index": ALL}, "n_clicks"),
         State({"type": "add_plot_arg", "index": ALL}, "value"),
         State("select_plot_dropdown", "value"),
         State("select_view_dropdown", "value"),
         ]
    )
    def update_plot_canvas(_, plot_ids, plot_close_buttons,
                           values, selected_plot, selected_view):
        # Case where we add a plot
        if selected_plot is not None:
            selected_view = renderer.study.views.get(selected_view)
            next_id = renderer.next_id()
            selected_plot = name_to_plot(selected_plot)
            renderer.plots[next_id] = selected_plot.from_config(
                next_id, renderer, values, selected_view)
            return list(renderer.plots.values()), None, None
        else:  # Case where we remove a plot
            for plot_id, n_clicks in zip(plot_ids, plot_close_buttons):
                if n_clicks:
                    renderer.plots.pop(plot_id["index"])
            return list(renderer.plots.values()), None, None

    return out
