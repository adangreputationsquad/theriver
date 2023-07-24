from dash import html

from datafiles.views.view import PointView
from dataviz.dataviz import DataStudyRenderer


def add(renderer: DataStudyRenderer, source: PointView, *args, **kwargs):
    plot_name = kwargs.get("plot_name", source.name)
    renderer.plots.append(
        html.Div(
            className="plot",
            children=[
                html.Thead(plot_name),
                html.Div(
                    [
                        html.Strong(source.name),
                        ": ",
                        source.data
                    ]
                )
            ]
        )
    )
