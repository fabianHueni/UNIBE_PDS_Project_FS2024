from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from datetime import date

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('../preprocessed_data/minutes.csv')

app.layout = html.Div([
    html.H1(children='FitBit Dashboard', style={'textAlign':'center'}),
    html.Div([
        dcc.Dropdown(df.Id.unique(), '1503960366', id='subject-selection', className="four columns"),
        dcc.DatePickerRange(
            id='date-picker-range',
            display_format='DD.MM.Y',
            first_day_of_week=1,
            min_date_allowed=date(2016, 3, 11),
            max_date_allowed=date(2016, 5, 12),
            initial_visible_month=date(2016, 3, 11),
        ),
    ], className="container"),

    html.Div([
        html.H2(children='Steps', style={'textAlign':'center'}),
        dcc.Graph(id='steps-graph'),
    ]),

    html.Div([
        html.H2(children='Calories', style={'textAlign':'center'}),
        dcc.Graph(id='calories-graph'),
    ]),

    html.Div([
        html.H2(children='Intensity', style={'textAlign':'center'}),
        dcc.Graph(id='intensity-graph'),
    ]),

    html.Div([
        html.H2(children='Sleep', style={'textAlign':'center'}),
        dcc.Graph(id='sleep-graph'),
    ]),

    html.Div([
        html.H2(children='Heartrate', style={'textAlign':'center'}),
        dcc.Graph(id='heartrate-graph'),
    ]),
])


@callback(
    [
        Output('steps-graph', 'figure'),
        Output('calories-graph', 'figure'),
        Output('intensity-graph', 'figure'),
        Output('sleep-graph', 'figure'),
        Output('heartrate-graph', 'figure'),
    ],
    [
        Input('subject-selection', 'value'),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date')
     ]
)
def update_steps(subject, date_range_start, date_range_end):
    dff = select_subject(df, subject)
    dff = select_date_range(dff, date_range_start, date_range_end)

    return (px.line(dff, x='DateTime', y='Steps'),
            px.line(dff, x='DateTime', y='Calories'),
            px.line(dff, x='DateTime', y='Intensity'),
            px.line(dff, x='DateTime', y='Sleep'),
            px.line(dff, x='DateTime', y='Heartrate'),
            )

def select_subject(dff, subject):
    """
    Selects the subject based on the given value.

    :param subject: The subject to select
    :return: The selected subject
    """
    return dff[dff['Id'] == subject]

def select_date_range(dff, date_range_start, date_range_end):
    """
    Filters the DataFrame based on the selected date range. If no date range is selected, the default range is used.

    :param dff: The dateframe to filter on
    :param date_range_start: The start date of the range
    :param date_range_end: The end date of the range
    :return: The filtered DataFrame
    """
    if date_range_start is None:
        date_range_start = '2016-03-11'
    if date_range_end is None:
        date_range_end = '2016-05-12'

    date_range_start = pd.to_datetime(date_range_start)
    date_range_end = pd.to_datetime(date_range_end)

    return dff[(pd.to_datetime(dff['DateTime']) >= date_range_start)
               & (pd.to_datetime(dff['DateTime']) <= date_range_end)]

if __name__ == '__main__':
    app.run(debug=True)