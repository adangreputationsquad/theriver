import json

import pandas as pd
from dash import html, dcc
from plotly.graph_objs import Layout

from datafiles.views.view import DfView
from dataviz.dataviz import DataStudyRenderer
import plotly.graph_objects as go

layout = Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
with open("dataviz/assets/countries.geojson", "r") as f:
    countries_geojson = json.load(f)

countries_codes = pd.read_csv(
    "dataviz/assets/countries_codes.csv",
    sep="\t", header=0
)


def add(renderer: DataStudyRenderer, source: DfView, *args, **kwargs):

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
        ),
        layout={"title": source.name}
    )

    layout.update(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        mapbox_style="carto-positron",
    )

    fig.update_layout(layout)

    renderer.plots.append(
        html.Div(
            className="plot",
            children=[
                dcc.Graph(id=source.name + "graph", figure=go.Figure(fig))]
        )
    )
