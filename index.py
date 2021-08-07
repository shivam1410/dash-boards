import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
if __name__ == '__main__':
    app.run_server(debug=True)
