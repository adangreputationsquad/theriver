from dash import html

from study.views.view import PointView
from dataviz.dataviz import DataStudyRenderer


def add(renderer: DataStudyRenderer, source: PointView, *args, **kwargs):
    if not isinstance(source.data, dict):
        raise AssertionError()

    renderer.plots.append(
        html.Div(children=[html.Div(
            [str("<br>".join([
                f'{key}: {val}' for key, val in source.data.items()
            ]))]
        )])
    )
