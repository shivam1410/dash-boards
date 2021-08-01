
from datetime import datetime, date, timedelta
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import pandas as pd

from index import app
from apps.sheetService import getSheets, getSheetData

getSheets();
df = getSheetData();

def get_sleep_graph(startdate, enddate):
    if(df.size > 0):
        sleep_df = df[(pd.to_datetime(df.Date)>=datetime.strptime(startdate, '%Y-%m-%d'))&(pd.to_datetime(df.Date)<=datetime.strptime(enddate,'%Y-%m-%d' ))]
        sleep_df = sleep_df[(sleep_df.Category== "Sleep")]
        date = sleep_df["Date"]
        stime = pd.to_datetime(sleep_df["Start Time"])
        etime = pd.to_datetime(sleep_df["End Time"])

        fig = px.timeline(sleep_df, x_start = stime, x_end = etime, y = date, 
                        title= "Sleepdata")
        fig.update_yaxes(autorange='reversed')
        return fig;

layout = html.Div(
    id = 'Sleep-display-value',
    children=[
        html.H3(children='Sleep Data'),
        html.Div(children = [
            dcc.DatePickerRange(
                id='sleep-date-picker',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date.today(),
                initial_visible_month=date.today(),
                start_date = date.today() - timedelta(7),
                end_date= date.today()
            ),
            html.Div(id='output-container-date-picker-range'),
            dcc.Graph(
                id='Sleep-data',
                figure=get_sleep_graph("2017-08-01", "2021-06-18")
            )
        ]),
    ]
)

@app.callback(
    Output('Sleep-data', 'figure'),
    [Input('sleep-date-picker', 'start_date'),
     Input('sleep-date-picker', 'end_date')])
def update_output(start_date, end_date):
    fig = get_sleep_graph(start_date, end_date)
    return fig