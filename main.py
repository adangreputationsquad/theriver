from study.datastudy import DataStudy
from dataviz.plot_types import PLOT
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

    json_data.make_point_view("test_viz", "pages_per_visit/0/date",
                              plot=PLOT.POINT.NAME_VALUE)
    json_data.make_point_view("test_viz_2", "pages_per_visit/1/date",
                              plot=PLOT.POINT.VALUE)
    csv_data.make_point_view("test_viz_3", col="Language", row=1,
                             plot=PLOT.POINT.NAME_VALUE)

    ds.render()
