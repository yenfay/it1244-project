import os
import json
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split, StratifiedKFold

col_names = (["time"]
        + [f"L{i}" for i in range(1, 9)]
        + [f"R{i}" for i in range(1, 9)]
        + ["L_total", "R_total"])

ROOT = Path(__file__).resolve().parent.parent
raw_dir = ROOT / "data" / "raw"
metadata_dir = ROOT/ 'data' / 'others' / "subject_metadata.xls"

def load(file):
    file = str(file)
    if file.endswith('txt'):
        return pd.read_csv(file, sep=r'\s+', header=None, names=col_names)
    return pd.read_csv(file)

def parse_file_name(file):
    # GaCo01_02.txt gives {study: "Ga", group: "Co", subject: "GaCo01", walk: 2}
    file = os.path.basename(str(file))   # also works if given a full path
    pairs = [('study', file[0:2]), ('group', file[2:4]), ('subject', file[0:6]), ('walk', int(file[7:9]))]
    return dict(pairs)

def load_metadata():
    metadata = pd.read_excel(metadata_dir)
    metadata = metadata.drop(metadata[(metadata['Study'] == 'Ju') & (metadata['Group'] == 'CO') & (metadata['Subjnum'] == 10)].index)
    metadata.loc[metadata['Study'] == 'Ju', 'Height (meters)'] /= 100
    metadata['Group'] = metadata['Group'].replace({'PD': 'Pt', 'CO': 'Co'})
    return metadata.reset_index(drop=True)

def list_walks():
    files = sorted(f for f in os.listdir(raw_dir) if f.endswith('_01.txt'))
    return pd.DataFrame([{'file': str(raw_dir / f), **parse_file_name(f)} for f in files])

#used for k-fold cross validation (Task 1)

def splits():
    # decides once which subjects are test/which go in each CV fold
    metadata = load_metadata()   # one row per subject
    tasks = {
        "task1": metadata,                                                          # all 165 subjects
        "task2": metadata[(metadata["Group"] == 'Pt') & metadata["UPDRSM"].notna()],   # 91 PD with UPDRSM
    }
    result = {}
    for task, df in tasks.items():
        # study for Task 2 only cos only Pt so group is same
        strata = df["Study"] + df["Group"] if task == "task1" else df["Study"]

        # 20% of subjects held out as the test set
        # from sklearn docs: X_train, X_test, y_train, y_test = train_test_split(X, y)
        train_ids, test_ids, train_strata, _ = train_test_split(
            df["ID"], strata, test_size=0.2, stratify=strata, random_state = 1)

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
    splits()

