# -----------------------------------------------------------------------------
import streamlit as st
import sys
sys.dont_write_bytecode = True

# -----------------------------------------------------------------------------
# Setup streamlit configs
st.set_page_config(
    page_title="Dataiku Sage Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Main
home = st.Page("pages/main/home.py", title="Home", default=True)

# -----------------------------------------------------------------------------
# Insights

## Operating System
disk_space = st.Page("pages/insights/disk_space.py", title="Disk Space")

## Dataiku - Main
users = st.Page("pages/insights/users.py", title="Users")

## Dataiku - Project
projects  = st.Page("pages/insights/projects.py",  title="Projects")
datasets  = st.Page("pages/insights/datasets.py",  title="Datasets")
recipes   = st.Page("pages/insights/recipes.py",   title="Recipes")
scenarios = st.Page("pages/insights/scenarios.py", title="Scenarios")

# -----------------------------------------------------------------------------
# Navigation Panel
pages = {
    "Sage Main": [
        home
    ],
    "Operating System": [
        disk_space
    ],
    "Dataiku Insights": [
        users,
        projects,
        datasets,
        recipes,
        scenarios
    ]
}

pg = st.navigation(pages, position="top")
pg.run()
# -----------------------------------------------------------------------------
