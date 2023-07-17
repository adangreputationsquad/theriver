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

    countries_data = ds.add_json(
        path=("/home/alexandre/Dropbox (Reputation Squad)/DATAPROJECTS/lib/"
              "Similar43/ressources/example_data_2.json"),
        name="countries",

    )

    countries_view = countries_data.make_dict_view(
        name="countries_view",
        key_pattern="top_country_shares/*/country",
        value_pattern="top_country_shares/*/value",
    )

    # engagement = json_data.make_df_view(
    #     name="test_json_to_df",
    #     patterns=["pages_per_visit/*/value", "visits/*/value",
    #               "unique_visitors/*/value"],
    #     cols_name=["pages_per_visit", "visits", "unique_visitors"],
    #     plot=PLOT.DF.SCATTER_PLOT
    # )

    total_traffic = countries_data.make_point_view(
        name="total_traffic",
        pattern="estimated_monthly_visits/2023-05-01"
    )

    weighted_countries = countries_view.apply(lambda x: x * total_traffic(),
                                              name="weighted_countries")

    ds.add_plot(weighted_countries, plot_type=PLOT.DICT.MAP)

    ds.render(debug=True)

