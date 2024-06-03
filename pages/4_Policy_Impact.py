import streamlit as st
import matplotlib.pyplot as plt

from load_data import *
from load_metadata import *
from synth import SyntheticControl

# with st.sidebar:
#     selection = st.radio(
#         "Choose dataset",
#         [d.name for d in DATASETS]
#     )
selection = 'Consumer Spending'

curr_dataset = DATASET_MAP[selection]
st.subheader(curr_dataset.name)
st.caption(curr_dataset.description)
state_data = dataset_to_state_data[selection]

policy = 'first_reopen'
policy_dates = policy_df[lambda df: df[policy]==1].set_index('statename')['date']

col1, col2 = st.columns([2,3], gap='large')
with col1:
    treated = st.selectbox(
        label = 'Estimate impact of reopening for this state',
        options = all_states,
        index = 5)
    treated_dt = policy_dates.get(treated, None)
    
    estimation_days = st.number_input(
        "Estimation period (days after policy for which controls must be valid)",
        min_value=7, max_value=100, value=14)
    buffer_days = st.number_input(
        "Buffer (days before policy to exclude from pre-treatment period)",
        min_value=0, max_value=14, value=1)

# truncate data to pre-period and estimation period
# mask control states when they become treated, drop any with insufficient data
def mask_control(X, starting_dates):
    X = X.copy()
    for col in X.columns:
        mask_start = starting_dates.get(col)
        if mask_start is not None:
            X.loc[mask_start:, col] = np.nan
    return X

data_trunc = state_data.loc[:treated_dt+pd.offsets.Day(estimation_days)]
y = data_trunc[treated]
X = data_trunc.drop(columns=[treated])  # controls
X = mask_control(X, policy_dates-pd.offsets.Day(buffer_days))
X = X.dropna(axis=1, how='any')

n_controls = X.shape[1]
if n_controls < 2:
    st.text(f"Not enough control states for synthetic control ({n_controls})")
else:
    sc = SyntheticControl()
    sc.fit(X.loc[:treated_dt-pd.offsets.Day(buffer_days)], y.loc[:treated_dt-pd.offsets.Day(buffer_days)])

    with col1:
        # visualize set of controls, weights on them
        plt.figure(figsize=(2,1+n_controls*0.5))
        pd.Series(sc.w_, index=X.columns).to_frame('sc_weight').round(2).sort_index(ascending=False)\
            .plot.barh(ylabel='', title='Synthetic control weights')
        st.pyplot(plt.gcf())
        # TODO: compare to uniform weights from paper for select treated states
        # just add another column
    
    with col2:
        show_controls = st.checkbox("Show control series")
        plt.figure(figsize=(8,4))
        pd.Series(sc.predict(X), index=X.index).rename('Synthetic control')\
            .plot(color='k', linewidth=1.5, title=f'{curr_dataset.name}\n{treated} vs synthetic control with {buffer_days}-day buffer')
        y.plot(color='red', linewidth=2, ax=plt.gca())
        if show_controls:
            X.add_prefix('_').plot(color='k', alpha=0.1, ax=plt.gca())
        plt.axvline(x=treated_dt, color='k', linewidth=2, linestyle='--', label=policy)
        plt.axvspan(treated_dt, treated_dt-pd.offsets.Day(buffer_days), color='gray', alpha=0.25, linewidth=0)
        plt.legend()
        st.pyplot(plt.gcf())


st.subheader("Methodology")
with st.expander("Synthetic control method"):
    st.write(r'''
    Let $Y_{it}$ indicate the outcome for state $i$ at time $t$.
    
    Assume the policy is enacted in state 1 at time $T_1$, while states $2, \ldots, J$ have not adopted the policy through time $T_1+h$.
    
    The pre-treatment period is $\{1, \ldots, T_1-1\}$; the post-treatment period is $\{T_1+1, \ldots, T_1+h\}$.
    
    We are interested in the effect of the policy in the post-treatment period:
    ''')
    st.latex(r'''
    \tau_{1t} = Y_{1t} - Y_{1t}^c
    ''')
    st.write(r'''
    where $Y_{1t}^c$ denotes the counterfactual outcome for state 1 at time $t$. We estimate this using the **synthetic control** method:
    ''')
    st.latex(r'''
    \widehat Y_{1t}^c = \sum_{j=2}^J w_j Y_{jt}
    ''')
    st.write(r'''
    We construct a synthetic control for state 1 as a weighted average of the untreated states. 
    The weights are chosen to match the pre-treatment outcomes of state 1 as closely as possible.
    Consider the "placebo" treatment effect $\widehat \tau_{1t}$ in the pre-treatment period.
    The synthetic control minimizes its $\ell_2$ norm:
    ''')
    st.latex(r'''
    \min_w \sum_{t=1}^{T_1-1} \widehat \tau_{it}^2
    \\
    \text{s.t. } \sum_{j=2}^J w_j = 1 \text{ and } w_j \geq 0 \; \forall j
    ''')
    st.write(r'''
    There are many variations on synthetic controls, including
    - regularizing the weights toward uniform
    - relaxing the weight constraints
    - balancing auxiliary covariates
    
    To account for error or slippage in policy effective dates, we have added a buffer $b$ such that the pre-treatment period is truncated to $\{1, \ldots, T_1-1-b\}$. The objective then becomes
    ''')
    st.latex(r'''
    \min_w \sum_{t=1}^{T_1-1-b} \widehat \tau_{it}^2
    ''')

st.subheader("Event study in paper [1]")
with st.expander("Treated and control states"):
    st.image('images/tableA10.png', caption='Treated and control states')

with st.expander("Difference-in-differences estimates of reopening impact"):
    st.image('images/tableA11.png', caption='Estimates of reopening impact')


content = """
### References
- Abadie, A. (2021). Using synthetic controls: Feasibility, data requirements, and methodological aspects. Journal of Economic Literature, 59(2), 391-425.
- Alves, M. (2022). Causal Inference for The Brave and True.
- Ben-Michael, E., Feller, A., & Rothstein, J. (2022). Synthetic controls with staggered adoption. Journal of the Royal Statistical Society Series B: Statistical Methodology, 84(2), 351-381.
"""

st.markdown(content)
