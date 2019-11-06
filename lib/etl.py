import pandas as pd

def parse_canvas_csv(path):
    df = pd.read_csv(path, parse_dates=['Timestamp'])
    df['End Position'] = df['Start Position'] + (df['Minutes Delivered'] * 60)
    return df
