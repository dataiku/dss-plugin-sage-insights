import pandas as pd
from sage.src import dss_folder

def main(df=None, df_filter={}):
    # Actually need a different dataset
    df = dss_folder.read_folder_input(folder_name="base_data", path="/mazzei_designer/scenarios/run_history.csv")
    filtered = df[df["step_outcome"] == "FAILED"]
    top10 = filtered.groupby('step_error_message').agg(
        type_count=('step_error_message', 'count')
    ).reset_index().sort_values("type_count", ascending=False)[:10]
    meta = {
        "pass": True,
        "type": "top10",
        "title": "Top 10 Scenario Error Messages"
    }
    return [meta, top10]