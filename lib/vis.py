import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter, MultipleLocator
from datetime import timedelta

palette = sns.color_palette()


def plot_session_intervals(df):
    plt.figure(figsize=(15, 5))
    xticks = set()
    for i, row in df.iterrows():
        (start, end) = (row.start, row.end)
        plt.scatter([start, end], [i, i])
        plt.hlines(i, start, end, palette[i % len(palette)])
        xticks.add(start)
        xticks.add(end)

    plt.xticks(rotation=45)
    xaxis = plt.gca().xaxis
    xaxis.set_major_formatter(FuncFormatter(lambda x, pos: timedelta(seconds=x)))
    xaxis.set_major_locator(MultipleLocator(300))
    plt.xlabel('Video time')
    plt.ylabel('Chronologically ordered event ID')

    sns.despine()
