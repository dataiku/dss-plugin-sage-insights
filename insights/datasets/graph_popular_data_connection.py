import pandas as pd


def main(df=None, df_filter={}):
    meta = {
        "pass": True,
        "type": "bar",
        "title": "Dataset count by Connection Type"
    }
    final_df = df.groupby("dataset_type")["project_key"].count()
    return [meta, final_df]