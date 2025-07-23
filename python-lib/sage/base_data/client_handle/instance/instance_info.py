import pandas as pd
from sage.src.dss_funcs import get_nested_value


def main(client):
    instance_info = client.get_instance_info().raw
    df = pd.DataFrame(instance_info, index=[0])
    
    for c in ["dssStartupTimestamp"]:
        df[c] = pd.to_datetime(df[c], unit="ms", utc=True)
        df[c] = pd.to_datetime(df[c], utc=True)
        df[c] = df[c].fillna(pd.to_datetime("1970-01-01", utc=True))
        df[c] = df[c].dt.strftime("%Y-%m-%d %H:%M:%S.%f")

    return df