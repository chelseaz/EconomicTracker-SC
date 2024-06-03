import streamlit as st

st.set_page_config(layout="wide")

content = """
We create a dashboard from public data on economic outcomes published by Chetty et al [1]. The dataset is useful for exploring consumer and employer activity in the wake of COVID. 

Their paper draws [conclusions](https://opportunityinsights.org/wp-content/uploads/2020/06/tracker-summary.pdf) such as:
"High-income individuals **reduced spending** sharply in March 2020, particularly in sectors that require in-person interaction. This reduction in spending greatly **reduced the revenues of small businesses** in affluent, dense areas... **Even though consumer spending and job postings had recovered fully** by December 2021, **employment rates in low-wage jobs remained depressed** in areas that were initially hard hit, indicating that the temporary fall in labor demand led to a persistent reduction in labor supply."

They also provide a dashboard [here](https://tracktherecovery.org/).

The paper estimates the aggregate impacts of state reopening policies.
Our dashboard investigates policy impact in a more granular way - per state, over time.

### References
[1] "The Economic Impacts of COVID-19: Evidence from a New Public Database Built Using Private Sector Data", by Raj Chetty, John Friedman, Nathaniel Hendren, Michael Stepner, and the Opportunity Insights Team. November 2020. Available at: https://opportunityinsights.org/wp-content/uploads/2020/05/tracker_paper.pdf
"""

col1, col2 = st.columns([2,1], gap='medium')
with col1:
    st.header('Economic tracker, Streamlit edition')
    st.markdown(content)
with col2:
    st.image('images/summary_figure3.png', caption='From [1]')
