import pandas as pd
from dash import html, dcc
from dash.development.base_component import Component

from datafiles.views.view import View
from dataviz.irenderer import IDataStudyRenderer
import plotly.express as px

from dataviz.src.components.iplot import IPlot


class Histogram(IPlot):
    _name = "histogram"

    @classmethod
    def name(cls) -> str:
        return cls._name

    @staticmethod
    def new(plot_id: str, renderer: IDataStudyRenderer, source: View, *args,
            **kwargs) -> Component:
        x_col = kwargs.pop("x_col")
        y_col = kwargs.pop("y_col", None)
        color = kwargs.pop("color", None)
        if x_col is None:
            raise ValueError("x_col is required")

        plot_name = kwargs.get("plot_name", source.name)
        if isinstance(source.data, pd.DataFrame):
            data = source.data
        else:
            raise NotImplementedError()

        if y_col is None:
            y_col = x_col + '_Count'
            cols = data.columns.to_list()
            data = data.groupby(cols).size().reset_index(name=y_col)

        layout = kwargs.pop("layout", {})

        fig = px.histogram(
            data_frame=data, x=x_col, y=y_col, color=color,
            title="Graph with Column Selection"
        )

        layout.update(
            xaxis={'title': x_col},
            yaxis={'title': y_col},
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
        )

        fig.update_layout(layout)
        plot = html.Div(
            className="plot",
            children=[
                html.Div(
                    children=IPlot.get_header(plot_id, plot_name)
                ),
                dcc.Graph(id=f"{source.name}_{plot_id}_graph", figure=fig),
            ]
        )

        renderer.plots[plot_id] = plot

        return plot

    @staticmethod
    def config_panel(selected_view: View) -> list[Component]:
        return (
                IPlot.html_dropdown("X column", 0, selected_view.data.columns) +
                IPlot.html_dropdown("Y column", 1, selected_view.data.columns) +
                IPlot.html_dropdown("Color column", 2, selected_view.data.columns)
        )

    @staticmethod
    def are_plot_args_valid(plot_args: list, selected_view: View) -> bool:
        if not plot_args:
            return False
        return plot_args[0]

    @staticmethod
    def from_config(plot_id: str, renderer: IDataStudyRenderer, plot_args: list,
                    selected_view: View):
        return Histogram.new(plot_id, renderer, selected_view,
                            x_col=plot_args[0], y_col=plot_args[1],
                            color=plot_args[2])
