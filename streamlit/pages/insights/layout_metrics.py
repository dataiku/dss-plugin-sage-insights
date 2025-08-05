import streamlit as st

from sage.src import dss_funcs
from sage.insights.data_structures import display_graph


# ------------------------------------------------------------------------------------
def main(data_category, display_data, modules):
    # load only the metric insights
    insights = []
    for value in display_data:
        if value.split(" ")[0].lower() == "metrics":
            insights.append(value)
    if not insights:
        st.error(f"No {data_category} Metrics to display.")
        return

    # Display
    for key in insights:
        with st.container(border=True):
            module_name = modules[key][0]
            fp = modules[key][1]
            FIGS = dss_funcs.load_insights(module_name, fp)
            if isinstance(FIGS, list):
                ncol = len(FIGS)
                cols = st.columns(ncol, gap="small", border=True)
                for i in range(ncol):
                    with cols[i]:
                        display_graph.main(FIGS[i])
            else:
                FIG = FIGS       
                display_graph.main(FIG)
                
    return