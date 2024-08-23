import pandas as pd
from scipy.stats import chi2_contingency
from typing import TypedDict, Optional, List
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def chi2(df: pd.DataFrame,
         dependent_var: Optional[List[str]],
         independent_var: Optional[List[str]]):
    """
    to check if two categorical variables are related or independent.
    
    death_inhosp [0/1] ~ sex [M/F] /asa[0~6]/opname/preop_htn [0/1]/preop_dm [0/1]/emop [0/1]
    :param df: anes_df
    :param dependent_var: binary variable
    :param independent_var: categorical variable
    :return: results of chi square
    """
    contingency_table = pd.crosstab(df[dependent_var], df[independent_var])
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    print(contingency_table)
    print("Chi-square statistic:", chi2)
    print("p-value:", p_value)


def linear_regression(df: pd.DataFrame,
                      dependent_var: Optional[List[str]],
                      independent_var: Optional[List[str]]):
    """
    # TODO: （icu_days: int） 跟 asa:int, age:int, gender:str, anes_time:float, op_time:float, op_name:str,有無關聯
    # linear regression: icu_days /age,anes_time,op_time.
    # binary logistic regression: death_inhosp /, age,anes_time, op_time, op_name
    # anes_time = anes_df['total anesthesia time (hrs)'].values.reshape(-1, 1)
    # anes_df['asa'] = anes_df['asa'].fillna(int(anes_df['asa'].mean()))
    # asa = anes_df['asa'].values.reshape(-1, 1)  # independent variable

    :param df:
    :param dependent_var:
    :param independent_var:
    :return:
    """
    dep_var = df[dependent_var].values.reshape(-1, 1)
    indep_var = df[independent_var].values.reshape(-1, 1)
    lr = LinearRegression()
    lr.fit(indep_var, dep_var)
    var_pred = lr.predict(indep_var)
    plt.scatter(indep_var, dep_var)
    plt.plot(dep_var, var_pred, color='red')
    plt.xlabel(independent_var)
    plt.ylabel(dependent_var)
    plt.title(f'Linear Regression: {dependent_var} vs {independent_var}')
    plt.show()


if __name__ == '__main__':
    anes_df = pd.read_csv("/Users/wei/Documents/physionet_surgicalpatients/clinical_data.csv")
    anes_df['total anesthesia time (hrs)'] = anes_df.apply(lambda x: (x['aneend'] - x['anestart']) / 60,
                                                           axis=1)  # hours
    anes_df['total surgery time (hrs)'] = anes_df.apply(lambda x: (x['opend'] - x['opstart']) / 60, axis=1)  # hours
    # chi2(anes_df, 'death_inhosp', 'preop_htn')
    # linear_regression(anes_df, 'bmi', 'height')
