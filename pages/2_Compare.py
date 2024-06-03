import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

from load_data import *
from load_metadata import *

displayed_by_dataset = {}

with st.sidebar:
    for d in DATASETS:
        displayed_by_dataset[d.name] = st.checkbox(d.name, value=True)

    # allow states to be added to list interactively
    # no comparative timeseries in opportunity explorer
    state_list = st.multiselect(
        label = 'States to compare',
        options = all_states,
        default = ['California', 'Washington', 'Georgia'])

col1, col2 = st.columns(2, gap='medium')
next_col = col1
def toggle_next_col(col):
    if col == col1:
        return col2
    else:
        return col1

max_dt = min([df.index.max() for df in dataset_to_state_data.values()])
for d in DATASETS:
    if displayed_by_dataset[d.name]:
        with next_col:
            st.subheader(d.name)
            st.caption(d.description)
            df = dataset_to_state_data[d.name].loc[:max_dt]
            st.line_chart(
               df[state_list].dropna(how='all').reset_index(), x="Date", y=state_list
            )
            with st.expander("Dataset description from [1]"):
                components.html(dataset_to_doc[d.metadata_id], height=500, scrolling=True)
        next_col = toggle_next_col(next_col)

# why were continuing claims higher in CA? different unemployment policy?
