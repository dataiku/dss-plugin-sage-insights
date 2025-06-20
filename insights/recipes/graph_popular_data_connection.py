import pandas as pd


def main(df=None, df_filter={}):
    meta = {
        "pass": True,
        "type": "bar",
        "title": "Recipes count by Recipe Type"
    }
    final_df = df.groupby("recipe_type")["project_key"].count()
    return [meta, final_df]