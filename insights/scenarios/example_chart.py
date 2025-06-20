import pandas as pd


def main(df=None, df_filter={}):
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