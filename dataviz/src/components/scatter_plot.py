import pandas as pd
from dash import html, dcc, Output, Input
from dash.development.base_component import Component
from datafiles.views.view import View, DfView, DictView
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
        if isinstance(source, DfView):
            data = source.data
            x_col = kwargs.pop("x_col", source.data.columns[0])
            y_cols = kwargs.pop("y_cols",
                                [col for col in data.columns if col != x_col])

        elif isinstance(source, DictView):
            data = pd.DataFrame().from_dict({"keys": source.data.keys(),
                                             "values": source.data.values()})
            x_col = "keys"
            y_cols = ["values"]
        else:
            raise NotImplementedError()

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
                IPlot.html_dropdown("Y column(s)", 1,
                                    selected_view.data.columns, multi=True)
            )
        elif isinstance(selected_view, DictView):
            return []
        raise NotImplementedError()

    @staticmethod
    def are_plot_args_valid(plot_args: list, selected_view: View) -> bool:
        if isinstance(selected_view, DictView):
            try:
                _ = [float(date_str)
                     for date_str in selected_view.data.keys()]
            except TypeError:
                return False
            return True
        elif isinstance(selected_view, DfView):
            return all(plot_args) and plot_args
        raise NotImplementedError()

    @staticmethod
    def from_config(plot_id: str, renderer: IDataStudyRenderer, plot_args: list,
                    selected_view: View):
        if isinstance(selected_view, DfView):
            return ScatterPlot.new(
                plot_id,
                renderer=renderer,
                source=selected_view,
                x_col=plot_args[0],
                y_cols=plot_args[1])
        elif isinstance(selected_view, DictView):
            return ScatterPlot.new(plot_id, renderer, selected_view)
