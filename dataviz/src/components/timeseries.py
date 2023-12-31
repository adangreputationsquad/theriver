import pandas as pd
from dash import html, dcc

from dataviz.irenderer import IDataStudyRenderer
from dateutil import parser
from datafiles.views.view import DictView, DfView, View
import plotly.express as px

from dataviz.src.components.iplot import IPlot


class Timeseries(IPlot):
    _name = "timeseries"

    @classmethod
    def name(cls) -> str:
        return cls._name

    @staticmethod
    def new(
            plot_id: str,
            renderer: IDataStudyRenderer, source: DfView | DictView,
            *args, **kwargs
    ):
        plot_name = kwargs.get("plot_name", source.name)
        val_cols = kwargs.pop("val_cols", None)
        time_col = kwargs.pop("time_col", None)

        # equivalent to isinstance(source, DictView)
        if isinstance(source.data, dict):
            dates = [parser.parse(date_str) for date_str in source.data.keys()]
            values = list(source.data.values())
            time_col = "date"
            val_col = "value"

            data = pd.DataFrame(
                {
                    time_col: dates,
                    val_col: values
                }
            )
            nb_vars = 1
        elif isinstance(source.data, pd.DataFrame):
            data = source.data
            if time_col is None:
                time_col = Timeseries.detect_date_column(source.data)
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

        plot = html.Div(
            children=[
                html.Div(
                    children=IPlot.get_header(plot_id, plot_name)
                ),
                dcc.Graph(figure=fig, id=source.name + "_graph"),
                dropdown
            ]
        )

        return plot

    @staticmethod
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

    @staticmethod
    def config_panel(selected_view: View):
        if isinstance(selected_view, DfView):
            return (
                IPlot.html_dropdown("Time column",
                                    0,
                                    options=selected_view.data.columns) +
                IPlot.html_dropdown("Time column",
                                    1,
                                    options=selected_view.data.columns,
                                    multi=True)
            )
        elif isinstance(selected_view, DictView):
            return []
        raise NotImplementedError()

    @staticmethod
    def are_plot_args_valid(plot_args, selected_view):
        if isinstance(selected_view, DictView):
            try:
                _ = [parser.parse(date_str)
                     for date_str in selected_view.data.keys()]
            except (parser.ParserError, TypeError):
                return False
            return True
        elif isinstance(selected_view, DfView):
            return all(plot_args) and plot_args
        raise NotImplementedError()

    @staticmethod
    def from_config(plot_id, renderer, plot_args, selected_view):
        if isinstance(selected_view, DfView):
            return Timeseries.new(
                plot_id,
                renderer=renderer,
                source=selected_view,
                time_col=plot_args[0],
                val_cols=plot_args[1])
        elif isinstance(selected_view, DictView):
            return Timeseries.new(plot_id, renderer, selected_view)
