import streamlit as st
import matplotlib.pyplot as plt

from load_data import *
from load_metadata import *

st.subheader("First reopening policy by state")

# Color code relative to date
dt = st.select_slider(
    'Policy implementation date',
    options=policy_df.query("first_reopen==1").date.dt.date.sort_values().unique(),
    value=pd.Timestamp('2020-05-08').date()
)
dtt = pd.Timestamp(dt)

def color_date(d):
    days_elapsed = (d - dtt).days
    if days_elapsed == 0:
        color = 'orange'
    elif days_elapsed < 0:
        # state already implemented
        color = 'white'
    else:
        # state has yet to implement
        color = 'khaki'
    return f'background-color: {color}'

display_df = policy_df.query("first_reopen==1")[['statename', 'date', 'policy_description']]\
    .reset_index(drop=True)\
    .style.applymap(color_date, subset=['date']).format({'date': "{:%Y-%m-%d}"})

st.dataframe(display_df, hide_index=True, use_container_width=True, height=500, column_config={
    'statename': st.column_config.TextColumn("State", width='small'),
    'date': st.column_config.DatetimeColumn("Implementation date", width='small'),
    'policy_description': st.column_config.TextColumn("Policy description", width='large')
})
