from dash import html

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
                html.Thead(plot_name),
                html.Div([str(data)], className="plot")
            ])
    renderer.plots[plot_id] = plot
