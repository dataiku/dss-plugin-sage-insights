import streamlit as st

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.header(f" Welcome")

# Splash
home_pg = st.Page(main, title="Home", icon=":material/login:", default=True)

# Instance Level
#projects = st.Page("pages/projects.py", title="Projects", icon=":material/dashboard:")
users = st.Page("pages/users.py", title="Users", icon=":material/dashboard:")

# Project Level
#datasets = st.Page("pages/datasets.py", title="Datasets", icon=":material/dashboard:")
#recipes = st.Page("pages/recipes.py", title="Recipes", icon=":material/dashboard:")
#scenarios = st.Page("pages/scenarios.py", title="Scenarios", icon=":material/dashboard:")

pg = st.navigation(
    {
        "Sage Insights": [home_pg],
        "Instance Level": [users_pg],
        #"Instance Level": [projects, users],
        #"Project Level": [datasets, recipes, scenarios]
    }
)
pg.run()