import numpy as np
import pandas as pd

from common import *

# Downloaded from https://github.com/OpportunityInsights/EconomicTracker
data_path = 'EconomicTracker/data'

city_ids = pd.read_csv(f'{data_path}/GeoIDs - City.csv')
county_ids = pd.read_csv(f'{data_path}/GeoIDs - County.csv')
state_ids = pd.read_csv(f'{data_path}/GeoIDs - State.csv')
all_states = state_ids.statename

def with_date(df, year_col='year', month_col='month', day_col='day'):
    return df.assign(Date = df.apply(lambda row: pd.Timestamp(year=row[year_col], month=row[month_col], day=row[day_col]), axis=1))

affinity_state = pd.read_csv(f'{data_path}/Affinity - State - Daily.csv')
affinity_state = affinity_state.pipe(with_date)\
    .join(state_ids.set_index('statefips'), on='statefips')\
    .replace('.', np.nan)\
    .set_index('Date')

# note daily freq until mid-2022
# affinity_state.groupby(['year', 'freq']).count()
spend_state_wide = affinity_state.set_index('statename', append=True).spend_all.astype(float)\
    .unstack().reindex(columns=all_states)\
    .dropna(how='all')

emp_state = pd.read_csv(f'{data_path}/Employment - State - Weekly.csv')
emp_state = with_date(emp_state, day_col='day_endofweek')\
    .join(state_ids.set_index('statefips'), on='statefips')\
    .replace('.', np.nan)\
    .set_index('Date')

emp_state_wide = emp_state.set_index('statename', append=True).emp.astype(float)\
    .unstack().reindex(columns=all_states)\
    .dropna(how='all')

ui_state = pd.read_csv(f'{data_path}/UI Claims - State - Weekly.csv')
ui_state = with_date(ui_state, day_col='day_endofweek')\
    .join(state_ids.set_index('statefips'), on='statefips')\
    .replace('.', np.nan)\
    .set_index('Date')

# TODO: coalesce with initclaims_rate_combined, contclaims_rate_combined
initclaims_rate_state_wide = ui_state.set_index('statename', append=True).initclaims_rate_regular.astype(float)\
    .unstack().reindex(columns=all_states)\
    .dropna(how='all')
contclaims_rate_state_wide = ui_state.set_index('statename', append=True).contclaims_rate_regular.astype(float)\
    .unstack().reindex(columns=all_states)\
    .dropna(how='all')

dataset_to_state_data = {
    'Consumer Spending': spend_state_wide,
    'Employment': emp_state_wide,
    'Initial Unemployment Claims': initclaims_rate_state_wide,
    'Continued Unemployment Claims': contclaims_rate_state_wide
}


policy_df = pd.read_csv(f'{data_path}/Policy Milestones - State.csv')
policy_df['date'] = pd.to_datetime(policy_df['date'])

reopen_df = policy_df[lambda df: df.policy_description.str.contains('reopen') | 
    (df.statename=='South Dakota') & (df['date'] == '2020-04-29')].copy()
reopen_df['first_dt'] = reopen_df.groupby('statename').date.transform('min')

# First policy per state with 'reopen' in description
policy_df.loc[reopen_df[lambda df: df.date == df.first_dt].index, 'first_reopen'] = 1
policy_df['first_reopen'] = policy_df['first_reopen'].fillna(0).astype(int)
