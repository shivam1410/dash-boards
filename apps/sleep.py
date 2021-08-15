# Dash dependecies
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Python dependecies
from datetime import date, datetime, time, timedelta
import plotly.express as px
import pandas as pd

# Custom dependencies
from index import app
from .sheetService import get_ranged_sheet_data


def get_sleep_graph(startdate, enddate):
    sleep_df = get_ranged_sheet_data(startdate, enddate);
    ############# Creating Dataset
    sleep_df = sleep_df[(sleep_df.Category== "Sleep")]
    dates = sleep_df["Date"]
    stime = pd.to_datetime(sleep_df["Start Time"])
    etime = pd.to_datetime(sleep_df["End Time"])
    ############# Creating Dataset

    ############# Creating Graphs
    fig = px.timeline(sleep_df, x_start = stime, x_end = etime, y = dates)
    fig.update_yaxes(autorange='reversed')
    # to add lines and distinction in graph
    today = date.today()
    initial_time=   datetime.combine(today,time(22,00,00))
    mid_time_0    =   datetime.combine(today,time(00,00,00))
    mid_time_1    =   datetime.combine(today,time(23,59,59))
    final_time  =   datetime.combine(today,time(7,00,00))
    fig.add_vline(x=initial_time, line_dash="dot",)
    fig.add_vline(x=final_time, line_dash="dot",)
    fig.add_vrect(x0=final_time, x1=mid_time_0, row="all", col=1,
              annotation_text="", annotation_position="top left",
              fillcolor="green", opacity=0.25, line_width=0)
    fig.add_vrect(x0=mid_time_1, x1=initial_time, row="all", col=1,
              annotation_text="", annotation_position="top left",
              fillcolor="green", opacity=0.25, line_width=0)
    return fig;

layout = html.Div(
    id = 'Sleep-display-value',
    children=[
        html.Hr(style={'padding-top':"30px"}),  # horizontal line
        html.H3(children='Sleep Data'),
        html.Div(children = [
            dcc.DatePickerRange(
                id='sleep-date-picker',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date.today(),
                initial_visible_month=date.today(),
                start_date = date.today() - timedelta(7),
                end_date= date.today()
            ),
            dbc.RadioItems(
                id="sleep-data-range",
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
                id='Sleep-data',
                figure=get_sleep_graph((date.today() - timedelta(6)).strftime('%Y-%m-%d'), date.today().strftime('%Y-%m-%d'))
            )
        ]),
    ]
)

@app.callback(
    Output('Sleep-data', 'figure'),
    [Input('sleep-date-picker', 'start_date'),
     Input('sleep-date-picker', 'end_date')])
def update_output(start_date, end_date):
    fig = get_sleep_graph(start_date, end_date)
    return fig

# Callback for option button['week', 'month', 'all'], changing date in datepicker 
@app.callback(
    Output('sleep-date-picker', 'start_date'),
    [Input('sleep-date-picker', 'end_date'),
    Input('sleep-data-range', 'value')])
def update_datepicker(end_date, value):
    # To find 7days, 30 days before end_date
    enddate = date.fromisoformat(end_date);
    if(value == "month"):
        return (enddate - timedelta(30));
    if(value == 'week'):
        return (enddate - timedelta(6));
    else:
        return date(2021, 2, 1);
