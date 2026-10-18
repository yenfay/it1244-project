# reason for using stride: as shown in boxplot in eda, total duration of walk files varies
# reason for using only 01 walks: consistency in walk condition also shown in eda
# reason for using CV instead of Standard deviation to measure irregularity: CV is SD but relative to the average. So basically irregularity relative to each persons pace. Highlighted in reference papers as well.

import numpy as np
import pandas as pd
from src.data import load, load_metadata, list_walks

threshold = 20

def walk_events(force, time):
    on = force.values > threshold
    strikes = time.values[1:][~on[:-1] & on[1:]]
    toe_off = time.values[1:][on[:-1] & ~on[1:]]
    return strikes, toe_off

def stride_times(strikes):
    strides = np.diff(strikes)
    median = np.median(strides)
    return strides[abs(strides - median) <= 0.3 * median]

def swing_times(strikes, toe_off):
    swings = []
    for t in toe_off:
        later = strikes[strikes > t]
        if len(later) > 0:
            swings.append(later[0] - t)
    swings = np.array(swings)
    median = np.median(swings)
    return swings[abs(swings - median) <= 0.3 * median]

def walk_features(walk, weight):
    strides, swings = {}, {}
    for foot in ['L', 'R']:
        strikes, toe_off = walk_events(walk[f'{foot}_total'], walk['time'])
        strides[foot] = stride_times(strikes)
        swings[foot] = swing_times(strikes, toe_off)
    cv = lambda x: x.std() / x.mean()
    swing_L, swing_R = swings['L'].mean(), swings['R'].mean()
    return {
        'stride_time': np.mean([strides['L'].mean(), strides['R'].mean()]),
        'stride_cv': np.mean([cv(strides['L']), cv(strides['R'])]),
        'swing_cv': np.mean([cv(swings['L']), cv(swings['R'])]),
        'swing_asymmetry': abs(swing_L - swing_R) / ((swing_L + swing_R) / 2),
        'peak_force': walk[['L_total', 'R_total']].max().mean() / weight,
    }

metadata = load_metadata().set_index('ID')
rows = {}
for _, w in list_walks().iterrows():
    rows[w['subject']] = walk_features(load(w['file']), metadata.loc[w['subject'], 'Weight (kg)'])

# build table X, contains one row per subject
X = pd.DataFrame.from_dict(rows, orient='index')
y = (metadata.loc[X.index, 'Group'] == 'Pt').astype(int)
