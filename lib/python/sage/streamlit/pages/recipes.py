from sage.streamlit.pages.layouts import layout_main
from sage.src import dss_folder
try:
    from sage.insights import recipes as dss_objects # change this line
except:
    dss_objects = False

category = "Recipes" # change this line
data_category = category.lower()
df = dss_folder.read_folder_input(
    folder_name = "base_data",
    path = f"/{data_category}/metadata.csv"
)
layout_main.main(category, data_category, dss_objects, df)