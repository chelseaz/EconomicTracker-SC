import streamlit as st

content = """
## Future work

#### Data
- Explore relationships between outcomes and state-level covariates
  - Population change
  - Partisanship
  - Hospitalization rate
- Explore outcomes at finer geographic levels (city, county) and subgroup level
- Collect data on other policies of interest
- Establish a pipeline to update data daily

#### Inference
- More advanced synthetic control that balances auxiliary covariates
- Systematically detect when pre-treatment fit is inadequate
- Permutation test swapping treated and control states
- Average treatment effect in the staggered adoption setting
- Export all analyses to csv; correct for multiple testing

#### Usability
- Propagate choice of state between pages with session state
"""

st.markdown(content)
