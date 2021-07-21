from datetime import datetime, date, timedelta
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
import pandas as pd

from app import app
from apps import upload

def get_all_dates(df):
    dates = df["Date"].unique()
    return dates;

def get_bullet_graph(startdate, enddate):
    try:
        df = pd.read_csv('csv/data.csv');
        bullet_df = df[(pd.to_datetime(df.Date)>=datetime.strptime(startdate, '%Y-%m-%d'))&(pd.to_datetime(df.Date)<=datetime.strptime(enddate,'%Y-%m-%d'))]
        Activities = ["Read", "Masturbate", "Sketch", "Coding", "Meditation", "office Work", "Writing"]
        dates = get_all_dates(bullet_df)
        
        # {
        #   "activity" : [1,0,1,0]
        # }
        act_diff_obj = {}
        act_obj = {}
        idx = 0
        for activity in Activities:
            act_obj[activity] = []
            act_diff_obj[activity] = []
            for date in dates:
                act_diff_obj[activity].append(idx)
                if(bullet_df[(bullet_df.Date == date)&(bullet_df.Category == activity)].size == 0):
                    act_obj[activity].append(0)
                else:
                    act_obj[activity].append(1)
            idx+=1 
        
        # print(act_obj)#
        # print(act_diff_obj)
        # colors=["Blue", "Crrimson"]
        fig = go.Figure()
        for key in act_obj:
            fig.add_trace(go.Bar(x=dates, y=act_obj[key],
                    base=act_diff_obj[key],
                    # marker_color=colors[],
                    name=key
                ))

        fig.update_layout( barmode="stack")
        return fig;
    except:
        app.layout = upload.layout


layout = html.Div(
    # id = 'Sleep-display-value',
    children=[
        html.H3(children='Activity Data'),
        dcc.DatePickerRange(
            id='bullet-date-picker',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date.today(),
            initial_visible_month=date.today(),
            start_date = date.today() - timedelta(30),
            end_date= date.today()
        ),
        html.Div(id='output-container-date-picker-range'),
        dcc.Graph(
            id='bullet-data',
            figure=get_bullet_graph((date.today() - timedelta(30)).strftime('%Y-%m-%d'), (date.today()).strftime('%Y-%m-%d'))
        )
    ]
)


@app.callback(
    Output('bullet-data', 'figure'),
    [Input('bullet-date-picker', 'start_date'),
     Input('bullet-date-picker', 'end_date')])
def update_output(start_date, end_date):
    fig = get_bullet_graph(start_date, end_date)
    return fig