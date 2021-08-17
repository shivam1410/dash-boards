# Dash dependecies
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Custom dependecies
from index import app
from apps import main

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
# Creating server for Heroku deployment
server = app.server

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/app/dashboard':
        return main.create_bar_graph()
    else:
        return '404'

if __name__ == '__main__':
    app.run_server()
    # app.run_server()