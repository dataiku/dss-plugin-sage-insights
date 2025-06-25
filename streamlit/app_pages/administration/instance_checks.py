import streamlit as st
import pandas as pd
import dataiku

# function
def some_output(label):
    tab_filtered = df[df["severity"] == label]
    option = st.selectbox(label="Select a code", options=tab_filtered["code"].unique())
    filtered = tab_filtered[tab_filtered["code"] == option]
    del filtered["code"]
    del filtered["severity"]
    filtered = filtered.drop_duplicates()
    markdown = ""
    for row in filtered.itertuples():
        message = getattr(row, "message")
        detail = getattr(row, "details")
        s = f"""
1. Error Message: {message}
    * {detail}
        """
        markdown += s
    st.markdown(markdown, unsafe_allow_html=True)


# Header
category = "Instance Sanity Checks"
st.title(category)

# Build the sanity check DF
client = dataiku.api_client()
instance_sanity_check = client.perform_instance_sanity_check()
data = []
for msg in instance_sanity_check.messages:
    data.append([
        msg.code,
        msg.severity,
        msg.message,
        msg.details
    ])
df = pd.DataFrame(data, columns=["code", "severity", "message", "details"])
df.loc[df["code"] == "WARN_PROJECT_LARGE_JOB_HISTORY", "severity"] = "ERROR"

# Build the layout
tab_labels = df["severity"].unique().tolist()
tabs = st.tabs(tab_labels)
for label, tab in zip(tab_labels, tabs):
    with tab:
        some_output(label)


