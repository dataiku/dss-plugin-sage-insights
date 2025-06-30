import streamlit as st

def main(data):
    if not data:
        return

    if not data["pass"]:
        return

    if data["title"]:
        st.title(data["title"])

    # Display different types of metrics
    if data["type"] == "metric":
        st.metric(data["label"], data["data"], delta=data["delta"], delta_color="normal", help=None, label_visibility="visible", border=False, width="stretch")
    
    # Display different types of charts
    if data["type"] == "bar_chart":
        st.bar_chart(data=data["data"], x=data["x"], y=data["y"], x_label=data["x_label"], y_label=data["y_label"], color=None, horizontal=data["horizontal"], stack=data["stack"], width=None, height=None, use_container_width=True)
    
    # EOF
    return