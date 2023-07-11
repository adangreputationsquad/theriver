from dash import html

from datafiles.views.view import PointView
from dataviz.dataviz import DataStudyRenderer


def add(renderer: DataStudyRenderer, source: PointView, *args, **kwargs):
    if isinstance(source.data, list):
        data = source.data
    elif isinstance(source.data, dict):
        data = list(source.data.keys())
    else:
        raise AssertionError()
    renderer.plots.append(
        html.Div(
            className="plot",
            children=[html.Div([str(data)], className="plot")])
    )
