from sage.streamlit.pages.layouts import layout_main
try:
    from sage.insights import datasets as dss_objects # change this line
except:
    dss_objects = False

category = "Datasets" # change this line
layout_main.main(category, dss_objects)