import pandas as pd
import matplotlib.pyplot as plt
# todo create bar chart by age by gender by op by dx

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
            gender_counts.plot(kind='bar', stacked=False, color=['blue', 'red'], alpha=0.7)

        plt.title('Gender Distribution by Age Group')
        plt.xlabel('Age Group')
        plt.ylabel('Count')
        plt.xticks(rotation=45)

        plt.legend(title='Gender')

    return plt.show()
