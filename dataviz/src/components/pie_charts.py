import pandas as pd
from dash import html, dcc, Output, Input
from plotly.graph_objs import Layout

from datafiles.views.view import DfView
from dataviz.dataviz import DataStudyRenderer
import plotly.graph_objects as go

layout = Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
_PULLED = None


def add(renderer: DataStudyRenderer, source: DfView, *args, **kwargs):
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

    plot_id = renderer.next_id()
    plot = html.Div(
            className="plot",
            children=[
                html.Thead(plot_name),
                dcc.Graph(id=source.name + "graph"),
            ]
        )
    renderer.plots[plot_id] = plot

    @renderer.app.callback(
        Output(source.name + "graph", "figure"),
        [Input(source.name + "graph", "clickData")]
    )
    def update_graph(clickData):
        global _PULLED
        layout = kwargs.pop("layout", {})
        layout.update(
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
        )
        pull = [0] * len(labels)
        if clickData is not None:
            if _PULLED == clickData["points"][0]["pointNumber"]:
                _PULLED = None
            else:
                _PULLED = clickData["points"][0]["pointNumber"]
                value = clickData["points"][0]["value"]
                pull[int(_PULLED)] = 0.1 + ((1 - value) * 0.3)

        fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=values,
                pull=pull
            )], layout=layout
        )

        return fig


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
