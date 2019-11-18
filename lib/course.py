from dataclasses import dataclass
from datetime import datetime as dt
from typing import List
import os
import pandas as pd
import json


@dataclass
class Lecture:
    index: int
    name: str
    date: dt

    def path(self):
        date = self.date.strftime('%-m_%-d_%Y')
        return f'../data/viewing/{date}.csv'

    def viewing_data(self):
        df = pd.read_csv(self.path(), parse_dates=['time'])
        df['lecture'] = self.index
        return df

    @classmethod
    def from_json(cls, json):
        return cls(index=json['index'],
                   name=json['name'],
                   date=dt.strptime(json['date'], '%m/%d/%Y'))

    def to_json(self):
        return {
            'index': self.index,
            'name': self.name,
            'date': dt.strftime(self.date, '%m/%d/%Y')
        }


@dataclass
class Assignment:
    index: int
    name: str
    duedate: dt
    lectures: List[int]

    def to_json(self):
        return {
            'index': self.index,
            'name': self.name,
            'duedate': dt.strftime(self.duedate, '%m/%d/%Y'),
            'lectures': self.lectures
        }

    def lecture_obj(self):
        return [IDX_TO_LECTURE[lec] for lec in self.lectures]

    @classmethod
    def from_json(cls, json):
        return cls(index=json['index'],
                   name=json['name'],
                   lectures=json['lectures'],
                   duedate=dt.strptime(json['duedate'], '%m/%d/%Y'))


LECTURE_JSON_PATH = os.path.abspath('../data/lectures.json')


def load_lectures():
    if os.path.isfile(LECTURE_JSON_PATH):
        return [
            Lecture.from_json(lec)
            for lec in json.load(open(LECTURE_JSON_PATH, 'r'))
        ]
    else:
        return []


LECTURES = load_lectures()

IDX_TO_LECTURE = {l.index: l for l in LECTURES}
NAME_TO_LECTURE = {l.name: l for l in LECTURES}

ASSIGNMENT_JSON_PATH = os.path.abspath('../data/assignments.json')


def load_assignments():
    if os.path.isfile(ASSIGNMENT_JSON_PATH):
        return [
            Assignment.from_json(lec)
            for lec in json.load(open(ASSIGNMENT_JSON_PATH, 'r'))
        ]
    else:
        return []


ASSIGNMENTS = load_assignments()

IDX_TO_ASSIGNMENT = {a.index: a for a in ASSIGNMENTS}
NAME_TO_ASSIGNMENT = {a.name: a for a in ASSIGNMENTS}
