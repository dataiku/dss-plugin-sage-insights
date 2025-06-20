import streamlit as st


def apple():
    if d:
        # Load Custom Modules
        modules = list(d.keys())
        option = st.selectbox( label = "Select a module", options = modules)
        # Display custom modules
        module_name, fp = d[option]
        results = dss_funcs.load_module(module_name, fp)
        if results[0]:
            st.header(option)
            st.dataframe(results[1])
        else:
            st.write(results[1])
    else:
        st.write(f"No Customer Modules for {category}")

def main(category):
    st.error("Coming Soon in version 1.1")
    return