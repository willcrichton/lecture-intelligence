import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter, MultipleLocator
from datetime import timedelta
import numpy as np
import pandas as pd
from intervaltree import IntervalTree

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
    xaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: timedelta(seconds=x)))
    xaxis.set_major_locator(MultipleLocator(300))
    plt.xlabel('Video time')
    plt.ylabel('Chronologically ordered event ID')

    sns.despine()


def lecture_heatmap(vd, ax, lec):
    vd = vd[vd.lecture == int(lec)]
    bins = [0 for _ in range(0, 90 * 60)]

    for _, row in vd.iterrows():
        for i in np.arange(np.floor(row.start), np.ceil(row.end)):
            bins[int(i)] += 1

    time = [pd.Timestamp(i * 1e9) for i in range(0, 90 * 60)]
    ax = pd.DataFrame({
        'viewers': bins,
        'time': time
    }).plot('time', 'viewers', figsize=(15, 5), legend=False, ax=ax)
    ax.set_ylabel('Number of students viewing at time')


def minutes_watched_per_hour(vd, ax):
    vd['hour'] = vd.time.dt.hour
    ax = vd.groupby('hour').sum().plot.bar(y='minutes', legend=False, ax=ax)
    ax.set_ylabel('Total minutes watched of all lectures')


def compute_coverage(lec_vd):
    START = 60 * 5
    END = 60 * 75
    t = IntervalTree()
    for _, row in lec_vd.iterrows():
        t.addi(row.start, row.end)
    t.merge_overlaps()
    t.chop(0, START)
    if len(t) == 0:
        return 0
    t.chop(END, max([i.end for i in t]))

    return sum([i.end - i.begin for i in t]) / (END - START)


def coverage_per_lecture(vd, ax):
    users = vd.user.unique()
    cov_rows = []
    for u in users:
        for lec in range(1, 14):
            lec_vd = vd[(vd.user == u) & (vd.lecture == lec)]
            cov_rows.append({
                'user': u,
                'lecture': lec,
                'coverage': compute_coverage(lec_vd)
            })

    cov_df = pd.DataFrame(cov_rows)
    ax = cov_df[cov_df.coverage > 0.05].groupby('lecture').mean().plot.bar(
        y='coverage', ylim=(0, 1), legend=False, ax=ax)
    ax.set_ylabel('Coverage')
