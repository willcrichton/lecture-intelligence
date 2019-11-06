from flask import Flask, request
import tempfile
from zipfile import ZipFile
import os
import etl

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    with tempfile.NamedTemporaryFile(suffix='.zip') as temp:
        name = next(request.files.keys())
        uploaded = request.files[name]
        uploaded.save(temp.name)
        temp.flush()

        date, _ = os.path.splitext(name)

        with ZipFile(temp.name, 'r') as zp:
            raw_name = zp.namelist()[0]
            zp.extractall(path='../data')

        os.rename(f'../data/{raw_name}', f'../data/{date}.csv')
        etl.anonymize_canvas_csv(f'../data/{date}.csv')

        return ''

if __name__ == '__main__':
    app.run()
