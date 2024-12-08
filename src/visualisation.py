import pandas
import pandas as pd
import matplotlib.pyplot as plt

__all__ = [""]


# todo create dashboard by age by gender by op by dx

def bar_chart(df: pd.DataFrame, age_group: str = None, gender: str = None):
    """
    create a bar chart to show how many "gender" in "age group"
    :param df: anes_df
    :param age_group: age group
    :param gender: male and female
    :return: bar chart
    """
    if age_group is not None:
        df['age'] = df['age'].str.replace('>', '')
        df['age'] = df['age'].astype(float).astype(int)  # convert data into int type
        bins = [0, 3, 12, 19, 64, 110]  # grouping age
        labels = ['Toddler (0-3)', 'Child (3-12)', 'Teen (12-19)', 'Adult (19-64)', 'Older people (64-110)']
        df["age group"] = pd.cut(df.age, bins=bins, labels=labels, right=False)
        if gender is not None:
            gender_counts = df.groupby(['age group', 'sex'], observed=False).size().unstack(fill_value=0)
            # observed: True, show observed values for categorical groupers; False, show all values for categorical groupers
            # unstack(fill_value = ), value to use when replacing NaN values
            gender_counts.plot(kind='bar', stacked=False, color=['blue', 'red'], alpha=0.7)

        plt.title('Gender Distribution by Age Group')
        plt.xlabel('Age Group')
        plt.ylabel('Count')
        plt.xticks(rotation=45)

        plt.legend(title='Gender')

    return plt.show()


def figure_by_gender(df: pd.DataFrame,
                     filter_col: str,
                     apply_filter: bool = True,
                     bar_chart: bool = False,
                     pie_chart: bool = False,
                     filter_val: str | int = None):
    """
    Generates a bar chart showing gender distribution for a specific column.


    :param df: dataframe
    :param filter_col: column name to filter the data
    :param apply_filter: whether to filter the df based on the 'filter_value'
    :param filter_val:value to filter the filter_column
    :param bar_chart: bar chart
    :param pie_chart: pie chart
    :return: plot
    """
    df = df.copy()
    if apply_filter:
        if filter_val is None:
            raise ValueError("'filter_value' must be provided if 'apply_filter' is enabled.")
        df = df[df[filter_col] == filter_val]

    # grouping data and create bar chart
    gender_counts: pandas.Series = df.groupby(['sex']).size()
    if bar_chart:
        # Apply a function groupby to each row or column of a DataFrame.
        # size(): Compute group sizes
        gender_counts.plot(kind='bar', color=['blue', 'red'], alpha=0.7, )
    if pie_chart:
        gender_counts.plot(kind='pie', color=['blue', 'red'],
                           autopct=lambda pct: f'{int(pct / 100. * gender_counts.sum())} ({pct:.1f}%)',
                           labels=gender_counts.index)

    plt.xlabel("Gender")
    plt.ylabel("Count")
    plt.xticks(rotation=0)  # adjust x-axis label rotation
    plt.title(f"Gender distribution of {filter_col} in {filter_val}")
    plt.show()
