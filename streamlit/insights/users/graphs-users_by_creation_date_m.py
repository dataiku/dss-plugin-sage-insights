import streamlit as st
import pandas as pd
import plotly.express as px

from sage.insights.data_structures import structures
from sage.src import dss_funcs, dss_folder

local_client = dss_funcs.build_local_client()
project_handle = local_client.get_default_project()
sage_project_key = project_handle.project_key

def main(df=pd.DataFrame()):
    # load data structure
    FIG = structures.get("plotly")

    # Load additional data
    if df.empty:
        df = dss_folder.read_local_folder_input(
            sage_project_key = sage_project_key,
            project_handle = project_handle,
            folder_name="base_data",
            path=f"/users/metadata.csv"
        )

    # Ensure 'creationDate' is datetime
    df['creationDate'] = pd.to_datetime(df['creationDate'], errors='coerce')

    # Group by month and count users created in each month
    monthly_counts = (
        df
        .groupby(df['creationDate'].dt.to_period('M'))
        .size()
        .reset_index(name='user_count')
    )

    # Convert period back to datetime for plotting
    monthly_counts['creationMonth'] = monthly_counts['creationDate'].dt.to_timestamp()

    # Compute cumulative sum
    monthly_counts['cumulative_users'] = monthly_counts['user_count'].cumsum()

    # Create the figure here
    fig = px.line(
        monthly_counts,
        x='creationMonth',
        y='cumulative_users',
        title='Cumulative Number of Users by Creation Date (Monthly)',
        labels={'creationMonth': 'Creation Date (Month)', 'cumulative_users': 'Cumulative Users'}
    )

    # Update layout
    fig.update_layout(xaxis_tickformat='%Y-%m', xaxis=dict(tickangle=-45))

    # Return as Dataiku insight figure
    FIG["title"] = "Cumulative Number of Users by Month"
    FIG["data"] = fig
    
    return FIG
