
from datetime import datetime, date, timedelta
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import pandas as pd

from index import app
from apps.sheetService import getSheets, getSheetData

# getSheets();

def get_ranged(startdate, enddate):
    # df = pd.read_csv('csv/data.csv');
    df = getSheetData();
    read_df = df[(pd.to_datetime(df.Date)>=datetime.strptime(startdate, '%Y-%m-%d'))&(pd.to_datetime(df.Date)<=datetime.strptime(enddate,'%Y-%m-%d' ))]
    return read_df

def get_all_graph(startdate, enddate, cat):
    # print(cat, len(cat))
    read_df = get_ranged(startdate, enddate)
    read_df = read_df[read_df["Category"].isin(cat)]
    # print(len(read_df))
    read_df["Time"] = pd.to_datetime(read_df["End Time"]) - pd.to_datetime(read_df["Start Time"])
    fig = px.bar(read_df, x = read_df["Date"], y = read_df["Time"], title= ", ".join(cat))
    return fig

def get_single_graph(startdate, enddate, cat):
    # print(cat, len(cat))
    read_df = get_ranged(startdate, enddate)
    read_df = read_df[read_df["Category"] == cat[len(cat)-1]]
    # print(len(read_df))
    read_df["Time"] = pd.to_datetime(read_df["End Time"]) - pd.to_datetime(read_df["Start Time"])
    fig = px.bar(read_df, x = read_df["Date"], y = read_df["Time"], title= cat[len(cat)-1])
    return fig

layout = html.Div(
    id = 'read-display-value',
    children=[
        html.Hr(),  # horizontal line
        html.H3(children='Read Data'),
        dcc.Dropdown(
            id="skills_dropdown",
            options = [ {'label': i, 'value':i} for i in ["Sketch", "Ukulele", "Music", "Read", "Coding"]],
            multi =True,
            value = ["Read"]
        ),
        dcc.DatePickerRange(
            id='read-date-picker',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date.today(),
            initial_visible_month=date.today(),
            start_date = date.today() - timedelta(7),
            end_date= date.today()
        ),
        html.Div(id='output-container-date-picker-range'),
        dcc.Graph(
            id='all-data',
            figure=get_all_graph("2017-08-01", "2021-06-18", ["Read"])
        ),
        dcc.Graph(
            id='single-data',
            figure=get_single_graph("2017-08-01", "2021-06-18", ["Read"])
        )
    ]
)

@app.callback(
    Output('all-data', 'figure'),
    [Input('read-date-picker', 'start_date'),
     Input('read-date-picker', 'end_date'),
     Input('skills_dropdown', 'value')])
def filter_output(start_date, end_date, value):
    fig = get_all_graph(start_date, end_date, value)
    return fig

@app.callback(
    Output('single-data', 'figure'),
    [Input('read-date-picker', 'start_date'),
     Input('read-date-picker', 'end_date'),
     Input('skills_dropdown', 'value')])
def filter_output(start_date, end_date, value):
    fig = get_single_graph(start_date, end_date, value)
    return fig