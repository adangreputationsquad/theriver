import pandas as pd
from dash import html, dcc, Output, Input
from dash.development.base_component import Component

from datafiles.views.view import View
from dataviz.irenderer import IDataStudyRenderer
import plotly.graph_objects as go

from dataviz.src.components.iplot import IPlot


class PieChart(IPlot):
    _name = "pie chart"

    @classmethod
    def name(cls) -> str:
        return cls._name

    # TODO: Make sure this is robust
    pulled = {}

    @staticmethod
    def new(plot_id: str, renderer: IDataStudyRenderer, source: View, *args,
            **kwargs) -> Component:
        plot_name = kwargs.get("plot_name", source.name)
        if isinstance(source.data, pd.DataFrame):
            data = source.data
            labels = kwargs.pop("names")
            values = kwargs.pop("values")
            if labels is None or values is None:
                labels, values = check_columns(data)
            labels = data[labels]
            values = data[values]
        elif isinstance(source.data, dict):
            labels = list(source.data.keys())
            values = list(source.data.values())
        else:
            raise NotImplementedError()

        plot = html.Div(
            className="plot",
            children=[
                html.Div(
                    children=IPlot.get_header(plot_id, plot_name)
                ),
                dcc.Graph(id=source.name + "graph"),
            ]
        )

        @renderer.app.callback(
            Output(source.name + "graph", "figure"),
            [Input(source.name + "graph", "clickData")]
        )
        def update_graph(clickData):
            pulled = PieChart.pulled.get(source.name)
            layout = kwargs.pop("layout", {})
            layout.update(
                template='plotly_dark',
                plot_bgcolor='rgba(0, 0, 0, 0)',
                paper_bgcolor='rgba(0, 0, 0, 0)',
            )
            pull = [0] * len(labels)
            if clickData is not None:
                if pulled == clickData["points"][0]["pointNumber"]:
                    pulled = None
                else:
                    pulled = clickData["points"][0]["pointNumber"]
                    value = clickData["points"][0]["value"]
                    pull[int(pulled)] = 0.1 + ((1 - value) * 0.3)
            PieChart.pulled[source.name] = pulled
            fig = go.Figure(
                data=[go.Pie(
                    labels=labels,
                    values=values,
                    pull=pull
                )], layout=layout
            )

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


_PULLED = None


def check_columns(df):
    string_col = None
    scalar_col = None

    if len(df.columns) != 2:
        raise ValueError(
            "Ambiguous data, got a dataframe that does not have two columns."
            "Use another view or pass labels and values arguments."
        )

        # Iterate over columns
    for column in df.columns:
        if df[column].dtype == object:
            if string_col is None:
                string_col = column
            else:
                raise ValueError("Multiple string columns found.")
        elif pd.api.types.is_numeric_dtype(df[column]):
            if scalar_col is None:
                scalar_col = column
            else:
                raise ValueError("Multiple scalar columns found.")

    if string_col is None or scalar_col is None:
        raise ValueError("Both string and scalar columns are not present.")

    return string_col, scalar_col
