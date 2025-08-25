import streamlit as st

from sage.src import dss_funcs
from sage.pages.insights import layout_metrics
from sage.pages.insights import layout_graphs
from sage.pages.insights import layout_explore
from sage.pages.insights import layout_testing


# ------------------------------------------------------------------------------------
# Main function
def main(category, stock_insights, custom_insights):
    data_category = category.lower().replace(" ", "_")
    # Setup base sideba
    st.set_page_config(initial_sidebar_state="expanded")
    st.set_page_config(layout="wide")
    with st.sidebar:
        with st.container(border=True):
            genre = st.selectbox(
                label = "## Select an Insight",
                options = ["Metrics", "Graphs", "Explore DataFrame"],
                index = 0
            )

    # Load the INSIGHTS information
    display_data = []
    modules = {}

    if stock_insights:
        tmp_modules, tmp_display_data = dss_funcs.collect_display_data(stock_insights)
        modules = modules | tmp_modules
        display_data += tmp_display_data
    if custom_insights:
        tmp_display_data, tmp_d = dss_funcs.collect_display_data(custom_insights)
        modules = modules | tmp_modules
        display_data += tmp_display_data
    display_data = sorted(display_data)

    # Display
    st.header(f"Dataiku {category}: {genre}")
    if genre == "Metrics":
        layout_metrics.main(data_category, display_data, modules)
    elif genre == "Graphs":
        layout_graphs.main(data_category, display_data, modules)
    elif genre == "Explore DataFrame":
        layout_explore.main(data_category, display_data, modules)
    elif genre == "idk":
        layout_testing.main(data_category, display_data, modules)
    return