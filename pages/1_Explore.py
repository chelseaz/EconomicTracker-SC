import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px

from load_data import *
from load_metadata import *

with st.sidebar:
    selection = st.radio(
        "Choose dataset",
        [d.name for d in DATASETS]
    )

curr_dataset = DATASET_MAP[selection]
st.subheader(curr_dataset.name)
st.caption(curr_dataset.description)

df = dataset_to_state_data[selection]
max_value = df.abs().max().max()

col1, _ = st.columns([2,1])
with col1:
    dt = st.select_slider(
        'Choose date',
        options=df.index.date,
        value=df.index.date.max()
        # TODO: keep slider value when selection changes
    )
    dtt = pd.Timestamp(dt)
    
    colname = dtt.strftime('%Y-%m-%d')
    data_on_date = df.loc[dtt].rename(colname)
    data_on_date = state_ids.join(data_on_date, on='statename')\
        .rename(columns = {'stateabbrev': 'state'})
    
    fig = px.choropleth(
        data_on_date,
        locationmode = 'USA-states', # set of locations match entries in `locations`
        locations='state',
        color=colname,
        color_continuous_scale='RdBu',
        range_color=(-max_value, max_value),
        scope='usa')
    st.plotly_chart(fig)
    # https://arilamstein.com/blog/2024/03/03/creating-interactive-choropleths-with-streamlit/
    
    with st.expander("Dataset description from [1]"):
        components.html(dataset_to_doc[curr_dataset.metadata_id], height=500, scrolling=True)
