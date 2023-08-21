import json

import pandas as pd
from dash import html, dcc, Output, Input
from plotly.graph_objs import Layout

from datafiles.views.view import DfView
from dataviz.irenderer import IDataStudyRenderer
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


def add(renderer: IDataStudyRenderer, source: DfView, *args, **kwargs):
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
            dcc.Graph(id=source.name + "graph", figure=go.Figure(fig))]
    )

    renderer.plots[plot_id] = plot

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