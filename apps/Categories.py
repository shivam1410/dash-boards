from datetime import datetime, date
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
from index import app
from apps.sheetService import getSheets, getSheetData

getSheets();
df = getSheetData();

Categories = {
    "Fundamental": ["Sleep", "Exercise", "Extra", "Eating", "Not-Sleep"],
    "Actions": ["Inside Task", "Outside Task", "Travel"],
    "Work": ["Office call", "office Work"],
    "Skills": ["Sketch", "Ukulele", "Read", "Meditation", "Plants"],
    "Compulsive": ["Compulsive", "Nicotine", "Social Media", "Nothing", "Masturbate"],
    "Entertainment": ["Film", "Youtube", "Music"],
    "Learning": ["Research", "Information", "Study", "Coding"],
    "People": ["Phone Call", "Text Chat", "Friends", "Family", "Conversation"],
    "Writing": ["Writing", "Time Tracker", "Expense", "Thinking"]
}

def get_all_dates(df):
    dates = df["Date"].unique()
    return dates;

def get_Category_graph(startdate, enddate):
    Category_df = df[(pd.to_datetime(df.Date)>=datetime.strptime(startdate, '%Y-%m-%d'))&(pd.to_datetime(df.Date)<=datetime.strptime(enddate,'%Y-%m-%d'))]
    # Category_df = df
    # print(Category_df)

    ########### Creating datasets
    # cat_obj = {
    #   "activity" : 0 days 00:14:00,
    #   ...
    # }
    # heirarchical_df = [["Fundamental", "Sleep", 58 days 18:56:00], ...]
    cat_obj = {}
    heirarchical_df=[];
    for key in Categories:
        DurationForOneCategory = [];
        for activity in Categories[key]:
            activityObject = Category_df[(Category_df.Category == activity)]; # taking single activity
            # Calculating sum  of all instances of that single activity
            durationForOneActivity = (pd.to_datetime(activityObject["End Time"]) - pd.to_datetime(activityObject["Start Time"])).sum();
            # Duration for one category contain duration of multiple activity
            DurationForOneCategory.append(durationForOneActivity);
            heirarchical_df.append([key,activity,durationForOneActivity])
        cat_obj[key] = pd.Series(DurationForOneCategory).sum();

    heirarchical_df = pd.DataFrame(heirarchical_df, columns=["Category","Activity","Duration"]);
    ########### Creating datasets

    ########### Creating Graphs
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "Sunburst"}]])

    fig1 = px.pie(values=cat_obj.values(), names=cat_obj.keys())
    fig2 = px.sunburst(
        heirarchical_df,
        path=["Category", "Activity"],
        values="Duration"
        )
    fig.add_trace(fig1['data'][0], row=1, col=1)
    fig.add_trace(fig2['data'][0], row=1, col=2)
    fig.update_layout(margin=dict(t=10, b=10, r=10, l=10))
    return fig;


layout = html.Div(
    id = 'Category-Graphs',
    children=[
        html.H3(children='Life spent on things from...'),
        dcc.DatePickerRange(
            id='Category-date-picker',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date.today(),
            initial_visible_month=date.today(),
            start_date = date(2021, 2, 1),
            end_date= date.today()
        ),
        html.Div(id='output-container-date-picker-range'),
        dcc.Graph(
            id='Category-data',
            figure=get_Category_graph((date(2021, 2, 1)).strftime('%Y-%m-%d'), (date.today()).strftime('%Y-%m-%d'))
        )
    ]
)


@app.callback(
    Output('Category-data', 'figure'),
    [Input('Category-date-picker', 'start_date'),
     Input('Category-date-picker', 'end_date')])
def update_output(start_date, end_date):
    fig = get_Category_graph(start_date, end_date)
    return fig