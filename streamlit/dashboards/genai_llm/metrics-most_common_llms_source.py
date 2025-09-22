from sage.dashboards.data_structures import structures
from sage.src import dss_duck
import plotly.express as px


def main(filters = {}):
    # Build SQL Query Statement and Query, 
    query = structures.get_query_dict()
    query["select"] = ["*"]
    query["from"]   = ["addon_llm_mapping as base"]
    df = dss_duck.query_duckdb(query, filters)

    # load data structure
    FIG = structures.get("metric")
    
    # Perform logic here
    FIGS = []
    FIG["label"] = "Most used LLM LLM Mesh -- All"
    FIG["data"] = df.groupby("llms_conn").size().sort_values().tail(1).reset_index()["llms_conn"][0]
    FIGS.append(FIG)

    # Split by Instance
    for i, g in df.groupby("instance_name"):
        FIG = structures.get("metric")
        FIG["label"] = f"Most used LLM LLM Mesh -- {i}"
        FIG["data"] = g.groupby("llms_conn").size().sort_values().tail(1).reset_index()["llms_conn"][0]
        FIGS.append(FIG)

    return FIGS