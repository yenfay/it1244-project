# IT1244 Project: Parkinsonian Gait (Group 8)

- **Task 1:** classify Parkinson's disease (PD) vs control from gait features.
- **Task 2:** predict PD severity (UPDRSM, plus Hoehn & Yahr and UPDRS) from gait.

## Project structure
```
data/raw/                  walk files (.txt), others/subject_metadata.xls
data/splits.json           fixed test set and 5 CV folds (do not edit)
src/                       data loading (data.py), features (features.py), models (models/)
notebooks/                 eda, task1_classification, task2_severity, results
presentation_material/     saved predictions, model weights and result tables
references_material/       the stuff we cite in our report
```

## 1. Set up the environment
Requires **Python 3.12**. From the project root folder:

```bash
python3.12 -m venv .venv
source .venv/bin/activate        
pip install -r requirements.txt
```

Check the version with `python --version` (it should show 3.12.x). (best for CNN modelling)

## 2. Select the kernelgit 
Open the project folder in VS Code (or Jupyter). In every notebook, choose the `.venv (Python 3.12.x)` kernel:
- **VS Code:** click the kernel name (top right) → Select Another Kernel → Python Environments → `.venv`.

## 3. Run the notebooks
Run them in this order. For each one, use **Restart** and then **Run All**:

1. `notebooks/eda.ipynb`: data checks and the reasoning behind the cleaning and features
2. `notebooks/task1_classification.ipynb`: trains Task 1 models and saves predictions and weights
3. `notebooks/task2_severity.ipynb`: trains Task 2 models and saves predictions and weights
4. `notebooks/results.ipynb`: evaluates all saved predictions (validation and test set)

Notes:
- `data/processed/` is created automatically the first time a notebook runs.
- Running notebooks 2 and 3 overwrites the files in `presentation_material/task1` and `presentation_material/task2`. To see our results without retraining, run only `results.ipynb`.
- Random seeds are fixed. CNN results may still differ slightly across machines.

## Outputs
| Folder | Contents |
|---|---|
| `presentation_material/task*/predictions/` | validation (per fold) and test predictions |
| `presentation_material/task*/weights/` | trained models: `.joblib` (load with `joblib.load`), `.keras` (load with `tf.keras.models.load_model`) |
| `presentation_material/results/` | summary tables and figures |