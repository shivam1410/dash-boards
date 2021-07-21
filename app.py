import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,url_base_pathname='/app/')
app.config.suppress_callback_exceptions = True
if __name__ == '__main__':
    app.run_server(debug=True)
