import pandas as pd


def parse_canvas_csv(path):
    df = pd.read_csv(path, parse_dates=['Timestamp'])
    df['End Position'] = df['Start Position'] + (df['Minutes Delivered'] * 60)
    return df.rename(
        columns={
            'Timestamp': 'time',
            'Start Position': 'start',
            'End Position': 'end',
            'Minutes Delivered': 'minutes',
            'User ID': 'user'
        })


def anonymize_canvas_csv(path):
    df = parse_canvas_csv(path)
    df.drop(columns=['UserName', 'Name', 'Email']).to_csv(path, index=False)
