import streamlit as st
import pandas as pd

from sage.src import dss_funcs


def body(category, dss_objects, df):
    # -------------------------------------------------------------------------
    # Load the INSIGHTS information
    metrics = []
    charts = []
    top10 = []
    d = dss_funcs.collect_modules(dss_objects)
    for key in d.keys():
        meta, result = dss_funcs.load_insights(d[key][0], d[key][1], df)
        if meta["pass"]:
            if meta["type"] == "metric":
                metrics.append([meta, result])
            elif meta["type"] == "top10":
                top10.append([meta, result])
            else:
                charts.append([meta, result])
        else:
            st.error(result)

    # -------------------------------------------------------------------------
    # Display
    col = st.columns((1, 3, 2), gap='medium', border=True)
    with col[0]:
        st.markdown(f'#### {category} Insights')
        for metric in metrics:
            meta, data = metric
            title = meta['title']
            value = meta["value"]
            delta = meta["delta"]
            if delta:
                st.metric(label=title, value=value, delta=delta)
            else:
                st.metric(label=title, value=value)
    with col[1]:
        for chart in charts:
            meta, data = chart
            title = meta['title']
            st.markdown(f"##### {title}")
            if meta["type"] == "bar":
                st.bar_chart(data, stack=False)
    with col[2]:
        for t10 in top10:
            meta, top10_df = t10
            title = meta['title']
            st.markdown(f"##### {title}")
            st.dataframe(top10_df, hide_index=True)
    return