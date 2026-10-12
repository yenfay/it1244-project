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

def load(file):
    file = str(file)
    if file.endswith('txt'):
        return pd.read_csv(file, sep=r'\s+', header=None, names=col_names)
    return pd.read_csv(file)

def txt_to_csv(raw_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for file in sorted(os.listdir(raw_dir)):
        if not file.endswith('.txt'):
            continue
        df = load(os.path.join(raw_dir, file))
        df.to_csv(os.path.join(out_dir, file.replace('.txt', '.csv')), index=False)

def parse_file_name(file):
    # GaCo01_02.txt gives {study: "Ga", group: "Co", subject: "GaCo01", walk: 2}
    file = os.path.basename(str(file))   # also works if given a full path
    pairs = [('study', file[0:2]), ('group', file[2:4]), ('subject', file[0:6]), ('walk', int(file[7:9]))]
    return dict(pairs)

# def splits():

if __name__ == '__main__':
    txt_to_csv(raw_dir, out_dir)

# make_splits(): StratifiedGroupKFold grouped by subject, saved once to splits.json for both tasks. Task 2 folds use only PD patients with UPDRSM, so SiPt02 and SiPt07 are excluded.