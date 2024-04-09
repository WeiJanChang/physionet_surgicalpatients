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
from data_normal_range import DATA_NORMAL_RANGE, extract_values

PathLike = Union[Path, str]


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


def abnormal_data(df: pd.DataFrame, output_path: PathLike = None, ) -> pd.DataFrame:
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
                if (isinstance(v, tuple) and not (v[0] <= data <= v[1])
                        and data not in ['Normal Sinus Rhythm', 'Normal']):
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
    abnormal_df[['preop_ecg', 'preop_pft', 'preop_hb', 'preop_plt', 'preop_pt', 'preop_aptt', 'preop_na', 'preop_k',
                 'preop_gluc', 'preop_alb', 'preop_ast', 'preop_alt', 'preop_bun', 'preop_cr', 'preop_ph', 'preop_hco3',
                 'preop_be', 'preop_pao2', 'preop_paco2', 'preop_sao2']] = abnormal_df['abnormal_data'].apply(
        lambda x: pd.Series(extract_values(x)))

    if output_path is not None:
        abnormal_df.to_csv(output_path, index=False)

    return abnormal_df


def select_data(abnormal_df: pd.DataFrame,
                abnormal_item: Optional[List[str]] = None,
                output_path: PathLike = None, ) -> pd.DataFrame:
    """
    enter item to find all patients with the specific data and save to another df
    :param abnormal_df:
    :param abnormal_item:
    :return: group_df
    """
    if abnormal_item is not None:
        items = {key: value for key, value in DATA_NORMAL_RANGE.items()}.keys()
        items_list = list(items)
        if abnormal_item in items_list:
            selected_data = abnormal_df.groupby(abnormal_item).apply(lambda x: x)
            group_df = selected_data.dropna(axis=1)
        else:
            raise ValueError(
                f'abnormal items {abnormal_item} not in this patient data, please check{items_list}')

    if output_path is not None:
        group_df.to_csv(output_path, index=False)

    return group_df


def select_pt(abnormal_df: pd.DataFrame,
              patient_id: int = None,
              abnormal_item: Optional[List[str]] = None, ) -> int:
    """
    enter patient ID to see abnormal data or see specific abnormal data from abnormal_df

    :param abnormal_df: patients with abnormal data
    :param patient_id: unique patient id
    :param abnormal_item: select specific item from a patient ID
    :return: data of the item
    """
    if patient_id is not None:
        patient_id_list = abnormal_df['patient_id'].tolist()
        if patient_id in patient_id_list:
            patient_id = abnormal_df['patient_id'] == patient_id
            selected_pt = abnormal_df[patient_id]
            if abnormal_item is not None:
                items = {key: value for key, value in DATA_NORMAL_RANGE.items()}.keys()
                items_list = list(items)
                if abnormal_item in items_list:
                    selected_pt = selected_pt.dropna(axis=1)
                    selected_pt = selected_pt[abnormal_item]
                else:
                    selected_pt = selected_pt.dropna(axis=1)
                    abnormal_items = list(selected_pt.columns[11:])
                    raise ValueError(
                        f'abnormal items {abnormal_item} not in this patient data, please check{abnormal_items}')
        else:
            raise ValueError(f'Patient ID {patient_id} not in the patient list, please recheck patient IDs')
    else:
        raise ValueError("Patient ID cannot be None")

    return selected_pt


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
    abnormal_df = abnormal_data(anes_df)
    # htn_path = 'htn_patients.csv'
    # dm_path = 'dm_patients.csv'
    # medical_history(anes_df, htn_path=htn_path, dm_path=dm_path)
    select_df = select_pt(abnormal_df, 5955, "preop_k")
    output_path = 'group.csv'
    group_df = select_data(abnormal_df, "preop_na", output_path=output_path)
