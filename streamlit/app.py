# -----------------------------------------------------------------------------
import streamlit as st
import sys
sys.dont_write_bytecode = True

# Initialization
if "initialize" not in st.session_state:
    st.session_state["initialize"] = True

if st.session_state.initialize:
    from sage.src import dss_duck
    dss_duck.initialize_duckdb()
    
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
# Platform Insights

## Operating System
disk_space = st.Page("pages/insights/disk_space.py", title="Disk Space")

## Dataiku - Client
users = st.Page("pages/insights/users.py", title="Users")

## Dataiku - Project
projects  = st.Page("pages/insights/projects.py",  title="Projects")
datasets  = st.Page("pages/insights/datasets.py",  title="Datasets")
recipes   = st.Page("pages/insights/recipes.py",   title="Recipes")
scenarios = st.Page("pages/insights/scenarios.py", title="Scenarios")

# -----------------------------------------------------------------------------
# Usage Patterns

## GEN AI / LLM
genai_llm = st.Page("pages/usage_patterns/genai_llm.py", title="GEN AI / LLM")

# -----------------------------------------------------------------------------
# Navigation Panel
pages = {
    "Sage Main": [
        home
    ],
    "Operating System": [
        disk_space
    ],
    "Platform Insights": [
        users,
        projects,
        datasets,
        recipes,
        scenarios
    ],
    "Usage Patterns": [
        genai_llm
    ]
}

pg = st.navigation(pages, position="top")
pg.run()
# -----------------------------------------------------------------------------
