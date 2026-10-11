#convert txt to csv with headers. in processed data
import os
import pandas as pd

col_names = (["time"]
        + [f"L{i}" for i in range(1, 9)]
        + [f"R{i}" for i in range(1, 9)]
        + ["L_total", "R_total"])

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   
raw_dir = ROOT / "data" / "raw"
out_dir = ROOT / "data" / "processed"

def txt_to_csv(raw_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for file in os.listdir(raw_dir):
        if not file.endswith(".txt"):
            continue
        df = pd.read_csv(os.path.join(raw_dir, file), sep=r"\s+", header=None, names=col_names)
        df.to_csv(os.path.join(out_dir, file.replace(".txt", ".csv")), index=False)


if __name__ == '__main__':
    txt_to_csv(raw_dir, out_dir)
