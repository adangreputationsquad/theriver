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


def add(renderer: DataStudyRenderer, source: DfView, *args, **kwargs):
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

    plot_id = renderer.next_id()
    plot = html.Div(
        className="plot",
        children=[
            html.Div(
                children=[
                    html.Thead(plot_name, style={'display': 'inline-block'}),
                    html.Button(
                        "X", id=plot_id + "_close", style={
                            'display': 'inline-block', "float": 'right'
                        }
                        ),
                ]
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
    renderer.plots[plot_id] = plot

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