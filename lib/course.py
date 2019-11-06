from lib.etl import parse_canvas_csv
from dataclasses import dataclass
import datetime as dt
from typing import List


@dataclass
class Lecture:
    index: int
    name: str
    date: dt.datetime

    def path(self):
        date = self.date.strftime('%-m_%-d_%Y')
        return f'../data/viewing/{date}.csv'

    def viewing_data(self):
        return parse_canvas_csv(self.path())


@dataclass
class Assignment:
    index: int
    name: str
    duedate: dt.datetime
    lectures: List[Lecture]


LECTURES = [
    Lecture(index=1, name='Introduction', date=dt.datetime(2019, 9, 23)),
    Lecture(index=2, name='Syntax and semantics', date=dt.datetime(2019, 9, 25)),
    Lecture(index=3, name='Lambda calculus', date=dt.datetime(2019, 9, 30)),
    Lecture(index=4, name='Type systems', date=dt.datetime(2019, 10, 2)),
    Lecture(index=5, name='Functional basics', date=dt.datetime(2019, 10, 7)),
    Lecture(index=6, name='Algebraic data types', date=dt.datetime(2019, 10, 9)),
    Lecture(index=7, name='Parametric types', date=dt.datetime(2019, 10, 14)),
    # No lecture 8
    Lecture(index=9, name='Mutability', date=dt.datetime(2019, 10, 21)),
    Lecture(index=10, name='Control flow: branches', date=dt.datetime(2019, 10, 23)),
    Lecture(index=11, name='Control flow: functions', date=dt.datetime(2019, 10, 28)),
    Lecture(index=12, name='Memory safety', date=dt.datetime(2019, 10, 30)),
    Lecture(index=13, name='Traits', date=dt.datetime(2019, 11, 4))
]

ASSIGNMENTS = [
    Assignment(index=1,
               name='JSafe',
               duedate=dt.datetime(2019, 10, 2),
               lectures=[LECTURES[1]]),
    Assignment(index=2,
               name='Lambda Theory',
               duedate=dt.datetime(2019, 10, 10),
               lectures=LECTURES[2:4]),
    Assignment(index=3,
               name='106 Redux',
               duedate=dt.datetime(2019, 10, 16),
               lectures=LECTURES[4:6]),
    Assignment(index=4,
               name='Interpreter',
               duedate=dt.datetime(2019, 10, 23),
               lectures=LECTURES[6]),
    Assignment(index=5,
               name='WebAssembly',
               duedate=dt.datetime(2019, 10, 30),
               lectures=LECTURES[7:10]),
    Assignment(index=6,
               name='Linear Types',
               duedate=dt.datetime(2019, 11, 7),
               lectures=LECTURES[10])
]
