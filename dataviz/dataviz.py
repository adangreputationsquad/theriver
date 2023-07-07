import pandas as pd
from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP


class DataStudyRenderer:

    def __init__(self, title, desc):
        self.app = Dash(external_stylesheets=[BOOTSTRAP])
        self.app.title = title
        self.desc = desc
        self.plots = list[html.Div]

    def run(self):
        self.app.layout = self.create_layout()
        self.app.run()

    def create_layout(self) -> html.Div:
        return html.Div(
            className="app-div",
            children=[
                html.H1(self.app.title),
                html.Hr(),
            ],
        )

    def add_timeseries_plot(self, dataframe: pd.DataFrame, name: str):
        pass


if __name__ == "__main__":
    renderer = DataStudyRenderer()
    renderer.run()
