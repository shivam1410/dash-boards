# Dash dependecies
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Python dependecies
from datetime import date, timedelta
import plotly.express as px
import pandas as pd
import numpy as np

# Custom dependencies
from index import app
from .sheetService import get_ranged_sheet_data  
from Constants.sheetConstants import *


def get_graph_for_multiple_skills(startdate, enddate, cat):
    read_df = get_ranged_sheet_data(startdate, enddate);
    ############# Creating Dataset
    read_df = read_df[read_df["Category"].isin(cat)]
    # print(len(read_df))
    read_df["Time"] = (pd.to_datetime(read_df["End Time"]) - pd.to_datetime(read_df["Start Time"]))/np.timedelta64(1, 'h')
    ############# Creating Dataset

    ############# Creating Graphs
    fig = px.bar(read_df, x = read_df["Date"], y = read_df["Time"], title= ", ".join(cat))
    fig.update_layout(template="plotly_dark")
    return fig

def get_graph_for_single_skills(startdate, enddate, cat):
    read_df = get_ranged_sheet_data(startdate, enddate);
    # Creating Dataset
    read_df = read_df[read_df["Category"] == cat[len(cat)-1]]
    # print(len(read_df))
    read_df["Time"] = (pd.to_datetime(read_df["End Time"]) - pd.to_datetime(read_df["Start Time"]))/np.timedelta64(1, 'h')
    #############
    # Creating Dataset

    fig = px.bar(read_df, x = read_df["Date"], y = read_df["Time"], title= cat[len(cat)-1])
    fig.update_layout(template=THEME)
    return fig

layout = html.Div(
    id = 'read-display-value',
    children=[
        html.Hr(),  # horizontal line
        html.H3(children='Skills Data'),
        dcc.Dropdown(
            id="skills_dropdown",
            options = [ {'label': i, 'value':i} for i in ["Sketch", "Ukulele", "Music", "Read", "Coding"]],
            multi =True,
            value = ["Read"],
            className="dash-bootstrap"
        ),
        dcc.DatePickerRange(
            id='read-date-picker',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date.today(),
            initial_visible_month=date.today(),
            start_date = date.today() - timedelta(7),
            end_date= date.today(),
            className="dash-bootstrap"
        ),
        dbc.RadioItems(
                id="read-data-range",
                className="btn-group",
                labelClassName="btn btn-secondary",
                labelCheckedClassName="active",
                options=[
                    {"label": "7 days", "value": "week"},
                    {"label": "30 days", "value": "month"},
                    {"label": "All time", "value": "all"},
                ],
                value="week",
            ),
        html.Div(id='output-container-date-picker-range'),
        dcc.Graph(
            id='all-data',
            figure=get_graph_for_multiple_skills((date.today() - timedelta(6)).strftime('%Y-%m-%d'), (date.today()).strftime('%Y-%m-%d'), ["Read"])
        ),
        dcc.Graph(
            id='single-data',
            figure=get_graph_for_single_skills((date.today() - timedelta(6)).strftime('%Y-%m-%d'), (date.today()).strftime('%Y-%m-%d'), ["Read"])
        )
    ]
)

@app.callback(
    Output('all-data', 'figure'),
    [Input('read-date-picker', 'start_date'),
     Input('read-date-picker', 'end_date'),
     Input('skills_dropdown', 'value')])
def filter_output(start_date, end_date, value):
    fig = get_graph_for_multiple_skills(start_date, end_date, value)
    return fig

@app.callback(
    Output('single-data', 'figure'),
    [Input('read-date-picker', 'start_date'),
     Input('read-date-picker', 'end_date'),
     Input('skills_dropdown', 'value')])
def filter_output(start_date, end_date, value):
    fig = get_graph_for_single_skills(start_date, end_date, value)
    return fig

# Callback for option button['week', 'month', 'all'], changing date in datepicker 
@app.callback(
    Output('read-date-picker', 'start_date'),
    [Input('read-date-picker', 'end_date'),
    Input('read-data-range', 'value')])
def update_datepicker(end_date, value):
    # To find 7days, 30 days before end_date
    enddate = date.fromisoformat(end_date);
    if(value == "month"):
        return (enddate - timedelta(30));
    if(value == 'week'):
        return (enddate - timedelta(6));
    else:
        return date(2021, 2, 1);
