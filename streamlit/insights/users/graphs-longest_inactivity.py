import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import datetime, timedelta      

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

    # Perform logic here
    # Parse last session and calculate inactivity
    now = datetime.now()

    df['last_session_activity'] = pd.to_datetime(df['last_session_activity'], errors='coerce')
    df['days_inactive'] = (now - df['last_session_activity']).dt.days
    df['days_inactive'] = df['days_inactive'].fillna(9999)

    inactive_users_df = df.copy()

    # Fill displayName if missing
    inactive_users_df['displayName'] = inactive_users_df['displayName'].fillna(inactive_users_df['login'])
    inactive_users_df['displayLabel'] = inactive_users_df.apply(
        lambda row: f"{row['displayName']} ({row['login']})" 
        if inactive_users_df['displayName'].duplicated(keep=False)[row.name] else row['displayName'],
        axis=1
    )   

    # Sort and take top 10
    top_inactive = inactive_users_df.sort_values(by='days_inactive', ascending=False).head(10).copy()

    # Label for days inactive
    top_inactive['days_inactive_label'] = top_inactive['days_inactive'].apply(
        lambda x: "Over a year" if x > 365 else f"{x} days"
    )

    # Create horizontal bar chart
    fig = px.bar(
        top_inactive,
        x='days_inactive',
        y='displayLabel',
        orientation='h',
        color='days_inactive',
        text='days_inactive_label',
        labels={'displayLabel': 'User', 'days_inactive': 'Days Inactive'},
        color_continuous_scale='YlGnBu'
    )

    # Aesthetics
    fig.update_layout(
        yaxis=dict(autorange='reversed'),  # largest on top
        margin=dict(t=50, l=150, r=50, b=50)
    )
    # Build the FIG construct to return
    FIG["title"] = "Top 10 Users with Longest Inactivity"
    FIG["data"] = fig
    
    return FIG