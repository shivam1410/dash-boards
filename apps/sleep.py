
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from app import app

df = pd.read_csv('Time Tracker - Sleep.csv');

date = df["Date"]
stime = pd.to_datetime(df["Start Time"])
etime = pd.to_datetime(df["End Time"])

fig = px.timeline(df, x_start = stime, x_end = etime, y = date, title= "Sleepdata")
fig.update_yaxes(autorange='reversed')

layout = html.Div(
    # id = 'Sleep-display-value',
    children=[

    html.H3(children='Sleep Data'),
    dcc.Dropdown(
        id = 'Sleep-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    dcc.Graph(
        id='Sleep-data',
        figure=fig
    )
])



@app.callback(
    Output('Sleep-display-value', 'children'),
    Input('Sleep-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)