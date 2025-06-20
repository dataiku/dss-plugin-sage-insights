import pandas as pd


def main(df=None, df_filter={}):
    # Metadata csv is already passed in
    # Example to load other data: from sage.src import dss_folder; df = dss_folder.read_folder_input(folder_name="base_data", path = "/users/metadata.csv")
    meta = {
        "pass": True,
        "type": "metric",
        "title": "Example",
        "delta": 2,
        "value": 10
    }
    return [meta, None]