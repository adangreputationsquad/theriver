import pandas as pd
from dash import html, dcc, Output, Input
from plotly.graph_objs import Layout

from datafiles.views.view import DfView, DictView
from dataviz.dataviz import DataStudyRenderer
from dateutil import parser
import plotly.express as px

layout = Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)


def add(
        renderer: DataStudyRenderer, source: DfView | DictView,
        *args, **kwargs
):
    plot_name = kwargs.get("plot_name", source.name)
    val_col = kwargs.pop("val_col", None)
    val_cols = kwargs.pop("val_cols", None)
    time_col = kwargs.pop("time_col", None)
    if isinstance(source.data, dict):
        dates = [parser.parse(date_str) for date_str in source.data.keys()]
        values = list(source.data.values())
        data = pd.DataFrame(
            {
                "date": dates,
                "value": values
            }
        )
        nb_vars = 1
    elif isinstance(source.data, pd.DataFrame):
        data = source.data
        if time_col is None:
            time_col = detect_date_column(source.data)
        if val_cols is None:
            val_cols = source.data.columns.to_list()
            val_cols.remove(time_col)
        val_col = val_cols[0]
        nb_vars = len(val_cols)

        data[time_col] = source.data[time_col].apply(parser.parse)
    else:
        raise NotImplementedError()

    layout = kwargs.pop("layout", {})
    fig = px.line(
        data_frame=data, x=time_col, y=val_col,
        title=source.name, *args, **kwargs
    )

    layout.update(
        xaxis={'title': time_col if time_col else "Date"},
        yaxis={'title': val_col if val_col else "Value"}
    )

    fig.update_layout(layout)

    dropdown = None
    if nb_vars > 1:
        dropdown = html.Div(
            className="dropdown-button",
            children=[
                html.B("Y (multiple) "),
                dcc.Dropdown(
                    id=source.name + '_y-dropdown',
                    options=[{'label': col, 'value': col} for col
                             in val_cols],
                    value=[val_col],
                    multi=True,
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
            dcc.Graph(figure=fig, id=source.name + "_graph"),
            dropdown
        ]
    )
    renderer.plots[plot_id] = plot

    if nb_vars > 1:
        @renderer.app.callback(
            Output(source.name + "_graph", "figure"),
            [Input(source.name + "_y-dropdown", "value")]
        )
        def update_graph(y_cols):
            layout = kwargs.pop("layout", {})

            fig = px.line(
                data_frame=data, x=time_col, y=y_cols,
                title="Graph with Column Selection"
            )

            layout.update(
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


def detect_date_column(dataframe):
    date_column = None
    for col in dataframe.columns:
        try:
            # We need to check if we don't have a float because pandas will
            # interpret floats as date
            if not dataframe[col].dtype == "float":
                pd.to_datetime(dataframe[col])
                if date_column is not None:
                    raise AssertionError(
                        "Multiple potential date columns "
                        "detected"
                    )
                date_column = col
        except ValueError or pd.errors.ParserError:
            pass
    if date_column is None:
        raise ValueError("No date column detected")

    return date_column
