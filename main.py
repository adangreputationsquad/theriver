from datastudy import DataStudy
from dataviz.plot_types import PLOT

if __name__ == '__main__':
    import plotly.express as px

    long_df = px.data.medals_long()

    ds = DataStudy("Test data datafiles", "Description of the study")
    csv_data = ds.add_csv(
        path="data/example_data_2.csv",
        name="My first data",
        desc="This data is a dataframe",
        encoding="utf-8",
        sep=","
    )
    json_data = ds.add_json(
        path="data/example_data_2.json",
        name="My first data but json",
        desc="This one is a json"
    )

    engagement = json_data.make_df_view(
        name="test_json_to_df",
        patterns=["pages_per_visit/*/value", "visits/*/value",
                  "unique_visitors/*/value"],
        cols_name=["pages_per_visit", "visits", "unique_visitors"],
        plot=PLOT.DF.SCATTER_PLOT
    )

    engagement_2 = json_data.make_df_view(
        name="test_json_to_df_timeseries",
        patterns=["pages_per_visit/*/value", "pages_per_visit/*/date",
                  "unique_visitors/*/value"],
        plot=PLOT.DF.TIMESERIES
    )

    medals = csv_data.make_df_view(
        name="test_bars",
        cols=["Medal", "Country"],
        group_by="Country",
        plot=PLOT.DF.BAR_CHARTS,
        x_col="Country",
    )

    ds.render(debug=True)
