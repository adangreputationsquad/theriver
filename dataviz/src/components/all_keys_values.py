from dash import html

from datafiles.views.view import PointView
from dataviz.dataviz import DataStudyRenderer


def add(renderer: DataStudyRenderer, source: PointView, *args, **kwargs):
    plot_name = kwargs.get("plot_name", source.name)
    if not isinstance(source.data, dict):
        raise AssertionError()

    text = []
    for key, val in source.data.items():
        text.append(f'{key}: {val}')
        text.append(html.Br())

    renderer.plots.append(
        html.Div(
            className="plot",
            children=[
                html.Div(
                    [
                        html.B(source.name),
                        html.P(text)
                    ],
                    className="plot"
                )]
        )
    )
