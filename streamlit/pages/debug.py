import streamlit as st
import dataiku
import tomllib


# load toml config
st.write("### Attempting load custom toml")
path = "../../../../project-lib-resources/api_configs.toml"
with open(path, "rb") as f:
    config_data = tomllib.load(f)
st.write(config_data)


