from sage.streamlit.pages.layouts import layout_main
try:
    from sage.insights import recipes as dss_objects # change this line
except:
    dss_objects = False

category = "Recipes" # change this line
layout_main.main(category, dss_objects)