# PTB-XL MI Data Pipeline

A pure-Python data pipeline (no pandas/NumPy) that streams Myocardial
Infarction (MI) patient records from the PTB-XL ECG clinical metadata
without loading the full dataset into memory.

## What it demonstrates
- **Generators**: `mi_patient_streamer` yields matching records lazily
- **Decorators**: `@timer` (with `functools.wraps`) times a function
- **Lambda, filter(), map(), min()**: lazy filtering and summarizing

## Dataset
PTB-XL ECG Database from PhysioNet. Download `ptbxl_database.csv` and
`scp_statements.csv` and place them next to the script.

## Run
python main.py

## Sample output
Loaded 9 MI-related diagnostic codes.
ID 9796 | Age 70 | lateral myocardial infarction
...
