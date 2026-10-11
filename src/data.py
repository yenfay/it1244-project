#convert txt to csv with headers. in processed data
import os
import pandas as pd
from pathlib import Path

col_names = (["time"]
        + [f"L{i}" for i in range(1, 9)]
        + [f"R{i}" for i in range(1, 9)]
        + ["L_total", "R_total"])

ROOT = Path(__file__).resolve().parent.parent   
raw_dir = ROOT / "data" / "raw"
out_dir = ROOT / "data" / "processed"

#load(file) returns each walking file as a df
def load(file):
    file = str(file)
    if file.endswith('txt'):
        return pd.read_csv(file, sep=r'\s+', header = None, names=col_names)
    return pd.read_csv(file)

def txt_to_csv(raw_dir, out_dir):
    os.make_dirs(out_dir, exist_ok=True)
    for file in sorted(os.listdir(raw_dir)):
        if not file.endswith('.txt'):
            continue
        df = load(os.path.join(raw_dir, file))
        df.to_csv(os.path.join(raw_dir, file.replace('.txt', '.csv')), index=False)




if __name__ == '__main__':
    txt_to_csv(raw_dir, out_dir)

# load_walk(file): returns the 19 named columns.
# parse_name(file): returns study, group, subject and walk number.
# load_metadata(): applies the §1 fixes, adds a label column (1 = PD), and gives the columns short names.
# list_walks(): one row per file, filtered to normal walks.
# make_splits(): StratifiedGroupKFold grouped by subject, saved once to splits.json for both tasks. Task 2 folds use only PD patients with UPDRSM, so SiPt02 and SiPt07 are excluded.