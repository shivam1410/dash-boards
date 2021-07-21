from os import path
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from index import app
from apps import sleep, reading, bullets, Leisure, upload


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

server = app.server

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/app/sleep':
        return sleep.layout
    elif pathname == '/app/read':
        return reading.layout
    elif pathname == '/app/bullets':
        return bullets.layout
    elif pathname == '/app/test':
        return Leisure
    elif pathname == '/app/upload':
        return upload.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)