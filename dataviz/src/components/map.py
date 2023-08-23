import json

import pandas as pd
from dash import html, dcc, Output, Input
from dash.development.base_component import Component

from datafiles.views.view import View, DfView, DictView
from dataviz.irenderer import IDataStudyRenderer
import plotly.graph_objects as go

from dataviz.src.components.iplot import IPlot

with open("dataviz/assets/countries.geojson", "r") as f:
    countries_geojson = json.load(f)

countries_codes = pd.read_csv(
    "dataviz/assets/countries_codes.csv",
    sep="\t", header=0
)


class Map(IPlot):
    _name = "map"

    @classmethod
    def name(cls) -> str:
        return cls._name

    @staticmethod
    def new(plot_id: str, renderer: IDataStudyRenderer, source: View, *args,
            **kwargs) -> Component:
        plot_name = kwargs.get("plot_name", source.name)
        if isinstance(source.data, pd.DataFrame):
            countries = kwargs.pop("countries")
            values = kwargs.pop("values")
        elif isinstance(source.data, dict):
            countries = list(source.data.keys())
            values = list(source.data.values())
        else:
            raise NotImplementedError()

        if countries[0] in countries_codes["Numeric code"].values:
            countries = [
                countries_codes.set_index('Numeric code')['Alpha-3 code'][code]
                for code in countries
            ]
        elif countries[0] in countries_codes["Alpha-2 code"].values:
            countries = [
                countries_codes.set_index('Numeric code')['Alpha-3 code'][code]
                for code in countries
            ]

        layout = kwargs.pop("layout", {})

        fig = go.Figure(
            go.Choroplethmapbox(
                geojson=countries_geojson, locations=countries, z=values,
                colorscale="Viridis", featureidkey="properties.ISO_A3",
            )
        )

        layout.update(
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            mapbox_style="carto-positron",
        )

        fig.update_layout(layout)

        plot = html.Div(
            className="plot",
            children=[
                html.Div(
                    children=IPlot.get_header(plot_id, plot_name)
                ),
                dcc.Graph(id=f"{source.name}_{plot_id}_graph", figure=go.Figure(fig))]
        )
        return plot

    @staticmethod
    def config_panel(selected_view: View) -> list[Component]:
        if isinstance(selected_view, DfView):
            return [IPlot.html_dropdown("Country_column", 0,
                                        selected_view.data.columns),
                    IPlot.html_dropdown("Value_column", 1,
                                        selected_view.data.columns, multi=True)
                    ]
        elif isinstance(selected_view, DictView):
            return []
        else:
            raise NotImplementedError()

    @staticmethod
    def are_plot_args_valid(plot_args: list, selected_view: View) -> bool:
        if isinstance(selected_view, DictView):
            return True
        elif isinstance(selected_view, DfView):
            return all(plot_args) and plot_args
        raise NotImplementedError()

    @staticmethod
    def from_config(plot_id: str, renderer: IDataStudyRenderer, plot_args: list,
                    selected_view: View):
        print("Making map")
        if isinstance(selected_view, DictView):
            return Map.new(plot_id, renderer, selected_view)
        elif isinstance(selected_view, DfView):
            return Map.new(plot_id, renderer, selected_view,
                           countries=plot_args[0], values=plot_args[1])
        raise NotImplementedError()
