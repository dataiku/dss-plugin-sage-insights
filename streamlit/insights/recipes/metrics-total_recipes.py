from sage.insights.data_structures import structures
from sage.src import dss_duck
import plotly.express as px


def main(filters = {}):
    # Build SQL Query Statement and Query, 
    query = structures.get_query_dict()
    query["select"] = ["*"]
    query["from"]   = ["recipes_metadata"]
    df = dss_duck.query_duckdb(query, filters, debug=True)

    # load data structure
    FIG = structures.get("metric")
    
    # Perform logic here
    FIGS = []
    FIG["label"] = "Total number of Recipes -- All"
    FIG["data"] = df["recipe_name"].nunique()
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Total number of Recipes -- {i}"
        FIG["data"] = g["recipe_name"].nunique()
        FIGS.append(FIG)

    return FIGS