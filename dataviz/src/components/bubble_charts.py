from dash import html, dcc
from dash.development.base_component import Component
from datafiles.views.view import View, DfView
from dataviz.irenderer import IDataStudyRenderer
import plotly.express as px

from dataviz.src.components.iplot import IPlot


class BubbleChart(IPlot):
    _name = "bubble-chart"

    @classmethod
    def name(cls) -> str:
        return cls._name

    @staticmethod
    def new(plot_id: str, renderer: IDataStudyRenderer, source: View, *args,
            **kwargs) -> Component:
        plot_name = kwargs.get("plot_name", source.name)
        if isinstance(source, DfView):
            data = source.data

            size = kwargs.pop("size", None)
            color = kwargs.pop("color", None)
            hover_name = kwargs.pop("hover_name", None)
            for arg in [size, color, hover_name]:
                if arg not in data.columns and arg is not None:
                    raise ValueError(f"Column {arg} not found")
            x_col = kwargs.pop("x_col", source.data.columns[0])
            y_col = kwargs.pop("y_col",
                               [col for col in data.columns if col != x_col])

        else:
            raise NotImplementedError()
        layout = kwargs.pop("layout", {})

        fig = px.scatter(
            data_frame=data, x=x_col, y=y_col,
            size=size, color=color, hover_name=hover_name,
            title="Graph with Column Selection"
        )

        layout.update(
            xaxis={'title': x_col if x_col else "x"},
            yaxis={'title': ', '.join(y_col) if y_col else "y"},
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

        return plot

    @staticmethod
    def config_panel(selected_view: View) -> list[Component]:
        if isinstance(selected_view, DfView):
            return (
                    IPlot.html_dropdown("X column", 0,
                                        selected_view.data.columns) +
                    IPlot.html_dropdown("Y column", 1,
                                        selected_view.data.columns) +
                    IPlot.html_dropdown("Size column", 2,
                                        selected_view.data.columns) +
                    IPlot.html_dropdown("Color column", 3,
                                        selected_view.data.columns)
            )
        raise NotImplementedError()

    @staticmethod
    def are_plot_args_valid(plot_args: list, selected_view: View) -> bool:
        return all(plot_args[:3]) and plot_args

    @staticmethod
    def from_config(plot_id: str, renderer: IDataStudyRenderer, plot_args: list,
                    selected_view: View):
        return BubbleChart.new(plot_id, renderer, selected_view,
                               x_col=plot_args[0], y_col=plot_args[1],
                               size=plot_args[2], color=plot_args[3])
