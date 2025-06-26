import pandas as pd


def main(df=None, df_filter={}):
    # Metadata csv is already passed in
    # Example to load other data: from sage.src import dss_folder; df = dss_folder.read_folder_input(folder_name="base_data", path = "/users/metadata.csv")
    meta = {
        "pass": True,
        "type": "bar",
        "title": "Example"
    }
    d = {
        "value_1": [1,2,3,4,5],
        "value_2": [3,4,5,6,7]
    }
    df = pd.DataFrame(d)
    return [meta, df]