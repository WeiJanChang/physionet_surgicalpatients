# Dataset Overview

This repository contains a dataset from this source:

## [PhysioNet](https://physionet.org/content/vitaldb/1.0.0/): VitalDB, a high-fidelity multi-parameter vital signs database in surgical patients

This dataset includes patient demographics, medical history, anes/op time, approach, and physiological data.

You can now in here find how to preprocess the data by handling missing values, encoding categorical variables, and
scaling numerical features as necessary.

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

# Data pre-processing

``
clinical_data.py
``

To find out patients with all abnormal_data, please use
`` from src.clinical_data import abnormal_data``

To select all patents who match specific lab data with abnormality, please use
`` from src.clinical_data import select_data``

To find patients based on ASA level
`` from src.clinical_data import select_asa``

To enter patient ID to see abnormal data or see specific abnormal data from df
`` from src.clinical_data import select_pt``

To find out patients with pre-op DM or HTN
`` from src.clinical_data import medical_history``

To calculate average anes and op time in each surgery.
`` from src.clinical_data import anes_op_time``
  

