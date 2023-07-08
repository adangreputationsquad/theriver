from datastudy import DataStudy
from dataviz.plot_types import PLOT

if __name__ == '__main__':
    ds = DataStudy("Test data datafiles", "my data datafiles")
    csv_data = ds.add_csv(
        "data/example_data.csv",
        "My first data",
        "This data is a dataframe",
        encoding="utf-16",
        sep="\t"
    )
    json_data = ds.add_json(
        "data/example_data_3.json",
        "My first data but json",
        "This one is a json"
    )

    engagement = json_data.make_df_view(
        name="test_json_to_df",
        pattern="pages_per_visit/*/value"
    )

    engagement_2 = json_data.make_df_view(
        name="test_json_to_df_2",
        patterns=["pages_per_visit/*/value", "pages_per_visit/*/date"]
    )

    perfs_view = json_data.make_dict_view(
        name="test_viz_4",
        key_pattern="pages_per_visit/*/date",
        value_pattern="pages_per_visit/*/value"
        )
    ds.add_plot(engagement_2, PLOT.DF.TIMESERIES)
    ds.render()
