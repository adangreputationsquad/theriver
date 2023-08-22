import pandas as pd
from dash import html, dcc, Output, Input
from dash.development.base_component import Component
from datafiles.views.view import View
from dataviz.irenderer import IDataStudyRenderer
import plotly.express as px

from dataviz.src.components.iplot import IPlot


class ScatterPlot(IPlot):
    _name = "scatter-plot"

    @classmethod
    def name(cls) -> str:
        return cls._name

    @staticmethod
    def new(plot_id: str, renderer: IDataStudyRenderer, source: View, *args,
            **kwargs) -> Component:
        plot_name = kwargs.get("plot_name", source.name)
        if isinstance(source.data, pd.DataFrame):
            data = source.data
            x_col = kwargs.pop("x_col", source.data.columns[0])
            y_cols = kwargs.pop("y_cols", None)

            available_columns = data.columns if y_cols is None else y_cols

            if y_cols is None:
                y_cols = [kwargs.pop("y_col", available_columns[1])]
        else:
            raise NotImplementedError()

        plot = html.Div(
            className="plot",
            children=[
                html.Div(
                    children=IPlot.get_header(plot_id, source.name)
                ),
                dcc.Graph(id=source.name + "graph"),
                html.Div(
                    children=[
                        html.B("X "),
                        dcc.Dropdown(
                            className="dropdown-button",
                            id=source.name + 'x-dropdown',
                            options=[{'label': col, 'value': col} for col
                                     in available_columns],
                            value=x_col,
                            style={
                                "width": "80%",
                                "display": "inline-bock"
                            }
                        )
                    ],
                    style={
                        "display": "inline-flex",
                        'width': '49%',
                        "float": "left",
                        "align-items": "center"
                    }
                ),
                html.Div(
                    children=[
                        html.B("Y (multiple) "),
                        dcc.Dropdown(
                            className="dropdown-button",
                            id=source.name + 'y-dropdown',
                            options=[{'label': col, 'value': col} for col
                                     in available_columns],
                            value=y_cols,
                            multi=True,
                            style={"width": "80%"}
                        )
                    ],
                    style={
                        "display": "inline-flex",
                        'width': '49%',
                        "float": "right",
                        "align-items": "center"
                    }
                ), ]
        )

        @renderer.app.callback(
            Output(source.name + "graph", "figure"),
            [Input(source.name + "x-dropdown", "value"),
             Input(source.name + "y-dropdown", "value")]
        )
        def update_graph(x_col, y_cols):
            layout = kwargs.pop("layout", {})

            fig = px.scatter(
                data_frame=data, x=x_col, y=y_cols,
                title="Graph with Column Selection"
            )

            layout.update(
                xaxis={'title': x_col if x_col else "x"},
                yaxis={'title': ', '.join(y_cols) if y_cols else "y"},
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
