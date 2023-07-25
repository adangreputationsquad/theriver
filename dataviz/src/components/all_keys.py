from dash import html, Output, Input

from datafiles.views.view import PointView
from dataviz.dataviz import DataStudyRenderer


def add(renderer: DataStudyRenderer, source: PointView, *args, **kwargs):
    plot_name = kwargs.get("plot_name", source.name)
    if isinstance(source.data, list):
        data = source.data
    elif isinstance(source.data, dict):
        data = list(source.data.keys())
    else:
        raise AssertionError()

    plot_id = renderer.next_id()
    plot = html.Div(
        className="plot",
        children=[
            html.Div(
                children=[
                    html.Thead(plot_name, style={'display': 'inline-block'}),
                    html.Button(
                        "X", id=plot_id + "_close",
                        style={'display': 'inline-block', "float": 'right'}
                        ),
                ]
            ),
            html.Div([str(data)], className="plot")
        ]
    )
    renderer.plots[plot_id] = plot

    @renderer.app.callback(
        Output("draggable", "children", allow_duplicate=True),
        [Input(plot_id + "_close", "id"),
         Input(plot_id + "_close", "n_clicks")],
        prevent_initial_call=True

    )
    def close(plot_id, n_clicks):
        plot_id = plot_id.strip("_close")
        if n_clicks is not None:
            renderer.plots.pop(plot_id)
        return list(renderer.plots.values())
