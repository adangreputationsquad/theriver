import pandas as pd
from dash import html, dcc

from study.views.view import PointView
from dataviz.dataviz import DataStudyRenderer
from dateutil import parser


def add(renderer: DataStudyRenderer, source: PointView, *args, **kwargs):
    if isinstance(source.data, dict):
        dates = [parser.parse(date_str) for date_str in source.data.keys()]
        values = list(source.data.values())
    elif isinstance(source.data, pd.DataFrame):
        val_col = kwargs.pop("val_col", None)
        time_col = kwargs.pop("time_col", None)
        if len(source.data.columns) > 2 and (val_col is None
                                             or time_col is None):
            raise AssertionError(
                "Ambiguous values for date columns and value"
                "columns, specify 'val_col' and 'time_col' kwargs"
            )
        if time_col is None:
            time_col = detect_date_column(source.data)
        dates = [parser.parse(date_str) for date_str in
                 source.data[time_col]]
        values = source.data.drop(columns=[time_col]).squeeze()

    else:
        raise NotImplementedError()

    renderer.plots.append(
        html.Div(
            children=[dcc.Graph(
                figure={
                    'data': [
                        {
                            'x': dates, 'y': values, 'type': 'line',
                            'name': 'Timeseries'
                        },
                    ],
                    'layout': {
                        'title': 'Timeseries Graph',
                        'xaxis': {'title': 'Date'},
                        'yaxis': {'title': 'Value'}
                    }
                }
            )]
        )
    )


def detect_date_column(dataframe):
    date_column = None
    for col in dataframe.columns:
        try:
            # We need to check if we don't have a float because pandas will
            # interpret floats as date
            if not dataframe[col].dtype == "float":
                pd.to_datetime(dataframe[col])
                if date_column is not None:
                    raise AssertionError("Multiple potential date columns "
                                         "detected")
                date_column = col
        except ValueError or pd.errors.ParserError:
            pass
    if date_column is None:
        raise ValueError("No date column detected")

    return date_column
