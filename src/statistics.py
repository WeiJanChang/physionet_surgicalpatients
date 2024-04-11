import pandas as pd
from scipy.stats import chi2_contingency
from typing import TypedDict, Optional, List


def chi2(df: pd.DataFrame,
         dependent_var: Optional[List[str]],
         independent_var: Optional[List[str]]):
    """

    :param df: anes_df
    :param dependent_var: binary variable
    :param independent_var: categorical variable
    :return: results of chi square
    """
    contingency_table = pd.crosstab(df[dependent_var], df[independent_var])
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    print("Chi-square statistic:", chi2)
    print("p-value:", p_value)


if __name__ == '__main__':
    anes_df = pd.read_csv("/Users/wei/Documents/physionet_surgicalpatients/clinical_data.csv")
