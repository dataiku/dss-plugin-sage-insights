import streamlit as st
import pandas as pd

from sage.src import dss_funcs


def body(category, dss_objects, df):
    # -------------------------------------------------------------------------
    # Filer on Project Key for some categories
    df_filter = {}
    if category in ["Datasets", "Rcipes", "Scenarios"]:
        project_keys = df.project_key.unique().tolist()
        project_keys = sorted(project_keys)
        project_keys.insert(0, "")
        option = st.selectbox(
            "How would you like to be contacted?",
            project_keys,
        )
        if option:
            df_filter["project_key"] = option

    # -------------------------------------------------------------------------
    # Load the INSIGHTS information
    metrics = []
    charts = []
    d = dss_funcs.collect_modules(dss_objects)
    for key in d.keys():
        meta, result = dss_funcs.load_insights(d[key][0], d[key][1], df, df_filter)
        if meta["pass"]:
            if meta["type"] == "metric":
                metrics.append([meta, result])
            else:
                charts.append([meta, result])
        else:
            st.write(result)

    # -------------------------------------------------------------------------
    # Create 2 columns
    ## Left for single point metrics
    ## Right for tables / Graphs
    col = st.columns((1.5, 4.5), gap='medium', border=True)
    with col[0]:
        st.markdown(f'#### {category} Insights')
        for metric in metrics:
            meta, data = metric
            title = meta['title']
            value = meta["value"]
            delta = meta["delta"]
            st.metric(label=title, value=value, delta=delta)

    with col[1]:
        for chart in charts:
            meta, data = chart
            title = meta['title']
            st.markdown(f"##### {title}")
            if meta["type"] == "bar":
                st.bar_chart(data, stack=False)
    return