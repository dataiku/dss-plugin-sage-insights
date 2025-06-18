import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import dataiku

st.title('Hello Streamlit!')

# This loads dummy data into a dataframe
df = pd.DataFrame({
    'Trial A': np.random.normal(0, 0.8, 1000),
    'Trial B': np.random.normal(-2, 1, 1000),
    'Trial C': np.random.normal(3, 2, 1000)
})

# Uncomment the following to read your own dataset
#dataset = dataiku.Dataset("YOUR_DATASET_NAME_HERE")
#df = dataset.get_dataframe()

c = alt.Chart(df).transform_fold(
    ['Trial A', 'Trial B', 'Trial C'], 
    as_=['Experiment', 'Measurement']
).mark_bar(
    opacity=0.3, 
    binSpacing=0
).encode(
    alt.X('Measurement:Q', bin=alt.Bin(maxbins=100)), 
    alt.Y('count()', stack=None), 
    alt.Color('Experiment:N')
)

st.altair_chart(c, use_container_width=True)
