import pandas as pd
from dash import html, dcc, Output, Input
from dash.development.base_component import Component

from datafiles.views.view import View
from dataviz.irenderer import IDataStudyRenderer
import plotly.express as px

from dataviz.src.components.iplot import IPlot


class BarChart(IPlot):
    _name = "bar-chart"

    @classmethod
    def name(cls) -> str:
        return cls._name

    @staticmethod
    def new(plot_id: str, renderer: IDataStudyRenderer, source: View, *args,
            **kwargs) -> Component:
        # TODO: Make sure this is robust
        x_col, y_col = args[0], args[1]
        plot_name = kwargs.get("plot_name", source.name)
        if isinstance(source.data, pd.DataFrame):
            data = source.data
        else:
            raise NotImplementedError()
        available_columns = data.columns
        if y_col is None:
            y_col = x_col + '_Count'
            cols = data.columns.to_list()
            data = data.groupby(cols).size().reset_index(name=y_col)

        dropdown = None
        if len(available_columns) > 1:  # Else we only have x and y
            dropdown = html.Div(
                children=[
                    html.B("color "),
                    dcc.Dropdown(
                        id=source.name + 'color-dropdown',
                        options=[{'label': col, 'value': col} for col
                                 in available_columns],
                        value=x_col,
                        style={"width": "80%"}
                    )
                ],
                style={
                    "display": "inline-flex",
                    'width': '49%',
                    "float": "left",
                    "align-items": "center"
                }
            )
        plot = html.Div(
            className="plot",
            children=[
                html.Div(
                    children=IPlot.get_header(plot_id, plot_name)
                ),
                dcc.Graph(id=source.name + "graph"), dropdown]
        )

        renderer.plots[plot_id] = plot

        @renderer.app.callback(
            Output(source.name + "graph", "figure"),
            [Input(source.name + "color-dropdown", "value")]
        )
        def update_graph(color):
            layout = kwargs.pop("layout", {})

            fig = px.bar(
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

            return fig

        return plot

    @staticmethod
    def config_panel(selected_view: View) -> Component:
        pass

    @staticmethod
    def are_plot_args_valid(plot_args: list, selected_view: View) -> bool:
        pass

    @staticmethod
    def from_config(plot_id: str, renderer: IDataStudyRenderer, plot_args: list,
                    selected_view: View):
        pass
