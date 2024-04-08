"""
pipeline

I. Data Collection and Preprocessing:
    - Gather clinical data from physionet, including patient demographics, medical history, anes/op time, approach, and physiological data.
    - Preprocess the data by handling missing values, encoding categorical variables, and scaling numerical features as necessary.

II. Predictive Modeling:
    - Split the preprocessed data into training and testing sets.
    - Train predictive models for each task:
        - Predicting risk of complications during surgery.
        - Predicting recovery times.
        - Predicting likelihood of specific post-operative conditions.
        - Predicting anesthesia dosage requirements.
        - Evaluate the models using appropriate metrics and cross-validation techniques.

III. Time Series Analysis:
    - Perform time series analysis on the physiological data collected during anesthesia and surgery.
    - Analyze trends, seasonal patterns, correlations, and variability in the time series data.
    - Use techniques such as dynamic time warping, forecasting, change point detection, and correlation analysis.

IV. Decision Support Systems:
    - Integrate predictive models and time series analysis results into decision support systems.
    - Provide real-time feedback on patient status based on intraoperative data.
    - Suggest appropriate interventions or adjustments during surgery.
    - Recommend optimal anesthesia dosages based on patient characteristics and procedure details.

V. Visualization and Interpretability:
    - Develop interactive visualizations to provide insights into patient physiological responses during anesthesia.
    - Visualize trends over time, correlations between variables, and patient-specific dashboards for monitoring.
    - Ensure that the visualizations are interpretable and facilitate understanding of the data by healthcare professionals.

VI. Model Deployment and Monitoring:
    - Deploy the predictive models and decision support systems into production environments.
    - Monitor the performance of the deployed models and systems, and update them as necessary based on feedback and new data.
"""
import collections

import pandas as pd
from typing import TypedDict, Any, NamedTuple, Optional, List, Union, Tuple, Dict
from pathlib import Path
from data_normal_range import DATA_NORMAL_RANGE

PathLike = Union[Path, str]


# todo: 寫一個fun 指定的病人/ 拿一群病人 拿病人的某個異常值

class AnesDict(TypedDict):
    caseid: str
    subjectid: str  # de-identified hospital ID of patient
    casestart: int  # sec
    caseend: int  # sec
    anestart: int  # sec, from casestart
    aneend: int  # sec, from casestart
    opstart: int  # sec, from casestart
    opend: int  # sec, from casestart
    adm: int  # sec, admission time from casestart
    dis: int  # sec, discharge time from casestart
    icu_days: int
    death_inhosp: int  # in-hospital mortality
    age: int
    sex: str
    height: int  # cm
    weight: int  # kg
    bmi: int  # kg/m2
    asa: int  # ASA classification
    emop: int  # binary, emergency operation
    department: str  # surgical depart.
    optype: str
    dx: str
    opname: str
    approach: str
    position: str
    ane_type: str
    preop_htn: int  # binary
    preop_dm: int  # binary
    preop_ecg: str
    preop_pft: str  # pulmonary function
    preop_hb: int  # g/dL
    preop_plt: int  # x1000/mcL
    preop_pt: int  # %
    preop_aptt: int  # sec
    preop_na: int  # mmol/L
    preop_k: int  # mmol/L
    preop_gluc: int  # mg/dL
    preop_alb: int  # g/dL
    preop_ast: int  # IU/L
    preop_alt: int  # IU/L
    preop_bun: int  # mg/dL
    preop_cr: int  # mg/dL
    preop_ph: int
    preop_hco3: int  # mmol/L
    preop_be: int  # mmol/L
    preop_pao2: int  # mmHg
    preop_paco2: int  # mmHg
    preop_sao2: int  # %
    cormack: str  # Cormack's grade
    airway: str  # airway toute
    tubesize: int
    dltubesize: str  # double lumen tube size
    lmasize: int  # LMA size
    iv1: str
    iv2: str
    aline1: str
    aline2: str
    cline1: str
    cline2: str
    intraop_ebl: int  # estimated blood loss, ml
    intraop_uo: int  # urine output, ml
    intraop_rbc: int  # RBC transfusion, Unit
    intraop_ffp: int
    intraop_ctystalloid: int  # ml
    intraop_colloid: int  # ml
    intraop_ppf: int  # propofol bolus, mg
    intraop_mdz: int  # midazolam, mg
    intraop_ftn: int  # fentanyl, mcg
    intraop_rocu: int  # Rocuronium, mg
    intraop_vecu: int  # Vecuronium, mg
    intraop_eph: int  # Ephedrine, mg
    intraop_phe: int  # Phenylephrine, mcg
    intraop_epi: int  # Epinephrine, mcg
    intraop_ca: int  # Calcium chloride, mg


def abnormal_data(df: pd.DataFrame, output_path: PathLike) -> pd.DataFrame:
    """
    To find out abnormal data from file of clinical data with crucial info, and save to another df.
    :param df:  clinical_data df
    :param output_path: path
    :return: abnormal_data df
    """
    abnormal_data_list: List[Dict[str, any]] = []
    for index, row in df.iterrows():
        abnormal_row = False
        abnormal_value = {}
        for k, v in DATA_NORMAL_RANGE.items():
            data = row[k]
            if not pd.isnull(data):
                if isinstance(v, tuple) and not (v[0] <= data <= v[1]):
                    abnormal_row = True
                    abnormal_value[k] = data

        if abnormal_row:
            abnormal_data_list.append({"patient_id": row['subjectid'],
                                       "age": row["age"],
                                       "gender": row["sex"],
                                       "height": row['height'],
                                       "weight": row['weight'],
                                       "diagnosis": row['dx'],
                                       "opname": row['opname'],
                                       "procedure": row['approach'],
                                       "anes": row['ane_type'],
                                       "ASA": row["asa"],
                                       "abnormal_data": abnormal_value})

    abnormal_df = pd.DataFrame(abnormal_data_list)

    if output_path is not None:
        abnormal_df.to_csv(output_path, index=False)

    return abnormal_df


def medical_history(df: pd.DataFrame, htn_path: PathLike, dm_path: PathLike) -> pd.DataFrame:
    """
    To find out who has pre-op DM or HTN
    :param df: clinical_data df
    :param htn_path: path
    :param dm_path: path
    :return: htn and dm_patients df
    """
    df = df.copy()
    htn_mask: pd.Series[bool] = df['preop_htn'] == 1
    dm_mask: pd.Series[bool] = df['preop_dm'] == 1
    htn_pt: pd.DataFrame = df[htn_mask]
    dm_pt: pd.DataFrame = df[dm_mask]

    if htn_path is not None:
        htn_pt.to_csv(htn_path, index=False)
    if dm_path is not None:
        dm_pt.to_csv(dm_path, index=False)

    return htn_pt, dm_pt


if __name__ == '__main__':
    anes_df = pd.read_csv("/Users/wei/Documents/physionet_surgicalpatients/clinical_data.csv")
    # output_path = 'pt_abnormal_data.csv'
    # abnormal_df = abnormal_data(anes_df, output_path)
    htn_path = 'htn_patients.csv'
    dm_path = 'dm_patients.csv'
    medical_history(anes_df, htn_path=htn_path, dm_path=dm_path)

