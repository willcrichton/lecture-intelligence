import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter, MultipleLocator
from datetime import timedelta
import numpy as np
import pandas as pd
from intervaltree import IntervalTree
from datetime import timedelta, date
import datetime as dt
from lib.course import LECTURES, IDX_TO_ASSIGNMENT, IDX_TO_LECTURE

palette = sns.color_palette()
sns.set()


def suplabel(axis, label, label_prop=None, labelpad=5, ha='center',
             va='center'):
    ''' Add super ylabel or xlabel to the figure
    Similar to matplotlib.suptitle
    axis       - string: "x" or "y"
    label      - string
    label_prop - keyword dictionary for Text
    labelpad   - padding from the axis (default: 5)
    ha         - horizontal alignment (default: "center")
    va         - vertical alignment (default: "center")
    '''
    fig = pylab.gcf()
    xmin = []
    ymin = []
    for ax in fig.axes:
        xmin.append(ax.get_position().xmin)
        ymin.append(ax.get_position().ymin)
    xmin, ymin = min(xmin), min(ymin)
    dpi = fig.dpi
    if axis.lower() == "y":
        rotation = 90.
        x = xmin - float(labelpad) / dpi
        y = 0.5
    elif axis.lower() == 'x':
        rotation = 0.
        x = 0.5
        y = ymin - float(labelpad) / dpi
    else:
        raise Exception("Unexpected axis: x or y")
    if label_prop is None:
        label_prop = dict()
    pylab.text(x,
               y,
               label,
               rotation=rotation,
               transform=fig.transFigure,
               ha=ha,
               va=va,
               **label_prop)


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
    lec = int(lec)
    vd = vd[vd.lecture == lec]
    max_time = int(vd.end.max())+1
    bins = [0 for _ in range(0, max_time)]

    for _, row in vd.iterrows():
        for i in np.arange(np.floor(row.start), np.ceil(row.end)):
            bins[int(i)] += 1

    time = [pd.Timestamp(i * 1e9) for i in range(0, max_time)]
    ax = pd.DataFrame({
        'viewers': bins,
        'time': time
    }).plot('time', 'viewers', figsize=(15, 5), legend=False, ax=ax)
    ax.set_title(
        f'Total viewing time by second for "{IDX_TO_LECTURE[lec].name}"')
    ax.set_ylabel('Number of students viewing at time')


def minutes_watched_per_hour(vd, ax):
    vd['hour'] = vd.time.dt.hour
    ax = vd.groupby('hour').sum().plot.bar(y='minutes', legend=False, ax=ax)
    ax.set_ylabel('Total minutes watched of all lectures')
    ax.set_title('Total lecture viewing by hour of day')


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
    ax.set_title('Mean percentage of each lecture watched')


def plot_lectures(df,
                  ax,
                  minimum_mins=10,
                  course_start=dt.datetime(2019, 9, 20),
                  course_end=dt.datetime(2019, 12, 15)):
    counts = []
    start_date = course_start
    end_date = course_end
    daterange = pd.date_range(start_date, end_date)
    for date in daterange:
        unique_users = df[df['time'].dt.date == date].groupby("user")
        exceeding_minimum_mins = unique_users.sum()["minutes"] > minimum_mins
        counts.append([date, exceeding_minimum_mins.shape[0]])
    ax.bar(np.array(counts)[:, 0], np.array(counts)[:, 1], alpha=0.3)
    #ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_ylabel('Number of students watching > 10 min of any lecture')
    ax.set_title('Lecture viewing per day')


def plot_assignment(vd, ax, assignment_index):
    assignment = IDX_TO_ASSIGNMENT[int(assignment_index)]
    lectures = assignment.lectures
    count = 0
    fig = ax.figure
    fig.clf()
    fig.set_size_inches(15, 5)

    axs = fig.subplots(len(lectures),
                       1,
                       squeeze=False,
                       sharex=True,
                       sharey=True)

    fig.suptitle(
        f'Lecture viewing habits relative to deadline for "{assignment.name}"')
    for lecture in lectures:
        df = vd[vd.lecture == lecture]
        plot_lectures(df, axs[count, 0])
        axs[count, 0].axvline(x=assignment.duedate)
        axs[count, 0].grid(True)
        axs[count, 0].set_ylabel('')
        axs[count, 0].set_title(
            f'Lecture {lecture}: {IDX_TO_LECTURE[lecture].name}')
        count += 1


def mean_lateness(vd, ax):
    vd['date'] = vd['time'].dt.date
    mean_late = []
    for u in vd.user.unique():
        all_days_after = []
        vdu = vd[vd.user == u]
        for lec in LECTURES:
            all_views = vdu[vdu.lecture == lec.index].groupby(
                'date').sum().reset_index()
            first_view = all_views[all_views.minutes > 10].date.min()
            if not pd.isna(first_view):
                days_after = (first_view - lec.date.date()).days
                all_days_after.append(days_after)

        mean_late.append({
            'user': u,
            'late': pd.Series(all_days_after).median(),
            'cnt': len(all_days_after)
        })

    df = pd.DataFrame(mean_late)
    df = df[df.cnt >= 5]
    bins = np.arange(0, np.ceil(max(df.late) + .5) + 1)
    df.hist('late', ax=ax, bins=bins - 0.5)
    ax.set_xlabel('Median number of days lecture is viewed after release')
    ax.set_ylabel('Number of students\n(who watched at least 5 lectures)')
    ax.set_title(
        'How long do students wait on average before watching lecture?')
    return df

def quarter_view(vd, ax):
	ax = vd.groupby("date").sum().plot.bar(y="minutes", rot=90, figsize=(13, 5), legend=False, color='cornflowerblue')

	for assgnment in ASSIGNMENTS:
    	# Compute assignment deadline with respect to the first lecture date (ax plots lines using indexes)
    	delta = assgnment.duedate - LECTURES[0].date 
    	ax.axvline(x=delta.days, color='darkblue')
    
    	ax.set_xlabel('Date')
    	ax.set_ylabel('Minutes watched of all lectures')
    	ax.set_title('When, and for how many minutes, do students consume lecture material?')

