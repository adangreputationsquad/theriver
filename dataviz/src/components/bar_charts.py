import pandas as pd
from dash import html, dcc, Output, Input
from plotly.graph_objs import Layout

from datafiles.views.view import DfView
from dataviz.dataviz import DataStudyRenderer
import plotly.express as px

layout = Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)


def add(
        renderer: DataStudyRenderer, source: DfView, x_col, y_col=None, *args,
        **kwargs
):
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

    plot_id = renderer.next_id()
    plot = html.Div(
            className="plot",
            children=[
                html.Div(
                    children=[
                        html.Thead(plot_name,style={'display': 'inline-block'}),
                        html.Button("X", id=plot_id + "_close",style={'display':'inline-block', "float": 'right'}),
                    ]
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

    @renderer.app.callback(
        Output("draggable", "children", allow_duplicate=True),
        [Input(plot_id + "_close", "id"),
         Input(plot_id + "_close", "n_clicks")],
        prevent_initial_call=True
    )
    def close(plot_id, n_clicks):
        plot_id = plot_id.strip("_close")
        if n_clicks is not None:
            renderer.plots.pop(plot_id)
        return list(renderer.plots.values())