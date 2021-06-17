
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from app import app

df = pd.read_csv('reading.csv');

fig = px.bar(df, x = df["Date"], y = df["Time"], title= "Description")

layout = html.Div(
    # id = 'read-display-value',
    children=[

    html.H3(children='read Data'),

    dcc.Graph(
        id='read-data',
        figure=fig
    )
])



@app.callback(
    Output('read-display-value', 'children'),
    Input('read-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)