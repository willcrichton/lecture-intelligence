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


def clean_viewing_data(vd):
    users = vd.user.unique()

    remove = []
    for u in users:
        vdu = vd[vd.user == u]
        if vdu.lecture.max() < 5 or vdu.sum().minutes < 100:
            remove.append(u)

    users = [u for u in users if u not in remove]
    return vd[vd.user.isin(users)]
