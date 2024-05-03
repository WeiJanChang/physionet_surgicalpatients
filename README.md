# Dataset Overview
This repository contains a dataset from this source:
## [PhysioNet](https://physionet.org/content/vitaldb/1.0.0/): VitalDB, a high-fidelity multi-parameter vital signs database in surgical patients
This dataset includes patient demographics, medical history, anes/op time, approach, and physiological data.

You can now in here find how to preprocess the data by handling missing values, encoding categorical variables, and scaling numerical features as necessary.

# Installation
- Create environment for the required dependencies
```
conda create -n pyphysionet python~=3.9.0
conda activate pyphysionet
cd [CLONED_DIRECTORY]
pip install -r requirements.txt
```
- Buildup the src path
```
conda install conda-build
conda develop src
cd src
```

# Data processing

## Find abnormal data 
```
python clinical_data.py
```

