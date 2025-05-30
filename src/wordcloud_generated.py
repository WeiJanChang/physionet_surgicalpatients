import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def gen_wordcloud(df: pd.DataFrame, col_name: str, graph_title: str = None, save_file: bool = False,
                  file_name: str = None):
    text_data = ' '.join(df[col_name].dropna().astype(str))
    wordcloud = WordCloud(
        width=1600, height=800,
        background_color='white',
        colormap='tab10',
        max_words=200
    ).generate(text_data)

    plt.figure(figsize=(14, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    if graph_title is not None:
        plt.title(graph_title, fontsize=20)
    if save_file:
        plt.savefig(fname=f'{file_name}.png', format='png')
    plt.show()


if __name__ == '__main__':
    df = pd.read_csv('../test_file/clinical_data.csv')
    gen_wordcloud(df, col_name='opname', graph_title='Overview of Operation Procedure', save_file=True,
                  file_name='op_wordcloud')
