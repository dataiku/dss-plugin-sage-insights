import streamlit as st
import pandas as pd
from sage.src import dss_folder
from sage.insights.data_structures import structures

def main(df=pd.DataFrame()):
    # load data structure
    data = structures.get("bar_chart") # change this line

    # Load additional data
    if df.empty:
        df = dss_folder.read_folder_input(
            folder_name="base_data",
            path=f"/{st.session_state.instance_name}/projects/metadata.csv" # change this line
        )

    # Perform logic here
    from datetime import date, timedelta
    today = date.today()
    md = { "days": [], "count": [] }
    for n in [30, 60, 90, 365]:
        activity = df[df["lastModifiedOn"].dt.date >= (today - timedelta(n))]
        md["days"].append(n)
        md["count"].append(activity["project_key"].nunique())
    df = pd.DataFrame(md)
    df.set_index("days", inplace=True)

    # Build the data structure
    data["title"] = "Active Projects over Days"
    data["data"] = df
    data["x_label"] = "Number of Active Projects"
    data["y_label"] = "# of Days"
    data["horizontal"] = True
    
    return data