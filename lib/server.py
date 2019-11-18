from flask import Flask, render_template, request, Response, jsonify
import os
import matplotlib.pyplot as plt
import sys
import pandas as pd
import io
from matplotlib.figure import Figure
from pickle_cache import PickleCache
import seaborn as sns
import json
import tempfile
from zipfile import ZipFile
from datetime import datetime as dt
from pathlib import Path

sys.path.append('..')

from lib.course import load_lectures, Lecture, LECTURE_JSON_PATH, load_assignments, ASSIGNMENT_JSON_PATH
from lib.etl import clean_viewing_data, anonymize_panopto_data
import lib.vis as vis


def load_clean_data():
    return clean_viewing_data(
        pd.concat([l.viewing_data() for l in load_lectures()]))


pcache = PickleCache('../chart-cache')
app = Flask(__name__, root_path=os.path.abspath("../dashboard"))
vd = load_clean_data()


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/input')
def input():
    return render_template('input.html')


@app.route('/api/lectures', methods=['GET', 'POST'])
def lectures():
    if request.method == 'POST':
        lecture_json = request.get_json()
        json.dump(lecture_json, open(LECTURE_JSON_PATH, 'w'))
        return ''
    else:
        return jsonify([l.to_json() for l in load_lectures()])


@app.route('/api/assignments', methods=['GET', 'POST'])
def assignments():
    if request.method == 'POST':
        assignment_json = request.get_json()
        print(assignment_json)
        json.dump(assignment_json, open(ASSIGNMENT_JSON_PATH, 'w'))
        return ''
    else:
        return jsonify([l.to_json() for l in load_assignments()])


@app.route('/api/plot.svg')
def plot():
    args = dict(request.args)
    kind = args.pop('kind')
    if hasattr(vis, kind):

        def get_svg():
            fig = Figure()
            ax = getattr(vis, kind)(vd, fig.add_subplot(1, 1, 1), **args)
            sns.despine(fig=fig)
            f = io.BytesIO()
            fig.savefig(f, format='svg')
            return f.getvalue()

        return Response(pcache.get(request.query_string, get_svg),
                        mimetype='image/svg+xml')

    else:
        return 'Bad request'


@app.route('/api/upload_viewing_data', methods=['POST'])
def upload_viewing_data():
    with tempfile.NamedTemporaryFile(suffix='.zip') as temp:
        name = next(request.files.keys())
        uploaded = request.files[name]
        uploaded.save(temp.name)
        temp.flush()

        date, _ = os.path.splitext(name)

        Path('../data/viewing').mkdir(parents=True, exist_ok=True)

        with ZipFile(temp.name, 'r') as zp:
            raw_name = zp.namelist()[0]
            zp.extractall(path='../data/viewing')

        os.rename(f'../data/viewing/{raw_name}', f'../data/viewing/{date}.csv')
        anonymize_panopto_data(f'../data/viewing/{date}.csv')

        return ''


@app.route('/api/generate_lecture_json')
def generate_lecture_json():
    global vd
    lecture_dates = [
        os.path.splitext(os.path.basename(path))[0]
        for path in os.listdir('../data/viewing')
    ]
    lecture_json = [{
        'index': i + 1,
        'date': dt.strftime(date, '%m/%d/%Y'),
        'name': ''
    } for i, date in enumerate(
        sorted([dt.strptime(date, '%m_%d_%Y') for date in lecture_dates]))]

    json.dump(lecture_json, open(LECTURE_JSON_PATH, 'w'))
    vd = load_clean_data()
    return ''


if __name__ == '__main__':
    app.run()
