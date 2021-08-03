import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os
import datetime as dt
import pandas as pd
from index import app
from apps import main
from apps.sheetService import getSheets



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
server = app.server

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/app/dashboard':
        return main.create_bar_graph()
    else:
        return '404'

if __name__ == '__main__':
    # app.run_server()
    app.run_server()