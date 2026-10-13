import os
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

col_names = (["time"]
        + [f"L{i}" for i in range(1, 9)]
        + [f"R{i}" for i in range(1, 9)]
        + ["L_total", "R_total"])

ROOT = Path(__file__).resolve().parent.parent
raw_dir = ROOT / "data" / "raw"
out_dir = ROOT / "data" / "processed"
metadata_dir = ROOT/ 'data' / 'others' / "subject_metadata.xls"

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

#used for k-fold cross validation (Task 1)

import json
from sklearn.model_selection import train_test_split, StratifiedKFold

def splits():
    # decides once which subjects are test/which go in each CV fold
    metadata = load(metadata_dir)   # metadata_clean.csv, one row per subject
    tasks = {
        "task1": metadata,                                                          # all 165 subjects
        "task2": metadata[(metadata["label"] == 1) & metadata["UPDRSM"].notna()],   # 91 PD with UPDRSM
    }
    result = {}
    for task, df in tasks.items():
        # what to keep balanced in every part: study + group for Task 1 (e.g. "GaCo"), study for Task 2
        strata = df["Study"] + df["Group"] if task == "task1" else df["Study"]

        # 20% of subjects held out as the test set
        train_ids, test_ids, train_strata, _ = train_test_split(
            df["ID"], strata, test_size=0.2, stratify=strata, random_state=1)

        # remaining 80% cut into 5 folds; each round, one fold validates and four train
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)
        folds = []
        for tr, val in skf.split(train_ids, train_strata):
            folds.append({"train": train_ids.iloc[tr].tolist(),
                          "val": train_ids.iloc[val].tolist()})

        result[task] = {"test": test_ids.tolist(), "folds": folds}

    with open(ROOT / "data" / "splits.json", "w") as f:
        json.dump(result, f, indent=2)

if __name__ == '__main__':
    txt_to_csv(raw_dir, out_dir)

# make_splits(): StratifiedGroupKFold grouped by subject, saved once to splits.json for both tasks. Task 2 folds use only PD patients with UPDRSM, so SiPt02 and SiPt07 are excluded.