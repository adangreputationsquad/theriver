from datastudy import DataStudy

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
        "data/example_data.json",
        "My first data but json",
        "This one is a json"
    )
