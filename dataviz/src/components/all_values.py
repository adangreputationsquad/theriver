from dash import html

from study.views.view import PointView
from dataviz.dataviz import DataStudyRenderer


def add(renderer: DataStudyRenderer, source: PointView):
    if isinstance(source.data, list):
        data = source.data
    elif isinstance(source.data, dict):
        data = list(source.data.values())
    else:
        raise AssertionError()
    renderer.plots.append(
        html.Div(children=[html.Div([str(data)])])
    )
