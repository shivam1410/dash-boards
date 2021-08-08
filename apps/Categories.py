# Dash dependecies
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Python dependecies
from datetime import date, timedelta
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd

# Custom dependencies
from index import app
from .sheetService import get_ranged_sheet_data
from .misc import *

CATEGORIES = {
    # "Eating" always comes with other activity like Film, music, Friends
    # Hence, It should'nt be quantified in time duration
    "Fundamental": ["Sleep", "Exercise", "Extra", "Not-Sleep", "Office call", "office Work"],
    "Actions": ["Inside Task", "Outside Task", "Travel"],
    "Pseudo Leisure": ["Compulsive", "Nicotine", "Social Media", "Nothing", "Masturbate", "Film", "Youtube", "Music", ],
    "Learning": ["Research", "Information", "Study", "Coding", "Sketch", "Ukulele", "Read", "Meditation", "Plants", "Writing", "Time Tracker", "Expense", "Thinking"],
    "People": ["Phone Call", "Text Chat", "Friends", "Family", "Conversation"]
}
# CATEGORIES_temp = {
#     "Fundamental": ["Sleep", "Exercise", "Extra", "Not-Sleep"],
#     "Actions": ["Inside Task", "Outside Task", "Travel"],
#     "Work": ["Office call", "office Work"],
#     "Skills": ["Sketch", "Ukulele", "Read", "Meditation", "Plants"],
#     "Compulsive": ["Compulsive", "Nicotine", "Social Media", "Nothing", "Masturbate"],
#     "Entertainment": ["Film", "Youtube", "Music"],
#     "Learning": ["Research", "Information", "Study", "Coding"],
#     "Writing": ["Writing", "Time Tracker", "Expense", "Thinking"]
#     "People": ["Phone Call", "Text Chat", "Friends", "Family", "Conversation"]
# }
def get_Category_graph(startdate, enddate):
    Category_df = get_ranged_sheet_data(startdate, enddate);

    ############# Creating datasets
    # cat_obj = {
    #   "activity" : 0 days 00:14:00,
    #   ...
    # }
    # heirarchical_df = [["Fundamental", "Sleep", 58 days 18:56:00], ...]
    cat_obj = {}
    heirarchical_df=[];
    for key in CATEGORIES:
        DurationForOneCategory = [];
        for activity in CATEGORIES[key]:
            activityObject = Category_df[(Category_df.Category == activity)]; # taking single activity
            # Calculating sum  of all instances of that single activity
            durationForOneActivity = (pd.to_datetime(activityObject["End Time"]) - pd.to_datetime(activityObject["Start Time"])).sum();
            # Duration for one category contain duration of multiple activity
            hours = get_hours(durationForOneActivity)
            DurationForOneCategory.append(hours);
            heirarchical_df.append([key,activity,hours])
        cat_obj[key] = pd.Series(DurationForOneCategory).sum()

    heirarchical_df = pd.DataFrame(heirarchical_df, columns=["Category","Activity","Hours"]);
    ############# Creating datasets

    ############# Creating Graphs
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "sunburst"}]])
    fig1 = px.pie(heirarchical_df, names='Category', values='Hours')
    fig2 = px.sunburst(
            heirarchical_df,
            path=["Category", "Activity"],
            values="Hours",
            hover_name="Hours"
        )
    fig.add_trace(fig1['data'][0], row=1, col=1)
    fig.add_trace(fig2['data'][0], row=1, col=2)
    fig.update_layout(margin=dict(t=10, b=10, r=10, l=10))
    return fig;


layout = html.Div(
    id = 'Category-Graphs',
    children=[
        html.Hr(style={'padding-top':"30px"}),  # horizontal line
        html.H3(children='Life spent on things from...',className="header"),
        html.Div(children=[
            dcc.DatePickerRange(
                id='Category-date-picker',
                min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date.today(),
                initial_visible_month=date.today(),
                start_date = date(2021, 2, 1),
                end_date= date.today()
            ),
            dbc.RadioItems(
                id="category-data-range",
                className="btn-group",
                labelClassName="btn btn-secondary",
                labelCheckedClassName="active",
                options=[
                    {"label": "7 days", "value": "week"},
                    {"label": "30 days", "value": "month"},
                    {"label": "All time", "value": "all"},
                ],
                value="week",
            )
        ]),
        
        html.Div(id='category-time-selection'),
        dcc.Graph(
            id='Category-data',
            figure=get_Category_graph((date.today() - timedelta(6)).strftime('%Y-%m-%d'), (date.today()).strftime('%Y-%m-%d'))
        )
    ]
)

# Callback for DatePicker 
@app.callback(
    Output('Category-data', 'figure'),
    [Input('Category-date-picker', 'start_date'),
     Input('Category-date-picker', 'end_date')])
def update_output(start_date, end_date):
    fig = get_Category_graph(start_date, end_date)
    return fig

# Callback for option button['week', 'month', 'all'], changing date in datepicker 
@app.callback(
    Output('Category-date-picker', 'start_date'),
    [Input('category-data-range', 'value')])
def update_datepicker(value):
    if(value == "month"):
        return (date.today()- timedelta(30));
    if(value == 'week'):
        return (date.today() - timedelta(6));
    else:
        return (date(2021, 2, 1));