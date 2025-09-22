from sage.insights.data_structures import structures
from sage.src import dss_duck
import plotly.express as px


def main(filters = {}):
    # Build SQL Query Statement and Query, 
    query = structures.get_query_dict()
    query["select"] = ["*"]
    query["from"]   = ["recipes_metadata"]
    df = dss_duck.query_duckdb(query, filters)

    # load data structure
    FIG = structures.get("metric")
    
    # Perform logic here
    FIGS = []
    FIG["label"] = "Average number of Recipes per Project -- All"
    FIG["data"] = df.groupby("project_key")["recipe_name"].count().mean().round(0).astype(int)
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Average number of Recipes per Project -- {i}"
        FIG["data"] = g.groupby("project_key")["recipe_name"].count().mean().round(0).astype(int)
        FIGS.append(FIG)

    return FIGS