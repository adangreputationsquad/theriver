from dash import html

from study.views.view import PointView
from dataviz.dataviz import DataStudyRenderer


def add(renderer: DataStudyRenderer, source: PointView, *args, **kwargs):
    renderer.plots.append(
        html.Div(
            children=[
                html.Div(
                    [
                        source.data
                    ]
                )
            ]
        )
    )
