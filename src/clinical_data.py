"""
pipeline

I. Data Collection and Preprocessing:
    - Gather clinical data from Physionet, including patient demographics, medical history, anes/op time, approach, and physiological data.
    - Preprocess the data by handling missing values, encoding categorical variables, and scaling numerical features as necessary.

V. Visualization and Interpretability:
    - Develop interactive visualizations to provide insights into patient physiological responses during anesthesia.
    - Visualize trends over time, correlations between variables, and patient-specific dashboards for monitoring.
    - Ensure that the visualizations are interpretable and facilitate understanding of the data by healthcare professionals.
"""
import pandas as pd
from typing import Optional, List, Union, Dict
from pathlib import Path
from data_normal_range import DATA_NORMAL_RANGE, extract_values

PathLike = Union[Path, str]
__all__ = ["abnormal_data", "select_data", "select_asa", "select_pt", "medical_history", "anes_op_time"]


def abnormal_data(df: pd.DataFrame, output_path: PathLike = None) -> pd.DataFrame:
    """
    To find out abnormal data from clinical data with crucial info, and save to another df.
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
                output_path: PathLike = None) -> pd.DataFrame:
    """
    enter item to find all patients with the specific data and save to another df
    :param abnormal_df: using function of abnormal_data to get abnormal_df
    :param abnormal_item: item of test
    :param output_path: output path
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


def select_asa(df: pd.DataFrame,
               asa: int = None,
               output_path: PathLike = None) -> pd.DataFrame:
    """
    create a new df based of ASA level
    :param df: anes_df or abnormal_df
    :param asa: asa level
    :param output_path: path
    :return: asa_df
    """
    if asa is not None:
        df['asa'] = df['asa'].fillna(0)  # there have NaN under ['asa']
        asa_mask = df['asa'] == asa
        asa_df = df[asa_mask]
        asa_df['asa'] = asa_df['asa'].astype(int)

        if asa == 0:
            print('Please check the ASA level of your patient')

    if output_path is not None:
        asa_df.to_csv(output_path, index=False)

    return asa_df


def select_pt(abnormal_df: pd.DataFrame,
              patient_id: int = None,
              abnormal_item: Optional[List[str]] = None) -> int:
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


def medical_history(df: pd.DataFrame, htn: bool = False, dm: bool = False) -> pd.DataFrame:
    """
    To find out who has pre-op DM or HTN
    :param df: clinical_data df
    :param htn: patients with hypertension
    :param dm: patients with diabetes
    :return: htn and dm_patients df
    """
    df = df.copy()
    if htn:
        htn_mask: bool = df['preop_htn'] == 1
        htn_pt: pd.DataFrame = df[htn_mask]
        htn_pt.to_csv('htn.csv', index=False)
        return htn_pt
    if dm:
        dm_mask: bool = df['preop_dm'] == 1
        dm_pt: pd.DataFrame = df[dm_mask]
        dm_pt.to_csv('dm.csv', index=False)
        return dm_pt


def anes_op_time(df: pd.DataFrame,
                 op_name: str = None,
                 output_path: PathLike = None) -> pd.DataFrame:
    """
    calculate anesthesia time and operation time and save to a new file.
    calculate average anes and op time in each surgery and save to a new file.
    :param df: anes_df
    :param op_name: surgery name
    :param output_path: path
    :return: time_df
    """
    df['total anesthesia time (hrs)'] = df.apply(lambda x: (x['aneend'] - x['anestart']) / 60, axis=1)  # hours
    df['total surgery time (hrs)'] = df.apply(lambda x: (x['opend'] - x['opstart']) / 60, axis=1)  # hours
    op_names = df['opname']
    average_anes = (df.groupby(op_names).apply(lambda x: x['total anesthesia time (hrs)'].mean())).to_frame()
    average_op = (df.groupby(op_names).apply(lambda x: x['total surgery time (hrs)'].mean())).to_frame()
    average_time_df = average_anes.merge(average_op, on="opname")
    average_time_df = average_time_df.rename(columns={'0_x': 'average_anes_time(hrs)', '0_y': 'average_op_time(hrs)'})
    average_time_df.to_csv('average_surgery_time.csv')

    if op_name is not None:
        op_name_mask = df['opname'] == op_name
        time_df = df[op_name_mask]

    if output_path is not None:
        time_df.to_csv(output_path, index=False)

    return time_df
