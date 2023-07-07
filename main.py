from datasudy.datastudy import DataStudy

if __name__ == '__main__':
    ds = DataStudy("Test data study", "my data study")
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

    csv_data.make_timeseries_view(
        "test", time_col="Date", value_col="Mobile Reach"
    )
    json_data.make_timeseries_view(
        "test_2",
        time_pattern="pages_per_visit/*/date",
        value_pattern="pages_per_visit/*/value"
    )

