from datastudy import DataStudy
from utils import math_pattern_to_values

if __name__ == '__main__':
    ds = DataStudy("Test data study", "my data study")
    ds.add_csv(
        "data/example_data.csv",
        "My first data",
        "This data is a dataframe",
        encoding="utf-16",
        sep="\t"
    )
    ds.add_json(
        "dadta/example_data_3.json",
        "My first data but json",
        "This one is a json"
    )

    ds.datas["My first data"].make_timeseries_view(
        "test", time_col="Date", value_col="Mobile Reach"
    )
    ds.datas["My first data but json"].make_timeseries_view(
        "test_2",
        time_pattern="pages_per_visit/*/date",
        value_pattern="pages_per_visit/*/value"
    )

