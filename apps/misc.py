from datetime import datetime, date, timedelta


def stringify(date):
    return date.strftime('%Y-%m-%d');

def get_all_dates(df):
    dates = df["Date"].unique()
    return dates;

def get_hours(time: timedelta):
    _time = time.total_seconds()/3600
    return _time
