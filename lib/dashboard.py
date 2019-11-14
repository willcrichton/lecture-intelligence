from flask import Flask, render_template, request, Response
import os
import matplotlib.pyplot as plt
import sys
import pandas as pd
import io
from matplotlib.figure import Figure
from pickle_cache import PickleCache
import seaborn as sns

sys.path.append('..')

from lib.course import LECTURES
from lib.etl import clean_viewing_data
import lib.vis as vis

pcache = PickleCache('./.cache')
app = Flask(__name__, root_path=os.path.abspath("../dashboard"))
vd = clean_viewing_data(pd.concat([l.viewing_data() for l in LECTURES]))


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/plot.svg')
def plot():
    kind = request.args.get('kind')
    if hasattr(vis, kind):

        def get_svg():
            fig = Figure()
            ax = getattr(vis, kind)(vd, fig.add_subplot(1, 1, 1))
            sns.despine(fig=fig)
            f = io.BytesIO()
            fig.savefig(f, format='svg')
            return f.getvalue()

        return Response(pcache.get(kind, get_svg), mimetype='image/svg+xml')

    else:
        return 'Bad request'


if __name__ == '__main__':
    app.run()
