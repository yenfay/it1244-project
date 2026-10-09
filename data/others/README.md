# Gait Dataset Documentation

## Overview and Problem Statement
People with Parkinson's disease often exhibit something called Parkinsonian gait. In this project you are tasked with two problems:
1. Determine whether someone has Parkinson's based on the properties of their gait.
2. Assess the severity of their Parkinson's based on their gait and any other additional metadata you see fit.
To achieve this, you are provided with the following:
Gait profiles of different patients ([Study][Group][SubjectID]_[WalkNumber].tx)
Metadata of test subjects (subject_metadata.xls.)

## Dataset File Naming Convention

Dataset files follow the format: `[Study][Group][SubjectID]_[WalkNumber].txt` The naming convention is described below whereas the data format description can be found in format.txt

Example: `GaCo01_02.txt`

### Study Code (2 letters)
Study source identifier (Ga, Ju, or Si)

### Subject Group (2 letters)
- `Co` : Control subject (healthy)
- `Pt` : Patient (Parkinson's Disease)

### Subject ID (2 digits)
Sequential numbering within each study-group combination (01, 02, 03, ...)

### Walk Number (2 digits after underscore)

**Ga Study (Dual-tasking)**
- `01` : Normal walking (baseline)
- `02-09` : Additional normal walking trials
- `10` : Dual-task (serial-7 subtraction while walking)

**Ju Study (Rhythmic Auditory Stimulation)**
- `01` : Baseline (no auditory cue)
- `02-06` : Various RAS conditions

**Si Study (Treadmill)**
- `01-06` : Various treadmill speeds/conditions

### Examples

| Filename | Interpretation |
|----------|----------------|
| `GaCo01_01.txt` | Ga study, Control subject #1, Normal walk |
| `GaCo01_10.txt` | Ga study, Control subject #1, Dual-task walk |
| `JuPt03_02.txt` | Ju study, PD Patient #3, Walk condition #2 |
| `SiCo15_04.txt` | Si study, Control subject #15, Walk condition #4 |


## Metadata File

File: `subject_metadata.xls`

### Columns

**Study**
Study source identifier (Ga, Ju, or Si)

**Group**
Subject group: Co (Control) or Pt (Patient)

**Subjnum**
Subject number within each study-group combination

**Gender**
Biological sex (M or F)

**Age**
Age in years at time of data collection

**Height (meters)**
Subject height in meters

**Weight (kg)**
Subject body mass in kilograms

**HoehnYahr**
Hoehn and Yahr scale for PD disease staging (0-5, NULL for controls)

**UPDRS**
Unified Parkinson's Disease Rating Scale total score (NULL for controls)

**UPDRSM**
UPDRS Part III Motor examination score (NULL for controls)

**TUAG**
Timed Up and Go test in seconds

**Speed_01 (m/sec)**
Average gait speed during normal walking (walk 01)

**Speed_10 (m/sec)**
Average gait speed during dual-task walking (walk 10, Ga study only)

## Suggestions & Comments
Here we shall provide some directions to help kickstart your project. Nevertheless, you are not required to answer these questions and encouraged to explore other questions that might be interesting to you.


In the first task, you are simply required to classify patient based on the presence/absence of Parkinson's disease; this in itself should be a relatively simple task. Nevertheless, we are provided with a large amount of data and using all these features might not be necessary.
Is there a way to engineer one/ a few feature/s that would be sufficient to predict the presence of Parkinson's? You are encouraged to look into the characteristics of Parkinsonian's gait to attempt and find a suitable metric.

In the second task, there are several metrics that you could predict. (e.g., UPDRSM, HoehnYahr) Is there a metric that your model could predict much better than others? Why is that so? You are encouraged to determine how these metrics quantify the severity of Parkinson's

