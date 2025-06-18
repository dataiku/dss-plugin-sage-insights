import tomllib
from sage.streamlit.pages.layouts import layout_main
from sage.src import dss_folder
try:
    from sage.insights import scenarios as dss_objects # change this line
except:
    dss_objects = False

category = "Scenarios" # change this line
data_category = category.lower()
df = dss_folder.read_folder_input(
    folder_name = "base_data",
    path = f"/{data_category}/metadata.csv"
)
with open(".streamlit/.sage_config.toml", "rb") as f:
    config_data = tomllib.load(f)
try:
    config = config_data[data_category]
except:
    config = {}
layout_main.main(category, data_category, dss_objects, df, config)